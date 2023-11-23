#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
author:
- AIX Development Team (@pbfinley1911)
module: viosupgrade
short_description: Upgrades the Virtual I/O Server
description:
- Performs the operations of backing up the virtual and logical
  configuration data, installing the specified image, and restoring the
  virtual and logical configuration data of the Virtual I/O Server (VIOS).
version_added: '2.9'
requirements:
- VIOS >= 2.2.6.30
options:
  image_file:
    description:
    - Specifies the image file that must be used for the installation on
      an alternative disk.
    type: str
    required: true
  mksysb_install_disks:
    description:
    - Specifies the alternative disks to install the available VIOS image.
    - The current C(rootvg) disk on the VIOS partition is not impacted by
      this installation. The VIOS partition remains in the running state
      during the installation of the alternative disk.
    - The size of the target disks must be greater than or equal to 30G.
    - The disks that are specified must not be in use.
    type: list
    elements: str
    required: true
  filename:
    description:
    - Specifies the file that contains the list of files that need to be
      backed up from the current system and saved in the new VIOS installed
      image. Each line must contain a single filename along with its path.
      Multiple files must be specified in separate new lines.
    - The files are copied to the respective directories in the newly
      installed rootvg disks.
    type: str
  cluster:
    description:
    - Specifies that cluster-level backup and restore operations are performed.
      Mandatory for a VIOS that is part of an SSP cluster.
    - If not set, cluster membership is determined automatically.
    type: bool
  timeout:
    description:
    - Specifies the timeout (in minutes) to wait for the upgrade to complete.
    type: int
    default: 60
  post_install_binary:
    description:
    - Specifies a binary to execute after the restore process of the VIOS metadata
      configuration is successful.
    type: str
  pre_restore_script:
    description:
    - Specifies the script name that runs before the system configuration is restored.
    - You cannot use this with the I(skiprestore) as true.
    - If a nonzero value is returned from the pre_restore_script, the upgrade operation
    - exits with a failure message. You must resolve the issue and rerun the operation by
    - using -o rerun option.
    type: bool
    default: no
  skipclusterstate:
    description:
    - Skips the verification of the SSP cluster state, so that the installation
      can be triggered on multiple VIOS nodes simultaneously.
    - You must ensure that all the SSP cluster nodes are not in C(DOWN) state at
      the same time as this can bring down the SSP cluster completely.
    type: bool
    default: no
  preserve_devname:
    description:
    - Allows you to preserve the device names in the newvg volume group.
    - The following virtual host adapter devices are preserved:
    - vfchost adapter devices,
    - fcnvme, nvme devices
    - fscsi devices
    - iSCSI devices
    - network adapter devices.
    type: bool
    default: no
  skiprestore:
    description:
    - Skips the restore operation of the VIOS metadata configuration after
    - the operation of the viosupgrade installation process is completed and
    - the VIOS is booted from the newly installed rootvg disk.
    - You cannot use this with the I(pre_restore_script) as true.
    type: bool
    default: no
  wait_reboot:
    description:
    - Waits for the system to reboot and for the upgrade to complete.
    - Only usable when the remote user is root and the transport is ssh with
      public key authentication.
    - Copies SSH host identification and root user SSH authorized_keys file to
      the newly installed rootvg disks.
    type: bool
    default: yes
notes:
  - The level of the target mksysb image must be at version 3.1.0.00, or later.
  - Installations through this module are of the type New and Complete installation.
    Any customized configurations that might exist on the currently running system
    before the installation starts (including the timezone), are not included in the
    new installation image.
  - If the C(altinst_rootvg) or C(old_rootvg) disks are already available in the
    VIOS, you must rename them.
  - This module does not require Python to be installed on the target VIOS.
'''

EXAMPLES = r'''
- name: Perform the VIOS upgrade operation on new rootvg disks hdisk1 and hdisk2
  viosupgrade:
    image_file: mymksysbA
    mksysb_install_disks: [hdisk1,hdisk2]

- name: Upgrade the VIOS that belongs to an SSP cluster
  viosupgrade:
    image_file: mymksysbA
    mksysb_install_disks: [hdisk1,hdisk2]
    cluster: yes

- name: Copy files from the current rootvg disk to a newly installed VIOS image
  viosupgrade:
    image_file: mymksysbA
    mksysb_install_disks: [hdisk1,hdisk2]
    filename: file_list_name
'''

RETURN = r'''
msg:
    description: The execution message.
    returned: always
    type: str
stdout:
    description: The standard output
    returned: always
    type: str
stderr:
    description: The standard error
    returned: always
    type: str
old_rootvg:
    description: The list of disks that are part of the old_rootvg after the upgrade
    returned: always
    type: list
    sample: [hdisk0]
ioslevel:
    description: The installed maintenance level of the system before and after the upgrade
    returned: always
    type: dict
    contains:
      before:
        description:
        - The installed maintenance level of the system before the upgrade
        returned: always
        type: str
      after:
        description:
        - The installed maintenance level of the system after the upgrade
        returned: success
        type: str
    sample:
        "ioslevel": {
            "before": "3.1.0.00",
            "after": "3.1.1.00"
        }
'''
