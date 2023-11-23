#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import re
import time

from datetime import datetime, timedelta
from shlex import quote

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase

SCRIPT = '''
filename=$1
shift
opts="$@"

if [ -n "$filename" ]; then
    backup_file=%tmpdir%/viosupg.backup
    if [ "$filename" == "-" ]; then
        > $backup_file
    else
        cp "$filename" $backup_file
    fi
    # Preserve SSH host identification during upgrade
    ls /etc/ssh/ssh_host* >> $backup_file
    ls /etc/ssh/sshd_config >> $backup_file
    # Preserve SSH authorized keys of the user during upgrade
    ls ~/.ssh/authorized_keys* >> $backup_file

    opts="$opts -g $backup_file"
fi

nohup /usr/ios/cli/ioscli viosupgrade -l $opts &
sleep 5
exit 0
'''


class ActionModule(ActionBase):
    TRANSFERS_FILES = True
    _VALID_ARGS = frozenset((
        'image_file',
        'mksysb_install_disks',
        'cluster',
        'filename',
        'timeout',
        'post_install_binary',
        'pre_restore_script',
        'skipclusterstate',
        'skiprestore',
        'preserve_devname',
        'wait_reboot'
    ))

    ioscli_cmd = '/usr/ios/cli/ioscli'

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)

    def get_ioslevel(self):
        """
        Return the latest installed maintenance level of the system.
        """
        cmd = "%s ioslevel" % self.ioscli_cmd
        cmd_result = self._low_level_execute_command(cmd)
        if cmd_result['rc'] != 0:
            return None
        ioslevel = cmd_result['stdout'].splitlines()[0]

        if not re.match(r"^\d+\.\d+\.\d+\.\d+$", ioslevel):
            return None

        return ioslevel

    def cluster_membership(self):
        """
        Return True if VIOS is part of a cluster, False otherwise.
        """
        cmd = "%s cluster -list -field cluster_name -fmt ," % self.ioscli_cmd
        cmd_result = self._low_level_execute_command(cmd)
        return cmd_result['rc'] == 0

    def get_vg_disks(self, vgname):
        """
        Return the list of hdisks that belong to the specified VG.
        """
        cmd = "%s lspv -field NAME VG -fmt ," % self.ioscli_cmd
        cmd_result = self._low_level_execute_command(cmd)
        if cmd_result['rc'] != 0:
            return None

        hdisks = []
        for line in cmd_result['stdout'].splitlines():
            fields = line.split(',', 2)
            if len(fields) == 2 and fields[1] == vgname:
                hdisks.append(fields[0])
        return hdisks

    def run(self, tmp=None, task_vars=None):
        self._supports_check_mode = False
        self._supports_async = True

        if task_vars is None:
            task_vars = {}

        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get('skipped', False) or result.get('failed', False):
            return result

        # Validate arguments
        image_file = self._task.args.get('image_file', None)
        if image_file is None:
            result['failed'] = True
            return result
        mksysb_install_disks = self._task.args.get('mksysb_install_disks', None)
        if mksysb_install_disks is None:
            result['failed'] = True
            return result
        if isinstance(mksysb_install_disks, (list, tuple)):
            mksysb_install_disks = list(mksysb_install_disks)
        else:
            mksysb_install_disks = [mksysb_install_disks]
        cluster = self._task.args.get('cluster', None)
        if cluster is not None:
            if not isinstance(cluster, bool):
                cluster = boolean(self._templar.template(cluster), strict=False)
        post_install_binary = self._task.args.get('post_install_binary', None)
        pre_restore_script = self._task.args.get('pre_restore_script', None)
        skipclusterstate = self._task.args.get('skipclusterstate', False)
        skiprestore = self._task.args.get('skiprestore', False)
        preserve_devname = self._task.args.get('preserve_devname', False)

        if pre_restore_script and skiprestore:
            result['failed'] = True
            result['msg'] = 'Using pre_restore_script and skiprestore together is prohibited.'
            return result
        if not isinstance(skipclusterstate, bool):
            skipclusterstate = boolean(self._templar.template(skipclusterstate), strict=False)
        if not isinstance(skiprestore, bool):
            skiprestore = boolean(self._templar.template(skiprestore), strict=False)
        wait_reboot = self._task.args.get('wait_reboot', True)
        if not isinstance(wait_reboot, bool):
            wait_reboot = boolean(self._templar.template(wait_reboot), strict=False)

        filename = self._task.args.get('filename', None)
        timeout = int(self._task.args.get('timeout', 60))

        result['ioslevel'] = {}

        # Retrieve the ioslevel before the upgrade
        result['ioslevel']['before'] = self.get_ioslevel()

        # Retrieve viosupgrade supported options from usage
        cmd = "%s viosupgrade -h" % self.ioscli_cmd
        cmd_result = self._low_level_execute_command(cmd)
        if cmd_result['rc'] != 0:
            result['stdout'] = cmd_result['stdout']
            result['stderr'] = cmd_result['stderr']
            result['msg'] = 'Command \'{0}\' failed with return code {1}.'.format(cmd, cmd_result['rc'])
            result['failed'] = True
            return result

        has_g_opt = re.search(r"^-g\s+", cmd_result['stdout'], re.MULTILINE) is not None
        has_F_opt = re.search(r"^-F\s+", cmd_result['stdout'], re.MULTILINE) is not None
        has_P_opt = re.search(r"^-P\s+", cmd_result['stdout'], re.MULTILINE) is not None
        has_k_opt = re.search(r"^-k\s+", cmd_result['stdout'], re.MULTILINE) is not None

        ruser = self._get_remote_user()
        wait_completion = False
        if (has_F_opt and has_g_opt and wait_reboot and
                self._connection.transport == 'ssh' and (not ruser or ruser == 'root')):
            wait_completion = True

        # Transfer the script to the target
        script_path = self._connection._shell.join_path(self._connection._shell.tmpdir, 'viosupg.sh')
        self._transfer_data(script_path, SCRIPT.replace('%tmpdir%', self._connection._shell.tmpdir))
        self._fixup_perms2((self._connection._shell.tmpdir, script_path))

        # Start background upgrade
        cmd = "/bin/sh %s" % script_path
        # We do not support filename without forcecopy
        if has_F_opt and has_g_opt and filename:
            cmd += " %s" % quote(filename)
        elif wait_completion:
            cmd += " -"
        else:
            cmd += " ''"
        cmd += " -i %s" % quote(image_file)
        cmd += " -a %s" % quote(':'.join(mksysb_install_disks))
        if cluster is None:
            # cluster not explicitly set, try to determine membership
            if self.cluster_membership():
                cmd += " -c"
        elif cluster:
            cmd += " -c"

        if has_F_opt:
            force_options = []
            if (has_g_opt and filename) or wait_completion:
                force_options += ['forcecopy']
            if skipclusterstate:
                force_options += ['skipclusterstate']
            if preserve_devname:
                force_options += ['devname']
            if skiprestore:
                force_options += ['skiprestore']
            if force_options:
                cmd += " -F %s" % ':'.join(force_options)

        if has_k_opt and pre_restore_script:
            cmd += " -k %s" % quote(pre_restore_script)
        if has_P_opt and post_install_binary:
            cmd += " -P %s" % quote(post_install_binary)

        cmd_result = self._low_level_execute_command(cmd)
        if cmd_result['rc'] != 0:
            result['stdout'] = cmd_result['stdout']
            result['stderr'] = cmd_result['stderr']
            result['msg'] = 'Command \'{0}\' failed with return code {1}.'.format(cmd, cmd_result['rc'])
            result['failed'] = True
            return result

        # Wait for the target to reboot and for the upgrade to complete
        self._display.vvv("{0}: waiting for upgrade to complete".format(self._task.action))
        max_end_time = datetime.utcnow() + timedelta(minutes=timeout)
        while datetime.utcnow() < max_end_time:
            try:
                cmd = "%s viosupgrade -l -q" % self.ioscli_cmd
                cmd_result = self._low_level_execute_command(cmd)
                if cmd_result['rc'] == 0:
                    match_key = re.search(r"^viosupgrade (.*)\r$", cmd_result['stdout'], re.MULTILINE)
                    if match_key:
                        state = match_key.group(1)
                        self._display.vvv("{0}: state is '{1}'".format(self._task.action, state))
                        if state == 'COMPLETED':
                            break
                        elif state == 'FAILED':
                            result['stdout'] = cmd_result['stdout']
                            result['stderr'] = cmd_result['stderr']
                            result['msg'] = 'viosupgrade failed'
                            result['failed'] = True
                            return result
                        elif 'in progress' in state and not wait_completion:
                            result['changed'] = True
                            result['msg'] = 'viosupgrade started successfully'
                            return result
                time.sleep(30)
            except Exception:
                time.sleep(30)
        else:  # Timeout
            result['msg'] = 'viosupgrade timed out'
            result['failed'] = True
            return result

        # Retrieve the ioslevel after the upgrade
        result['ioslevel']['after'] = self.get_ioslevel()

        # Return the old rootvg disks
        result['old_rootvg'] = self.get_vg_disks('old_rootvg')

        result['changed'] = True
        result['msg'] = 'viosupgrade completed successfully'
        return result
