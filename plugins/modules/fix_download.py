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
- Shreyansh Chamola (@schamola)
module: fix_download
short_description: Download fixes for VIOS from EFD.
description:
- Electronic Fix Distribution (EFD) provides a cloud API, using which, users can download TL and SP fixes for different POWER subsystems.
- This module uses curl to send JSON payloads to EFD(Electronic Fix Distribution) so as to get the list of fixes available for that particular machine
  or download a particular fix for the machine.
version_added: '1.7.0'
requirements:
- VIOS >= 2.2.5.0
- Python >= 3.0.0
- Curl should be present.
options:
  action:
    description:
    - Specifies the action that the module needs to perform.
    - C(list) Lists the fixes that are available for user's machine.
    - C(download) Downloads a specific fix for machine.
    type: str
    choices: [ list, download ]
    required: True
  fix_id:
    description:
    - Specifies the file that the user wants to be downloaded.
    type: str
  directory:
    description:
    - Specifies the directory where the user wants the file to be downloaded.
    type: str
    default: '/'
  clean_directory:
    description:
    - Specifies if the directory should be emptied or not.
    type: bool
    default: 'False'
notes:
    - An empty directory is required for downloading the fixes. If directory is not clean, provide consent by using
    - I(clean_directory) as True. This module will clean the directory otherwise will fail with the message
    - "Non empty directory has been provided. Either provide an empty directory or set clean_directory to True."
    - Downloading ISO images are not supported through EFD portal, user needs to manually download from ESS.
'''

EXAMPLES = r'''
  - name: List fixes for the system
    fix_download:
      action: "list"
    register: result
  - debug: var=result.List_of_Fixes

  - name: Download a fix/file
    fix_download:
      action: "download"
      fix_id: "{{ name_fs }}"
      directory: "{{ dir }}"
'''

RETURN = r'''
msg:
    description: The execution message.
    returned: always.
    type: str
    sample: 'The fix has been downloaded. Response confirmed. The payload file was deleted.'
rc:
    description: The return code.
    returned: always.
    type: int
stdout:
    description: The standard output.
    returned: always.
    type: str
stderr:
    description: The standard error.
    returned: always.
    type: str
cmd:
    description: Command executed.
    returned: always.
    type: str
List_of_Fixes:
    description: Dictionary output of available fixes for the system.
    returned: If I(action=list).
    type: dict
    sample:
        "List_of_Fixes": [
            {
                "applies_to_version": "3.1.4.21",
                "description": "VIOS 3.1.4.21 Fix Pack",
                "id": "VIOS_FP_3.1.4.21",
                "name": "Fix Pack: VIOS 3.1.4.21",
                "release_date": "2023-04-28T00:00:00.000Z",
                "status": "available",
                "type": "group_FP",
                "upgrades_to_version": "3.1.4.21"
            },
            {
                "applies_to_version": "3.1.4.10",
                "description": "VIOS 3.1.4.10 Fix Pack",
                "id": "VIOS_FP_3.1.4.10",
                "name": "Fix Pack: VIOS 3.1.4.10",
                "release_date": "2022-12-02T00:00:00.000Z",
                "status": "available",
                "type": "group_FP",
                "upgrades_to_version": "3.1.4.10"
            }
        ]
updates:
    description: Updates recieved from EFD portal after sending the payload.
    returned: Never
    type: JSON
    sample:
        "updates": [
                 {
                    "id":"VIOS_FP_3.1.4.21",
                    "status":"available",
                    "description":"VIOS 3.1.4.21 Fix Pack",
                    "release_date":"2023-04-28T00:00:00.000Z",
                    "name":"Fix Pack: VIOS 3.1.4.21",
                    "applies_to_version":"3.1.4.21",
                    "upgrades_to_version":"3.1.4.21",
                    "type":"group_FP",
                    "files":[
                       {
                          "descriptor":"application/self-extracting",
                          "description":"VIOS installp image (bff)",
                          "size":512,
                          "hash":"+V7C1AJAU9sdg7qY/Kc4R8aGgd/YCLi9DMxxImLuYEs=",
                          "hashAlgorithm":"SHA-256",
                          "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04/sar/CMA/VIA/0bclt/3/VIOS_FP_3.1.4.21.bff",
                          "url_type":"edge"
                       },
                       {
                          "descriptor":"metadata/deployment-descriptor.fix",
                          "description":"DeploymentDescriptor",
                          "size":51626,
                          "hash":"Csm/6CLSkoQxEbu9pjc6OGMA3YJBxb0uuT0ewgOLqv0=",
                          "hashAlgorithm":"SHA-256",
                          "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04/sar/CMA/VIA/0bclt/3/VIOS_FP_3.1.4.21.dd.xml",
                          "url_type":"edge"
                       },
                       {
                          "descriptor":"metadata/package-descriptor.fix",
                          "description":"PackageDescriptor",
                          "size":187283,
                          "hash":"4FT5XB13Yjaf4Y4MIDBySwd+2Lng9M0qEEf7405PsH4=",
                          "hashAlgorithm":"SHA-256",
                          "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04/sar/CMA/VIA/0bclt/3/VIOS_FP_3.1.4.21.pd.sdd",
                          "url_type":"edge"
                       },
                       {
                          "descriptor":"application/self-extracting",
                          "description":"cksum verifier",
                          "size":3584,
                          "hash":"yWJIxRMXh+CEUc6S+X6m1LZQQC39S98k7kyHtqMzuS0=",
                          "hashAlgorithm":"SHA-256",
                          "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04/sar/CMA/VIA/0bclt/3/ck_sum.bff",
                          "url_type":"edge"
                       }
                    ]
                 }
              ]
'''

import json
import time
import datetime
import urllib.request

from ansible.module_utils.basic import AnsibleModule

event_id = ""
size_of_file = 0
softwareupdate_event_id = ""
getresponse_event_id = ""
confirmresopnse_event_id = ""
asset = ""
sr_no = ""
payload = {}
results = dict(
    changed=False,
    cmd='',
    msg='',
    stdout='',
    stderr='',
    List_of_Fixes='',
)

####################################################################################
# Helper Functions
####################################################################################


def check_empty_directory(module):
    '''
    Utility function to check if the provided directory is empty or not.

    arguments:
        module(dict) - The Ansible module.

    returns:
        Fails if the directory is not empty and user has not provided consent to empty it.
    '''

    loc = module.params['directory']

    if not check_existence(module, loc):
        results['msg'] = "The provided directory does not exist."
        module.fail_json(**results)

    cmd = "ls " + loc + " | wc -l"

    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "Failed to check if the directory is empty"
        module.fail_json(**results)

    if str(results['stdout']) != "0":
        if not module.params['clean_directory']:
            results['msg'] = "Non empty directory has been provided. Either provide an empty directory or set clean_directory to True."
            module.fail_json(**results)
        empty_directory(module)


def check_space(module, required_space):
    '''
    Utility function to check if the provided directory has required space or not.

    arguments:
        module (dict) - The Ansible module.
        required_space (int) - Space required in the provided directory.

    returns:
        True - If space is enough.
        False - If space is not enough.
    '''

    cmd = "df -m "
    cmd += module.params['directory']

    rc, stdout, stderr = module.run_command(cmd)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "The following command failed: " + cmd
        module.fail_json(**results)

    values = stdout.split("\n")[1]
    details = values.split()
    space = float(details[2])
    required_space = float(required_space)

    if space < required_space:
        results['msg'] = "Not enough space present in the provided directory. " + str(round(required_space - space, 1)) + "MB more needed."
        module.fail_json(**results)


def check_requirements(module):
    '''
    Utility Function to check if the requirements are already satisfied or not.

    arguments:
        module (dict) : The Ansible module.

    returns:
        Nothing
    '''

    cmd = "ls /opt/freeware/bin/"

    check_curl = cmd + 'curl'

    rc, stdout, stderr = module.run_command(check_curl)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "Curl is not present in the system, please install and rerun."
        module.fail_json(**results)

    results['msg'] = "Curl is present on the system, requirement satisfied!"


def empty_directory(module):
    '''
    Utility function to empty the directory if it is not empty and the user has provided permission to empty it.

    arguments:
        module (dict) : The Ansible module

    returns:
        Nothing
    '''

    loc = module.params['directory']

    cmd = "rm -rf " + loc

    rc, stdout, stderr = module.run_command(cmd)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "Following command failed: " + cmd
        module.fail_json(**results)

    cmd = "mkdir " + loc

    rc, stdout, stderr = module.run_command(cmd)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "Following command failed: " + cmd
        module.fail_json(**results)

    results['msg'] += " The provided directory was emptied."


def get_oslevel(module):
    '''
    Function to get the os level from the machine

    arguments:
        module (dict) : The Ansible module

    returns:
        oslevel (str) : Containing the current oslevel of the machine.
    '''

    cmd = "/usr/ios/cli/ioscli ioslevel"

    rc, stdout, stderr = module.run_command(cmd)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results["msg"] = "Failed to determine the oslevel of the machine."
        module.fail_json()

    oslevel = stdout.strip()

    if oslevel[-2:] == "00":
        oslevel = oslevel[:-1]

    return oslevel


def get_info(module):
    '''
    Function to get the values for asset and asset_id

    arguments:
        module (dict) : The Ansible module

    returns:
        Nothing
    '''

    global asset
    global asset_id

    cmd_for_asset = "uname -M"

    rc, stdout, stderr = module.run_command(cmd_for_asset)

    results['cmd'] = cmd_for_asset
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "The following command failed: " + cmd_for_asset
        module.fail_json()

    # asset will be something like this: XXXX-YYY

    asset = stdout.split(",")[1].strip()

    cmd_for_assetid = "uname -m"

    rc, stdout, stderr = module.run_command(cmd_for_assetid)

    results['cmd'] = cmd_for_assetid
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "The following command failed: " + cmd_for_assetid
        module.fail_json()

    # asset_id will be something like this: XXXXXXXXXXXX

    asset_id = stdout.strip()


def get_serial_no(module):
    '''
    Function to get the serial number of the machine.

    arguments:
        module (dict) : The Ansible module

    returns:
        Nothing
    '''

    global sr_no

    cmd = '/usr/sbin/lscfg -vpl sysplanar0'

    rc, stdout, stderr = module.run_command(cmd)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "The following command failed: " + cmd
        module.fail_json()

    sr_no = parse_sr_no(stdout)
    stdout = "Retrieved serial number: " + sr_no

    results[stdout] = sr_no


def parse_sr_no(stdout):
    '''
    Utility function to parse the output of lscfg command, so as to retrieve the serial number.

    arguments:
        stdout (str) : Standard output of lscfg command.

    returns:
        serial (str) : serial number of the machine.
    '''

    stdout = stdout.split("\n\n")
    system_vpd = ""

    for segment in stdout:
        if "System VPD" in segment:
            system_vpd = segment
            break

    system_vpd = system_vpd.split("\n      ")

    serial = ""

    for line in system_vpd:
        if "Machine/Cabinet Serial No" in line:
            serial = line
            break

    serial = serial.split(".")[-1]
    return serial


def check_for_updates(stdout):
    '''
    Utility function to check if updates are available in the reponse field.

    arguments:
        stdout (str) : Contains standard output of the curl command

    returns:
        True: If updates are available
        False: If updates are not available
    '''

    res = json.loads(stdout)

    try:
        if res["response_state"]["transactions"][softwareupdate_event_id]["response_object"]["updates"]:
            return 1
        return 0
    except KeyError:
        return 0


def check_response(stdout):
    '''
    Utility function to check if the connection was made or not.

    arguments:
        stdout (str) : Contains standard output of the curl command

    returns:
        True : If the response was 200 (OK)
        False : In all the other cases (Except 200 OK response)
    '''

    res = json.loads(stdout)

    try:
        if res["transaction"]["rc"] == 200:
            return 1
        return 0
    except KeyError:
        return 0


def check_for_authentication(module, stdout):
    '''
    Utility function to check if there was any authentication related faliure.

    arguments:
        stdout (str) : Contains standard output of the command

    returns:
        True: If no authentication faliure was faced.
        False: If there was any type of authentication faliure.
    '''

    res = json.loads(stdout)

    try:
        res = res["response_state"]["transactions"][softwareupdate_event_id]["response_object"]["updates"][0]["error"]
        results['msg'] = "Following error was encountered: " + res
        return 0
    except KeyError:
        return 1


def check_existence(module, filename):
    '''
    Utility function to check if the file exists or not.

    arguments:
        module (dict) - The Ansible module.
        filename (str) - The URL where file is located.

    returns:
        True - If the file exists.
        False - If the file does not exist.
    '''

    cmd = "ls " + filename

    rc, stdout, stderr = module.run_command(cmd)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "Location: " + filename + " could not be found."
        return 0
    return 1


def dictionary_to_json(dict_val, payload_type):
    '''
    Utility Function to convert the user provided data from dictionary
    format to JSON format, which will further be used to send requests.

    arguments:
        module (dict): the Ansible module.

    returns:
        json_object (JSON) : JSON object containing all the attributes in JSON format.
    '''

    out_file = open("payloadfile.json", "w")

    temp_out = open(payload_type, "w")

    json.dump(dict_val, out_file, indent=4)

    json.dump(dict_val, temp_out, indent=4)

    out_file.close()
    temp_out.close()


def remove_json_file(module):
    '''
    Helper function to remove the payload file from the system. The payload is being sent as a file,
    this function wil be removing that file.

    arguments:
        module (dict) : The Ansible module.

    returns:
        Nothing
    '''

    cmd = "rm /payloadfile.json"

    rc, stdout, stderr = module.run_command(cmd)

    results['stdout'] = stdout
    results['stderr'] = stderr

    if rc != 0:
        results['rc'] = rc
        results['msg'] += " The payload file 'payloadfile.json' could not be removed."
        module.fail_json(**results)

    results['msg'] += " The payload file was deleted."


def wait_for_response(module):
    '''
    Utility function to keep sending the request until the required response is received.

    arguments:
        module (dict) : The Ansible module.
        cmd (str) : CURL command to send the payload.

    returns:
        Nothing
    '''

    counter = 0

    while counter <= 11:
        time.sleep(10)
        rc, stdout, stderr = module.run_command(curl_cmd)
        if check_for_updates(stdout):
            break
        counter += 1

    results['cmd'] = curl_cmd
    results['rc'] = rc
    results['stderr'] = stderr
    results['stdout'] = stdout

    if counter > 11 and not check_for_updates(stdout):
        results['msg'] = "Could not find any fixes for the machine. Request timed out."
        module.fail_json(**results)
    else:
        if not check_for_authentication(module, stdout):
            module.fail_json(**results)
        results['msg'] = "Response received."


def get_URL(module):
    '''
    Function to retreive the URL from the JSON response

    arguments:
        module (dict) - The Ansible module

    returns:
        URL (str) - URL from where the fix can be downloaded.
    '''

    global size_of_file
    size_of_file = 0

    generate_payload(module, "download")

    wait_for_response(module)

    res = json.loads(results['stdout'])

    fields = res["response_state"]["transactions"][softwareupdate_event_id]["response_object"]["updates"]

    results['List_of_Fixes'] = fields

    URL = []

    for fix_group in fields:
        for keys in fix_group["files"]:
            URL.append(keys["url"])
            size_of_file += keys['size']

    if URL != []:
        return URL
    else:
        results['msg'] = "Could not retrieve the URLs."
        module.fail_json(**results)


def generate_event_details():
    '''
    Utility function to generate get event_time and event_time_ms

    arguments: None

    returns:
        Nothing
    '''

    global event_time
    global event_time_ms

    event_time_ms = round(time.time() * 1000)
    event_time = str(datetime.datetime.now()).split('.', maxsplit=1)[0]


def generate_event_id():
    '''
    Utility function to generate the event id.

    arguments:
        module (dict) : The Ansible module.

    returns:
        event_id (str) - Contains event_id that will be sent in the JSON payload.
    '''

    global event_id

    event_id = "IBM_VIOS"

    event_id += "_" + asset
    event_id += "_" + asset_id
    event_id += "_" + str(event_time_ms)

    # event_id will be something like: IBM_VIOS_XXXX-XXX_XXXXXXXXXXXX_1687344006365


def generate_event_header(payload_type):
    '''
    Utility funtion for generating header of the event.

    arguments:
        payload_type (str) - Signifies the type of event (software_update, geturl, download or confirm_response)

    returns:
        event_header (dict) - Dictionary containing all the required details that need to go inside the event header.
    '''

    global softwareupdate_event_id
    global getresponse_event_id
    global confirmresopnse_event_id

    event_header = {}
    if payload_type == "post" or payload_type == "downloadpost":
        event_header["event_type"] = "software_update"

    elif payload_type == "geturl" or payload_type == "download":
        event_header["event_type"] = "last_contact"

    else:
        event_header["event_type"] = "confirm_response"

    event_header["event_id"] = event_header["event_type"] + "_" + event_id

    if payload_type == "post" or payload_type == "downloadpost":
        softwareupdate_event_id = event_header["event_id"]
    elif payload_type == "geturl":
        getresponse_event_id = event_header["event_id"]
    else:
        confirmresopnse_event_id = event_header["event_id"]

    event_header["event_time"] = event_time
    event_header["event_time_ms"] = event_time_ms

    return event_header


def generate_post_body():
    '''
    Utility function that generates the body for the event part of the payload for POST method.

    arguments: None

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of the
                            payload for POST method.
    '''

    credentials = {}
    mtsn_info = {}

    event_body = {
        "action": "order_vios_software",
        "operation": "order_software",
        "request_type": "preview_all_fixes",
        "component": "system",
        "efd_product": "ibm/vios",
    }

    event_body["product_version"] = oslevel

    machine_type = asset.split("-")[0]
    mtsn_info["machine_type"] = machine_type
    mtsn_info["serial_number"] = sr_no
    mtsn_info["country"] = "US"

    credentials["mtsn"] = [mtsn_info]

    event_body["credentials"] = credentials

    return event_body


def generate_geturl_body():
    '''
    Utility function that generates the body for the event part of the payload for getting the fixes.

    arguments: None

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of
                            the payload for getting the fixes.
    '''

    event_body = {}

    event_body["description"] = "Check on progress of software update - last contact is required to poll the service"
    event_body["enable_response_detail"] = True

    enable_response_detail_filter = []
    enable_response_detail_filter.append(softwareupdate_event_id)
    event_body["enable_response_detail_filter"] = enable_response_detail_filter

    event_body["component"] = "system"

    return event_body


def generate_confirm_body():
    '''
    Utility function that generates the body for the event part of the payload for confirming the resonse.

    arguments: None

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of the payload
                            for confirming the response.
    '''

    event_body = {}
    event_body["description"] = "Send the acknowledgement of getting the reponse"
    event_body["event_transaction_id"] = softwareupdate_event_id
    event_body["event_type"] = "software_update"
    event_body["component"] = "system"

    return event_body


def generate_downloadpost_body(module):
    '''
    Utility function that generates the body for the event part of the payload for getting the URLs.

    arguments: None

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of the payload
                            for getting the URLs.
    '''

    credentials = {}
    mtsn_info = {}
    filename = module.params['fix_id']

    event_body = {
        "action": "order_vios_software",
        "request_type": "specific_fix",
        "operation": "order_software",
        "component": "system",
        "expand_groups": True,
        "efd_product": "ibm/vios",
    }

    if isinstance(filename, list):
        event_body["update_ids"] = filename
    else:
        event_body["update_ids"] = [filename]

    event_body["product_version"] = oslevel

    machine_type = asset.split("-")[0]
    mtsn_info["machine_type"] = machine_type
    mtsn_info["serial_number"] = sr_no
    mtsn_info["country"] = "US"

    credentials["mtsn"] = [mtsn_info]

    event_body["credentials"] = credentials

    return event_body


def generate_download_body():
    '''
    Utility function that generates the body for the event part of the payload for getting the URL for a particular fix.

    arguments: None

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of
                            the payload for getting the URL for fix.
    '''

    event_body = {}

    event_body["description"] = "Check on progress of software update - last contact is required to poll the service"
    event_body["enable_response_detail"] = True

    enable_response_detail_filter = []
    enable_response_detail_filter.append(softwareupdate_event_id)
    event_body["enable_response_detail_filter"] = enable_response_detail_filter

    event_body["component"] = "system"

    return event_body


def generate_event(module, payload_type):
    '''
    Utility function to generate the JSON object (event), that will be sent in the JSON payload.

    arguments:
        payload_type (str) - Contains the type of request for which the event needs to be generated

    returns:
        event (list) - Dictionary inside a list containing required information about the event.

    This part is being generated here :

    "events": [
    {
      "header": {
        "event_id": "software_update_IBM_AIX_XXXX-XXX_XXXXXXX_1687344006365",
        "event_time": "2023-06-21 05:40:06",
        "event_time_ms": 1687344006365,
        "event_type": "software_update"
      },
      "body": {
        "operation": "order_software",
        "action": "order_aix_software",
        "component": "system",
        "expand_groups": true,
        "request_type": "preview_all_fixes",
        "efd_product": "ibm\aix",
        "product_level": "7200-02",
        "credentials": {
          "mtsn": [
            {
              "machine_type": "XXXX",
              "serial_number": "XXXXXXX",
              "country": "US"
            }
          ]
        },
        "product_version": ""
      }
    }
  ]
    '''

    events = {}

    events["header"] = generate_event_header(payload_type)

    if payload_type == "post":
        events["body"] = generate_post_body()

    elif payload_type == "geturl":
        events["body"] = generate_geturl_body()

    elif payload_type == "download":
        events["body"] = generate_download_body()

    elif payload_type == "downloadpost":
        events["body"] = generate_downloadpost_body(module)

    else:
        events["body"] = generate_confirm_body()

    events_list = []
    events_list.append(events)

    return events_list


def generate_payload(module, payload_type):
    '''
    Function to generate the Payload

    arguments:
        module - The Ansible module
        payload_type - Type of payload that needs to be created
    returns:
        payload_json (JSON) - A JSON object containing payload.

    The payload will look like this:

    {
   "agent":"Power_Ansible",
   "api_key":"iwkiwis8s9292sksk432156",
   "private_key":"39e93i93i9ei39abcde",
   "target_space":"prod",
   "asset":"XXXX-YYY",
   "asset_id":"XXXXXXXXXXXX",
   "asset_virtual_id":"00000000",
   "asset_type":"Power",
   "asset_vendor":"IBM",
   "country_code":"US",
   "type":"eccnext_apisv1s",
   "version":"1.0.0.1",
   "event_time":"2023-06-21 05:40:06",
   "event_time_ms":1687344006365,
   "software_level":{
      "name":"IBM_VIOS_Version",
      "vrmf":"3.1.4.0"
   },
   "event_id":"IBM_VIOS_XXXX-XXX_XXXXXXXXXXXX_1687344006365",
   "events":[
      {
         "header":{
            "event_type":"software_update",
            "event_id":"software_update_IBM_VIOS_XXXX-XXX_XXXXXXXXXXXX_1687344006365",
            "event_time":"2023-06-21 05:40:06",
            "event_type":"software_update"
         },
         "body":{
            "action":"order_vios_software",
            "operation":"order_software",
            "request_type":"preview_all_fixes",
            "component":"system",
            "efd_product":"ibm\vios",
            "product_version":"3.1.4.0",
            "credentials":{
               "mtsn":[
                  {
                     "machine_type":"XXXX",
                     "serial_number":"XXXXXXXXXXXX",
                     "country":"US"
                  }
               ]
            }
         }
      }
   ]
}

    '''

    software_level_info = {}

    payload["agent"] = "Power_Ansible"
    payload["api_key"] = "iwkiwis8s9292sksk432156"
    payload["private_key"] = "39e93i93i9ei39abcde"
    payload["target_space"] = "prod"
    payload["asset"] = asset
    payload["asset_id"] = asset_id
    payload["asset_virtual_id"] = "00000000"
    payload["asset_type"] = "Power"
    payload["asset_vendor"] = "IBM"
    payload["country_code"] = "US"
    payload["type"] = "eccnext_apisv1s"
    payload["version"] = "1.0.0.1"

    generate_event_details()
    payload["event_time"] = event_time
    payload["event_time_ms"] = event_time_ms

    software_level_info["name"] = "IBM_VIOS_Version"
    software_level_info["vrmf"] = oslevel
    payload["software_level"] = software_level_info

    # Value of event_id = will be something like this: IBM_VIOS_XXXX-XXX_XXXXXXXXXXXX_1687344006365

    generate_event_id()

    payload["event_id"] = event_id

    events = generate_event(module, payload_type)
    payload["events"] = events

    dictionary_to_json(payload, payload_type)


def download_fix(module, URL):
    '''
    Function to download the fix from the provided link.

    arguments:
        module (dict) - The Ansible module
        url (str) - URL of the fix

    returns:
        Nothing
    '''

    global size_of_file

    size_of_file /= 1000000
    check_space(module, size_of_file)

    for link in URL:
        filename = link.split('/')[-1]
        location = module.params['directory']

        if location[-1] != '/':
            location += '/'

        location += filename

        # urlretrieve will be used to download the file from the retrieved URL.

        urllib.request.urlretrieve(link, location)

    results['msg'] += "The fix has been downloaded."
    results['changed'] = True


####################################################################################
# Action Handler Functions
####################################################################################


def send_post(module):
    '''
    To send the POST request to EFD portal including all the necessary information.

    arguments:
        module (dict): The Ansible module.

    returns:
        Nothing
    '''

    generate_payload(module, "post")

    rc, stdout, stderr = module.run_command(curl_cmd)

    results['cmd'] = curl_cmd
    results['rc'] = rc
    results['stderr'] = stderr
    results['stdout'] = stdout

    if not check_response(stdout):
        results['msg'] = "POST request unsuccessful."
        module.fail_json(**results)
    results['msg'] = "POST request successful."


def send_downloadpost(module):
    '''
    To send the POST request to EFD portal including all the necessary information required for getting the URLs and further downloading the fixes.

    arguments:
        module (dict) : The Ansible module.

    returns:
        Nothing
    '''

    generate_payload(module, "downloadpost")

    rc, stdout, stderr = module.run_command(curl_cmd)

    results['cmd'] = curl_cmd
    results['rc'] = rc
    results['stderr'] = stderr
    results['stdout'] = stdout

    if not check_response(stdout):
        results['msg'] = "POST request unsuccessful."
        module.fail_json(**results)
    results['msg'] = "POST request successful."


def get_fixes(module):
    '''
    To send the POST request to EFD portal including all the necessary information.

    arguments:
        module (dict): The Ansible module.

    returns:
        Nothing
    '''

    generate_payload(module, "geturl")

    wait_for_response(module)

    res = json.loads(results['stdout'])

    results["List_of_Fixes"] = res["response_state"]["transactions"][str(softwareupdate_event_id)]["response_object"]["updates"]
    results['msg'] = "Successfully retrieved information about fixes, see List_of_fixes for the information."


def confirm_json(module):
    '''
    To send the POST request to EFD portal including all the necessary information.

    arguments:
        module (dict): The Ansible module.

    returns:
        Nothing
    '''

    generate_payload(module, "confirm")

    rc, stdout, stderr = module.run_command(curl_cmd)

    results['cmd'] = curl_cmd
    results['rc'] = rc
    results['stderr'] = stderr
    results['stdout'] = stdout

    if not check_response(stdout):
        results['msg'] = "Could not send confirm request."
        module.fail_json(**results)

    results['msg'] += " Response confirmed."


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            action=dict(type='str',
                        choices=['list', 'download'],
                        required=True),
            fix_id=dict(type='str'),
            directory=dict(type='str',
                           default='/'),
            clean_directory=dict(type='bool',
                                 default=False)
        ),
    )

    global curl_cmd
    global oslevel

    check_space(module, 2)
    check_requirements(module)
    oslevel = get_oslevel(module)
    get_info(module)
    get_serial_no(module)

    # The final command will be something like this: /opt/freeware/bin/curl --request POST --header 'accept: application/json' --header
    # 'content-type: application/json' -d @payload.json

    curl_cmd = "/opt/freeware/bin/curl --request POST --header 'accept: application/json' --header 'content-type: application/json' -d @payloadfile.json"
    curl_cmd += " --url  'https://esupport.ibm.com/connect/api/v1'"

    action = module.params['action']

    if action == "list":
        send_post(module)
        get_fixes(module)
        confirm_json(module)
    else:
        if not module.params['fix_id']:
            results['msg'] = "Fix id was not provided."
            module.fail_json(**results)
        check_empty_directory(module)
        send_downloadpost(module)
        URL = get_URL(module)
        download_fix(module, URL)
        confirm_json(module)

    remove_json_file(module)

    module.exit_json(**results)


if __name__ == '__main__':
    main()
