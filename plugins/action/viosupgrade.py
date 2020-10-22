#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import re
import time

from datetime import datetime, timedelta

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    TRANSFERS_FILES = True
    _VALID_ARGS = frozenset((
        'image_file',
        'mksysb_install_disks',
        'cluster',
        'filename',
        'timeout',
        'post_install_binary',
        'forcecopy',
        'skipclusterstate'
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

    def get_old_rootvg(self):
        """
        Return the list of hdisks that belong to old_rootvg.
        """
        cmd = "%s lspv -field NAME VG -fmt ," % self.ioscli_cmd
        cmd_result = self._low_level_execute_command(cmd)
        if cmd_result['rc'] != 0:
            return None

        hdisks = []
        for line in cmd_result['stdout'].splitlines():
            fields = line.split(',', 2)
            if len(fields) == 2 and fields[1] == "old_rootvg":
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
        forcecopy = self._task.args.get('forcecopy', False)
        if not isinstance(forcecopy, bool):
            forcecopy = boolean(self._templar.template(forcecopy), strict=False)
        skipclusterstate = self._task.args.get('skipclusterstate', False)
        if not isinstance(skipclusterstate, bool):
            skipclusterstate = boolean(self._templar.template(skipclusterstate), strict=False)

        filename = self._task.args.get('filename', None)
        timeout = int(self._task.args.get('timeout', 60))

        result['ioslevel'] = {}

        # Retrieve the ioslevel before the upgrade
        result['ioslevel']['before'] = self.get_ioslevel()

        # Start background upgrade
        cmd = "(nohup %s viosupgrade -l" % self.ioscli_cmd
        cmd += " -i %s" % image_file
        cmd += " -a %s" % ':'.join(mksysb_install_disks)
        if cluster is None:
            # cluster not explicitly set, try to determine membership
            if self.cluster_membership():
                cmd += " -c"
        elif cluster:
            cmd += " -c"

        force_options = []
        if forcecopy:
            force_options += ['forcecopy']
        if skipclusterstate:
            force_options += ['skipclusterstate']
        if force_options:
            cmd += " -F " + ':'.join(force_options)

        if post_install_binary:
            cmd += " -P %s" % post_install_binary
        if filename:
            cmd += " -g %s" % filename
        cmd += " &) && sleep 2"

        cmd_result = {}
        try:
            cmd_result = self._low_level_execute_command(cmd)
        except AnsibleConnectionFailure:
            self._display.vvv("{0}: connection closed".format(self._task.action))
            # Connection got closed because of system shutdown, ignore
            cmd_result['rc'] = 0
        result['stdout'] = cmd_result['stdout']
        result['stderr'] = cmd_result['stderr']
        if cmd_result['rc'] != 0:
            result['msg'] = 'Command \'{0}\' failed with return code {1}.'.format(cmd, cmd_result['rc'])
            result['failed'] = True
            return result

        # This code requires to copy the SSH keys to the new rootvg so that
        # the Ansible control node can connect after the upgrade.
        # This requires a version of viosupgrade that supports -P option and
        # -F forcecopy option.

        # Wait for system to reboot and for upgrade to complete
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
                time.sleep(30)
            except Exception:
                time.sleep(30)
                # As a workaround for now, exit when target is rebooted
                break
        else:  # Timeout
            result['msg'] = 'viosupgrade timed out'
            result['failed'] = True
            return result

        '''
        # Retrieve the ioslevel after the upgrade
        result['ioslevel']['after'] = self.get_ioslevel()

        # Return the old rootvg disks
        result['old_rootvg'] = self.get_old_rootvg()
        '''

        result['changed'] = True
        result['msg'] = 'viosupgrade completed successfully'

        return result
