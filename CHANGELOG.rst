.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

Releases
========

Version 1.3.0
---------------
Notes
  * New module: fix_download to download fixes from EFD portal.
  * 5 New playbooks: viosbr, updateios, viosupgrade, fix_download, end-to-end update.
  * Enhancement to support remove_outdated_filesets action in updateios module.
  * Enhancement to support view action in viosbr module.
  * Support for -k -F devname in viosupgrade module.
  * Updated dnf bootstrap to address the changes in Toolbox.
  * Enhancement in dnf bootstrap to install dnf on all VIOS version.
  * YUM is no more supported.

Availability
  * `Automation Hub v1.3.0`_
  * `Galaxy v1.3.0`_
  * `GitHub v1.3.0`_

.. _Automation Hub v1.3.0:
   https://cloud.redhat.com/ansible/automation-hub/ibm/power_vios

.. _Galaxy v1.3.0:
   https://galaxy.ansible.com/download/ibm-power_vios-1.3.0.tar.gz

.. _GitHub v1.3.0:
   https://github.com/IBM/ansible-power-vios/releases/download/v1.3.0/ibm-power_vios-1.3.0.tar.gz

Version 1.2.3
-------------
Notes
  * Fix pylint issue and import error

Availability
  * `Automation Hub v1.2.2`_
  * `Galaxy v1.2.2`_
  * `GitHub v1.2.2`_

.. _Automation Hub v1.2.2:
   https://cloud.redhat.com/ansible/automation-hub/ibm/power_vios

.. _Galaxy v1.2.2:
   https://galaxy.ansible.com/download/ibm-power_vios-1.2.2.tar.gz

.. _GitHub v1.2.2:
   https://github.com/IBM/ansible-power-vios/releases/download/v1.2.2/ibm-power_vios-1.2.2.tar.gz

Version 1.2.2
-------------
Notes
  * Fix broken dnf bootstrap playbook and include dnf bootstrap role

Availability
  * `Automation Hub v1.2.2`_
  * `Galaxy v1.2.2`_
  * `GitHub v1.2.2`_

.. _Automation Hub v1.2.2:
   https://cloud.redhat.com/ansible/automation-hub/ibm/power_vios

.. _Galaxy v1.2.2:
   https://galaxy.ansible.com/download/ibm-power_vios-1.2.2.tar.gz

.. _GitHub v1.2.2:
   https://github.com/IBM/ansible-power-vios/releases/download/v1.2.2/ibm-power_vios-1.2.2.tar.gz

Version 1.2.0
--------------
Notes
  * mapping_facts: reports VIOS mappings (lsmap command) as Ansible facts
  * updateios: fix automated answer to updateios command (issue #6 )
  * viosupgrade: option for wait upon reboot
  * viosupgrade: documenting ssh pubkey support and use of ansible tmpdir

Availability
  * `Automation Hub v1.2.0`_
  * `Galaxy v1.2.0`_
  * `GitHub v1.2.0`_

.. _Automation Hub v1.2.0:
   https://cloud.redhat.com/ansible/automation-hub/ibm/power_vios

.. _Galaxy v1.2.0:
   https://galaxy.ansible.com/download/ibm-power_vios-1.2.0.tar.gz

.. _GitHub v1.2.0:
   https://github.com/IBM/ansible-power-vios/releases/download/v1.2.0/ibm-power_vios-1.2.0.tar.gz

Version 1.1.2
--------------
Notes
  * mapping_facts: reports VIOS mappings (lsmap command) as Ansible facts

Availability
  * `Automation Hub v1.1.2`_
  * `Galaxy v1.1.2`_
  * `GitHub v1.1.2`_

.. _Automation Hub v1.1.2:
   https://cloud.redhat.com/ansible/automation-hub/ibm/power_vios

.. _Galaxy v1.1.2:
   https://galaxy.ansible.com/download/ibm-power_vios-1.1.2.tar.gz

.. _GitHub v1.1.2:
   https://github.com/IBM/ansible-power-vios/releases/download/v1.1.2/ibm-power_vios-1.1.2.tar.gz

Version 1.1.1
--------------
Notes
  * Includes viosupgrade plugin (async actions)

Availability
  * `Automation Hub v1.1.1`_
  * `Galaxy v1.1.1`_
  * `GitHub v1.1.1`_

.. _Automation Hub v1.1.1:
   https://cloud.redhat.com/ansible/automation-hub/ibm/power_vios

.. _Galaxy v1.1.1:
   https://galaxy.ansible.com/download/ibm-power_vios-1.1.1.tar.gz

.. _GitHub v1.1.1:
   https://github.com/IBM/ansible-power-vios/releases/download/v1.1.0/ibm-power_vios-1.1.1.tar.gz

Version 1.1.0
------------------
Notes
  * Collection content for community upstream of Ansible Content for IBM Power Systems.

Availability
  * `Automation Hub v1.1.0`_
  * `Galaxy v1.1.0`_
  * `GitHub v1.1.0`_

.. _Automation Hub v1.1.0:
   https://cloud.redhat.com/ansible/automation-hub/ibm/power_vios

.. _Galaxy v1.1.0:
   https://galaxy.ansible.com/download/ibm-power_vios-1.1.0.tar.gz

.. _GitHub v1.1.0:
   https://github.com/IBM/ansible-power-vios/releases/download/v1.1.0/ibm-power_vios-1.1.0.tar.gz

Version 1.0.2-beta
------------------
Notes
  * Initial beta release of IBM Power Systems VIOS collection, referred to as power_vios

Availability
  * `Galaxy v1.0.2-beta`_
  * `GitHub v1.0.2-beta`_

.. _Galaxy v1.0.2-beta:
   https://galaxy.ansible.com/download/ibm-power_vios-1.0.2-beta.tar.gz

.. _GitHub v1.0.2-beta:
   https://github.com/IBM/ansible-power-vios/releases/download/v1.0.2/ibm-power_vios-1.0.2-beta.tar.gz

Version 1.2.2
-------------
Notes
  * Fix broken bootstrap playbook, include new role for dnf bootstrap playbook
  * which installs and updates dnf and python3 along with other dependencies

Availability
  * `Galaxy v1.2.2
  * `GitHub v1.2.2

.. _Galaxy v1.2.2:
   https://galaxy.ansible.com/download/ibm-power_vios-1.2.2.tar.gz

.. _GitHub v1.2.2
   https://github.com/IBM/ansible-power-vios/releases/download/v1.2.2/ibm-power_vios-1.2.2.tar.gz

