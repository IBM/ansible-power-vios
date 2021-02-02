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
module: viosecure
short_description: Configures security hardening rules and firewall
description:
- Activates and deactivates security hardening rules.
- Configures and unconfigures the firewall settings of the network.
version_added: '2.9'
requirements:
- VIOS >= 2.2.5.0
- Python >= 2.7
options:
  level:
    description:
    - Specifies the security level settings to choose.
    - Specifying C(high) security level might cause stability or
      serviceability issues especially in a cluster environment.
    - Mutually exclusive with I(file).
    type: str
    choices: [ low, medium, high, default]
  rule:
    description:
    - Specifies the name of the rule to be applied.
    type: str
  file:
    description:
    - Specifies the security rules file to be applied.
    - Mutually exclusive with I(level).
    type: str
  firewall:
    description:
    - Specifies the firewall state and rules.
    type: dict
    suboptions:
      ipv4:
        description:
        - Specifies the IPv4 firewall state and rules.
        type: dict
        suboptions: &ipcommon
          active:
            description:
            - Specifies the state of the firewall.
            type: bool
          default:
            description:
            - Load default firewall rules.
            - Mutually exclusive with I(rules).
            type: bool
          rules:
            description:
            - Specifies the list of firewall rules.
            type: list
            elements: dict
            suboptions:
              present:
                description:
                - Specifies whether the rule should be present or not.
                type: bool
                default: yes
              port:
                description:
                - Specifies the port number or a service name from the
                  C(/etc/services) file.
                - All the IP activity to and from that local port is allowed.
                type: str
                required: true
              interface:
                description:
                - Specifies the network interface name, like C(en0).
                type: str
              remote:
                description:
                - Specifies that the port is a remote port.
                - All the IP activity to and from that remote port is allowed.
                type: bool
                default: no
              address:
                description:
                - IP address.
                type: str
              timeout:
                description:
                - Timeout period.
                - The timeout period can be specified as a number (in seconds),
                  or with a number followed by C(m) (minutes), C(h) (hours), or C(d) (days).
                  The maximum timeout period is 30 days.
                type: str
      ipv6:
        description:
        - Specifies the IPv6 firewall state and rules.
        type: dict
        suboptions: *ipcommon
notes:
  - Applying a C(high) security profile might cause stability or
    serviceability issues especially if the VIOS is part of a cluster environment.
'''

EXAMPLES = r'''
- name: Apply all of the low system security settings to the system
  viosecure:
    level: low

- name: Apply security rules from file myfile
  viosecure:
    file: myfile

- name: Apply the single rule lls_maxage
  viosecure:
    level: low
    rule: lls_maxage

- name: Allow the users from IP address 10.10.10.10 to rlogin
  viosecure:
    firewall:
      ipv4:
        active: yes
        rules:
        - present: yes
          port: "login"
          address: "10.10.10.10"

- name: Allow users to rlogin for seven days
  viosecure:
    firewall:
      ipv4:
        active: yes
        rules:
        - present: yes
          port: "login"
          timeout: "7d"

- name: Allow rsh client activity through interface en0
  viosecure:
    firewall:
      ipv4:
        active: yes
        rules:
        - present: yes
          port: 514
          remote: yes
          interface: "en0"

- name: Load default firewall rules
  viosecure:
    firewall:
      ipv4:
        active: yes
        default: yes
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
firewall:
    description: The current firewall settings
    returned: always
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule


ioscli_cmd = '/usr/ios/cli/ioscli'


def security_apply(module, params):
    global results

    cmd = [ioscli_cmd, 'viosecure']
    if params['level']:
        cmd += ['-level', params['level'], '-apply']
        if params['rule']:
            cmd += ['-rule', params['rule']]
    else:
        cmd += ['-file', params['file']]

    ret, stdout, stderr = module.run_command(cmd)
    if ret != 0:
        results['stdout'] = stdout
        results['stderr'] = stderr
        results['msg'] = 'Could not apply security rules, return code {0}.'.format(ret)
        module.fail_json(**results)


def firewall_view(module):
    """
    Returns a dictionary with current firewall settings.

    $ viosecure -firewall view -fmt ,
    ON
    all,5989,any,wbem-https,0.0.0.0,0
    all,5988,any,wbem-http,0.0.0.0,0
    all,5987,any,wbem-rmi,0.0.0.0,0
    all,any,657,rmc,0.0.0.0,0
    all,657,any,rmc,0.0.0.0,0
    all,443,any,https,0.0.0.0,0
    all,any,427,svrloc,0.0.0.0,0
    all,427,any,svrloc,0.0.0.0,0
    all,80,any,http,0.0.0.0,0
    all,any,53,domain,0.0.0.0,0
    all,22,any,ssh,0.0.0.0,0
    all,21,any,ftp,0.0.0.0,0
    all,20,any,ftp-data,0.0.0.0,0
    """
    global results

    # Do not use ':' as seperator because it causes problems with IPv6 addresses
    sep = ','

    firewall = {}

    for ip in ['ipv4', 'ipv6']:
        firewall[ip] = {}
        cmd = [ioscli_cmd, 'viosecure', '-firewall', 'view', '-fmt', sep]
        if ip == 'ipv6':
            cmd += ['-ip6']
        ret, stdout, stderr = module.run_command(cmd)
        if ret != 0:
            results['stdout'] = stdout
            results['stderr'] = stderr
            results['msg'] = 'Could not retrieve {0} rules, return code {1}'.format(ip, ret)
            module.fail_json(**results)
        # First line indicates state ON or OFF
        lines = stdout.split('\n')
        status = lines.pop(0)
        if status == 'ON':
            firewall[ip]['active'] = True
        rules = []
        for line in lines:
            fields = line.split(sep, 6)
            if len(fields) != 6:
                continue
            rule = {}
            if fields[0] != 'all':
                rule['interface'] = fields[0]
            if fields[1] != 'any':
                rule['port'] = int(fields[1])
            else:
                rule['port'] = int(fields[2])
                rule['remote'] = True
            if (ip == 'ipv6' and fields[4] != '::') or (ip == 'ipv4' and fields[4] != '0.0.0.0'):
                rule['address'] = fields[4]
            if fields[5] != '0':
                rule['timeout'] = fields[5]
            rules += [rule]
        firewall[ip]['rules'] = rules

    return firewall


def firewall_apply(module, params):
    """
    Apply the specified firewall settings.
    """
    global results

    firewall = params['firewall']

    for ip in firewall:
        if ip != 'ipv4' and ip != 'ipv6':
            continue
        if firewall[ip] is None:
            continue
        if 'rules' in firewall[ip] and firewall[ip]['rules']:
            for rule in firewall[ip]['rules']:
                if 'port' not in rule:
                    continue

                cmd = [ioscli_cmd, 'viosecure', '-firewall']
                if rule['present']:
                    cmd += ['allow']
                else:
                    cmd += ['deny']

                # port can be an int or a string specifying a service from /etc/services
                cmd += ['-port', str(rule['port'])]
                if 'interface' in rule and rule['interface']:
                    cmd += ['-interface', rule['interface']]
                if 'address' in rule and rule['address']:
                    cmd += ['-address', rule['address']]
                if rule['timeout'] is not None:
                    cmd += ['-timeout', rule['timeout']]
                if 'remote' in rule and rule['remote']:
                    cmd += ['-remote']
                if ip == 'ipv6':
                    cmd += ['-ip6']

                # To maintain idempotency, we do not want to fail in the
                # deny case (present=no) if the rule does not exist.
                if not rule['present']:
                    cmd += ['-quiet']

                ret, stdout, stderr = module.run_command(cmd)
                if ret != 0:
                    results['stdout'] = stdout
                    results['stderr'] = stderr
                    results['msg'] = 'Could not apply rule, return code {0}.'.format(ret)
                    module.fail_json(**results)

        # Check if firewall needs to be activated/deactivated
        cmd = [ioscli_cmd, 'viosecure', '-firewall']
        if 'active' in firewall[ip] and firewall[ip]['active']:
            cmd += ['on']
            if 'default' in firewall[ip] and firewall[ip]['default']:
                cmd += ['-reload', '-force']
        else:
            cmd += ['off']
        if ip == 'ipv6':
            cmd += ['-ip6']
        ret, stdout, stderr = module.run_command(cmd)
        if ret != 0:
            results['stdout'] = stdout
            results['stderr'] = stderr
            results['msg'] = 'Could not change firewall state, return code {0}.'.format(ret)
            module.fail_json(**results)


def main():
    global results

    ipcommon = dict(
        type='dict',
        options=dict(
            active=dict(type='bool'),
            default=dict(type='bool'),
            rules=dict(
                type='list', elements='dict',
                options=dict(
                    present=dict(type='bool', default=True),
                    port=dict(required=True, type='str'),
                    remote=dict(type='bool', default=False),
                    address=dict(type='str'),
                    timeout=dict(type='str'),
                    interface=dict(type='str'),
                )
            )
        )
    )

    module = AnsibleModule(
        argument_spec=dict(
            level=dict(type='str', choices=['low', 'medium', 'high', 'default']),
            rule=dict(type='str'),
            file=dict(type='str'),
            firewall=dict(
                type='dict',
                options=dict(
                    ipv4=ipcommon,
                    ipv6=ipcommon
                )
            ),
        ),
        mutually_exclusive=[
            ['level', 'file']
        ],
        required_one_of=[
            ['level', 'file', 'firewall']
        ]
    )

    results = dict(
        changed=False,
        msg='',
        stdout='',
        stderr='',
    )

    if module.params['level'] or module.params['file']:
        security_apply(module, module.params)
    if module.params['firewall']:
        firewall_apply(module, module.params)

    results['firewall'] = firewall_view(module)

    results['changed'] = True
    results['msg'] = 'viosecure completed successfully'
    module.exit_json(**results)


if __name__ == '__main__':
    main()
