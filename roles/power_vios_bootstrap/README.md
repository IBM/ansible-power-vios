# Ansible Role: power_vios_bootstrap
The [IBM Power Systems VIOS](../../README.md) collection provides an [Ansible role](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html), referred to as `power_vios_bootstrap`, which automatically loads and executes commands to install and update dnf and dependent softwares.In addition it installs python3 and dependencies as well.

For guides and reference, see the [Docs Site](https://ibm.github.io/ansible-power-vios/roles.html).

## Requirements

None.

## Role Variables

Available variables are listed below, along with if they are required, type and default values:

    pkgtype (True, str, none)

Specifies the package service requiring bootstrap installation.
pkgtype: [dnf]
Bootstrap for dnf is supported for VIOS 3.X.

-- pkgtype arguments
- dnf
Uses the AIX toolsbox to install dnf and dependencies on AIX 7.3 and above.

    opt_free_size (optional, str, 900)

Specifies the free space in megabytes needed in the /opt folder. It is used by dnf, wget and pycurl bootstraps.

    var_free_size (optional, str, 200)

Specifies the free space in megabytes needed in the /var folder.

    download_dir (optional, str, ~)

Specifies the temporary download location for install scripts and packages. The location resides on the Ansbile control node.

    target_dir (optional, str, /tmp/.ansible.cpdir)

Specifies the target location (per inventory host) for copying and restoring package files and metadata. If the target location does not exist, then a temporary filesystem is created using the target_dir as the mount point.  Upon role completion, the target location is removed.

## Dependencies

None.

## Example Playbook

    - hosts: vios
      gather_facts: no
      include_role:
        name: power_vios_bootstrap
      vars:
        pkgtype: dnf

## Copyright
© Copyright IBM Corporation 2021
