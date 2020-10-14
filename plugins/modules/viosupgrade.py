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
- Python >= 2.7
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
notes:
  - The level of the target mksysb image must be at version 3.1.0.00, or later.
  - Installations through this module are of the type New and Complete installation.
    Any customized configurations that might exist on the currently running system
    before the installation starts (including the timezone), are not included in the
    new installation image.
  - If the C(altinst_rootvg) or C(old_rootvg disks) are already available in the
    VIOS, you must rename them.
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
ioslevel:
    description: The installed maintenance level of the system before and after the upgrade
    returned: always
    type: dict
'''
