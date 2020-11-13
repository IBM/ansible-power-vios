#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
author:
- AIX Development Team (@pbfinley1911)
module: mapping_facts
short_description: Returns the mapping between physical, logical, and virtual devices as facts
description:
- Returns information about the mapping between the virtual host adapters and the physical
  devices they are backed to.
version_added: '2.9'
requirements:
- VIOS >= 2.2.5.0
- Python >= 2.7
options:
  component:
    description:
    - Specifies the type of devices to retrieve information for.
    - C(vscsi) to list virtual SCSI devices.
    - C(npiv) to list NPIV devices.
    - C(net) to list shared Ethernet adapters.
    - C(all) to list all devices.
    type: str
    choices: [vscsi, net, npiv, all]
    default: all
  vadapter:
    description:
    - Specifies the device name of a server virtual adapter.
    - Mutually exclusive with I(physloc).
    type: str
  physloc:
    description:
    - Specifies the device physical location code of a server virtual adapter.
    - Mutually exclusive with I(vadapter).
    type: str
  types:
    description:
    - "Specifies the type of devices to display.
      The following types are supported:"
    - C(disk) to list physical backing devices.
    - C(lv) to list logical volume backing devices.
    - C(optical) to list optical backing devices.
    - C(tape) to list tape backed devices.
    - C(file) to list file backed devices.
    - C(file_disk) to list file backed disk devices.
    - C(file_opt) to list file backed optical devices.
    - C(cl_disk) to list clustered backing devices.
    - C(usb_disk) to list USB disks.
    type: list
    elements: str
'''

EXAMPLES = r'''
- name: Gather the mapping facts
  mapping_facts:
- name: Print the mapping facts
  debug:
    var: ansible_facts.mappings

- name: Populate the mapping facts with the mapping information for
        NPIV device vfchost0
  mapping_facts:
    component: npiv
    vadapter: vfchost0

- name: Populate the mapping facts with the mapping information for
        optical backing devices
  mapping_facts:
    types: optical
'''

RETURN = r'''
ansible_facts:
  description:
  - Facts to add to ansible_facts about the mapping between physical, logical, and virtual devices.
  returned: always
  type: complex
  contains:
    mappings:
      description:
      - Contains mappings for NPIV, VSCSI and SEA.
      returned: success
      type: dict
      elements: dict
      contains:
        npiv:
          description:
          - Maps virtual fibre channel adapter name to backing information.
          returned: always
          type: dict
          elements: dict
          contains:
            clntid:
              description:
              - Client logical partition ID.
              returned: always
              type: int
            clntname:
              description:
              - Client logical partition name.
              returned: when available
              type: str
            clntos:
              description:
              - The operating system on the client logical partition.
              returned: when available
              type: str
            fc:
              description:
              - Physical fibre channel adapter name.
              returned: always
              type: str
            fcphysloc:
              description:
              - The physical location of the fibre channel adapter.
              returned: always
              type: str
            flags:
              description:
              - Virtual fibre channel adapter flags.
              returned: always
              type: int
            physloc:
              description:
              - The physical location code of the server virtual fibre channel adapter.
              returned: always
              type: str
            ports:
              description:
              - Physical fibre channel port number.
              returned: always
              type: int
            status:
              description:
              - Virtual fibre channel adapter status.
              returned: always
              type: str
            vfcclient:
              description:
              - Client virtual fibre channel adapter name.
              returned: when available
              type: str
            vfcclientdrc:
              description:
              - Client virtual fibre channel adapter used for Dynamic Reconfiguration Connection (DRC).
              returned: when available
              type: str
          sample:
            "vfchost18": {
                "clntid": 19,
                "clntname": "lpar19",
                "clntos": "AIX",
                "fc": "fcs1",
                "fcphysloc": "U78CD.001.FZH1998-P1-C6-T2",
                "flags": 10,
                "physloc": "U8284.22A.21FD4BV-V1-C26",
                "ports": 3,
                "status": "LOGGED_IN",
                "vfcclient": "fcs0",
                "vfcclientdrc": "U8284.22A.21FD4BV-V19-C3"
            }
        net:
          description:
          - Maps virtual ethernet adapter name to backing information.
          returned: always
          type: dict
          elements: dict
          contains:
            backing:
              description:
              - Backing device.
              returned: always
              type: str
            bdphysloc:
              description:
              - The physical location code of the backing device.
              returned: when available
              type: str
            physloc:
              description:
              - The physical location code of the server virtual adapter.
              returned: always
              type: str
            sea:
              description:
              - Shared Ethernet adapter.
              returned: when available
              type: str
            status:
              description:
              - Shared Ethernet adapter status.
              returned: when available
              type: str
          sample:
            "net": {
                "ent4": {
                    "backing": "ent3",
                    "bdphysloc": "U78CB.001.WZS09RT-P1-C2-T4",
                    "physloc": "U8284.22A.21FD4BV-V1-C2-T1",
                    "sea": "ent5",
                    "status": "Available"
                }
            }
        vscsi:
          description:
          - Maps server virtual adapter name to backing information.
          returned: always
          type: dict
          elements: dict
          contains:
            clientid:
              description:
              - Client partition ID.
              returned: always
              type: str
            physloc:
              description:
              - The physical location code of the server's virtual adapter.
              returned: always
              type: str
            vtds:
              description:
              - Maps virtual target device name to backing information.
              returned: always
              type: dict
              elements: dict
              contains:
                backing:
                  description:
                  - Backing device.
                  returned: always
                  type: str
                bdphysloc:
                  description:
                  - The physical location code of the backing device.
                  returned: always
                  type: str
                lun:
                  description:
                  - Logical unit number.
                  returned: always
                  type: str
                mirrored:
                  description:
                  - The backing device is part of a Peer-to-Peer Remote Copy (PPRC) pair.
                  returned: when available
                  type: bool
                status:
                  description:
                  - Virtual target device status.
                  returned: always
                  type: str
          sample:
            "vhost0": {
                "clientid": "0x00000018",
                "physloc": "U8284.22A.21FD4BV-V1-C29",
                "vtds": {
                    "vtscsi0": {
                        "backing": "hdisk4",
                        "bdphysloc": "U78CD.001.FZH1998-P1-C6-T2-W500507680B215660-L0",
                        "lun": "0x8100000000000000",
                        "mirrored": false,
                        "status": "Available"
                    },
                    "vtscsi2": {
                        "backing": "hdisk5",
                        "bdphysloc": "U78CD.001.FZH1998-P1-C6-T2-W500507680B215660-L1000000000000",
                        "lun": "0x8200000000000000",
                        "mirrored": false,
                        "status": "Available"
                    }
                }
            }
'''

from ansible.module_utils.basic import AnsibleModule


ioscli_cmd = '/usr/ios/cli/ioscli'
delimiter = ','  # Delimiter to use for lsmap -fmt


def vscsi_mappings(module, mappings):
    """
    Retrieve VSCSI mappings.
    """
    cmd = [ioscli_cmd, 'lsmap']
    if module.params['vadapter']:
        cmd += ['-vadapter', module.params['vadapter']]
    elif module.params['physloc']:
        cmd += ['-plc', module.params['physloc']]
    else:
        cmd += ['-all']
    if module.params['types']:
        cmd += ['-type']
        cmd += module.params['types']
    cmd += ['-fmt', delimiter]
    ret, stdout, stderr = module.run_command(cmd)
    if ret != 0:
        if (ret == 15 and module.params['component'] != 'vscsi') or ret == 17:
            return
        module.fail_json(msg='lsmap failed rc=%d' % ret, stdout=stdout, stderr=stderr)

    # List of fields returned by lsmap:
    # svsa:physloc:clientid(:vtd:status:lun:backing:bdphysloc:mirrored)+
    mappings['vscsi'] = {}
    for line in stdout.splitlines():
        raw_fields = line.split(delimiter)
        if len(raw_fields) < 9:
            continue
        fields = [field.strip() for field in raw_fields]

        svsa = fields[0]
        mapping = {}
        mapping['physloc'] = fields[1]
        mapping['clientid'] = fields[2]
        mapping['vtds'] = {}
        for i in range(3, len(fields), 6):
            if not fields[i]:
                break
            vtd = {}
            vtd['status'] = fields[i + 1]
            vtd['lun'] = fields[i + 2]
            if fields[i + 3]:
                vtd['backing'] = fields[i + 3]
            if fields[i + 4]:
                vtd['bdphysloc'] = fields[i + 4]
            if fields[i + 5] != 'N/A':
                vtd['mirrored'] = fields[i + 5] != 'false'

            mapping['vtds'][fields[i]] = vtd
        mappings['vscsi'][svsa] = mapping


def npiv_mappings(module, mappings):
    """
    Retrieve NPIV mappings.
    """
    cmd = [ioscli_cmd, 'lsmap', '-npiv']
    if module.params['vadapter']:
        cmd += ['-vadapter', module.params['vadapter']]
    elif module.params['physloc']:
        cmd += ['-plc', module.params['physloc']]
    else:
        cmd += ['-all']
    cmd += ['-fmt', delimiter]
    ret, stdout, stderr = module.run_command(cmd)
    if ret != 0:
        if (ret == 63 and module.params['component'] != 'npiv') or ret == 17:
            return
        module.fail_json(msg='lsmap failed rc=%d' % ret, stdout=stdout, stderr=stderr)

    # List of fields returned by lsmap -npiv:
    # name:physloc:clntid:clntname:clntos:status:fc:fcphysloc:ports:flags:vfcclient:vfcclientdrc
    mappings['npiv'] = {}
    for line in stdout.splitlines():
        raw_fields = line.split(delimiter)
        if len(raw_fields) < 12:
            continue
        fields = [field.strip() for field in raw_fields]

        name = fields[0]
        mapping = {}
        mapping['physloc'] = fields[1]
        mapping['clntid'] = int(fields[2])
        if fields[3]:
            mapping['clntname'] = fields[3]
        if fields[4]:
            mapping['clntos'] = fields[4]
        mapping['status'] = fields[5]
        mapping['fc'] = fields[6]
        mapping['fcphysloc'] = fields[7]
        mapping['ports'] = int(fields[8])
        mapping['flags'] = int(fields[9], 16)
        if fields[10]:
            mapping['vfcclient'] = fields[10]
        if fields[11]:
            mapping['vfcclientdrc'] = fields[11]

        mappings['npiv'][name] = mapping


def net_mappings(module, mappings):
    """
    Retrieve SEA mappings.
    """
    cmd = [ioscli_cmd, 'lsmap', '-net']
    if module.params['vadapter']:
        cmd += ['-vadapter', module.params['vadapter']]
    elif module.params['physloc']:
        cmd += ['-plc', module.params['physloc']]
    else:
        cmd += ['-all']
    cmd += ['-fmt', delimiter]
    ret, stdout, stderr = module.run_command(cmd)
    if ret != 0:
        if (ret == 16 and module.params['component'] != 'net') or ret == 17:
            return
        module.fail_json(msg='lsmap failed rc=%d' % ret, stdout=stdout, stderr=stderr)

    # List of fields returned by lsmap -net:
    # svea:physloc:sea:backing:status:bdphysloc
    mappings['net'] = {}
    for line in stdout.splitlines():
        raw_fields = line.split(delimiter)
        if len(raw_fields) < 6:
            continue
        fields = [field.strip() for field in raw_fields]

        svea = fields[0]
        mapping = {}
        mapping['physloc'] = fields[1]
        if fields[2]:
            mapping['sea'] = fields[2]
        if fields[3]:
            mapping['backing'] = fields[3]
        if fields[4]:
            mapping['status'] = fields[4]
        if fields[5]:
            mapping['bdphysloc'] = fields[5]

        mappings['net'][svea] = mapping


def main():
    module = AnsibleModule(
        argument_spec=dict(
            component=dict(type='str', choices=['vscsi', 'net', 'npiv', 'all'], default='all'),
            vadapter=dict(type='str'),
            physloc=dict(type='str'),
            types=dict(type='list', elements='str')
        ),
        mutually_exclusive=[
            ['vadapter', 'physloc'],
        ],
        supports_check_mode=True
    )

    mappings = {}

    # Populate mappings
    component = module.params['component']
    if component == 'all' or component == 'vscsi':
        vscsi_mappings(module, mappings)
    if not module.params['types']:
        if component == 'all' or component == 'npiv':
            npiv_mappings(module, mappings)
        if component == 'all' or component == 'net':
            net_mappings(module, mappings)

    results = dict(ansible_facts=dict(mappings=mappings))

    module.exit_json(**results)


if __name__ == '__main__':
    main()
