#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage Zscaler Private Access (ZPA) 2022
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_segment_group import SegmentGroupService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_segment_group_info
short_description: Gather information about an server group
description:
    - This module can be used to gather information about an server group.
author:
    - William Guilherme (@willguibr)
version_added: '1.0.0'
options:
  name:
    description:
     - Name of the server group.
    required: false
    type: str
  id:
    description:
     - ID of the server group.
    required: false
    type: str
"""

EXAMPLES = '''
- name: server group
  hosts: localhost
  tasks:
    - name: Gather information about all server group
      willguibr.zpacloud_ansible.zpa_segment_group_info:
        name: Browser Access Apps
        #id: 216196257331291969
      register: servers
    - name: servers
      debug:
        msg: "{{ servers }}"
'''

RETURN = r"""
data:
    description: server group information
    returned: success
    elements: dict
    type: list
    sample: [
      {
                "app_connector_groups": [
                    "216196257331291924"
                ],
                "applications": [
                    "216196257331291974"
                ],
                "config_space": "DEFAULT",
                "description": "SGIO Domain Controllers",
                "dynamic_discovery": true,
                "enabled": true,
                "id": "216196257331291964",
                "ip_anchored": false,
                "name": "SGIO Domain Controllers",
                "servers": [
                    "216196257331291974"
                ]
            }
    ]
"""


def core(module):
    segment_group_name = module.params.get("name", None)
    segment_group_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = SegmentGroupService(module, customer_id)
    segment_groups = []
    if segment_group_id is not None:
        segment_group = service.getByID(segment_group_id)
        if segment_group is None:
            module.fail_json(
                msg="Failed to retrieve segment group ID: '%s'" % (id))
        segment_groups = [segment_group]
    elif segment_group_name is not None:
        segment_group = service.getByName(segment_group_name)
        if segment_group is None:
            module.fail_json(
                msg="Failed to retrieve segment group Name: '%s'" % (segment_group_name))
        segment_groups = [segment_group]
    else:
        segment_groups = service.getAll()
    module.exit_json(changed=False, data=segment_groups)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()