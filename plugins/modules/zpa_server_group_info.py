#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_server_group_info
short_description: Retrieves information about an server group
description:
    - This module will allow the retrieval of information about a server group resource.
author:
    - William Guilherme (@willguibr)
version_added: '1.0.0'
options:
  client_id:
    description: ""
    required: false
    type: str
  client_secret:
    description: ""
    required: false
    type: str
  customer_id:
    description: ""
    required: false
    type: str
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

EXAMPLES = """
- name: Get Details of All Server Groups
  willguibr.zpacloud.zpa_server_group_info:

- name: Get Details of a Specific Server Group by Name
  willguibr.zpacloud.zpa_server_group_info:
    name: Example

- name: Get Details of a Specific Server Group by ID
  willguibr.zpacloud.zpa_server_group_info:
    id: "216196257331291969"
"""

RETURN = """
# Returns information on a specified Server Group.
"""

from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_server_group import ServerGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc


def core(module):
    server_group_name = module.params.get("name", None)
    server_group_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ServerGroupService(module, customer_id)
    server_groups = []
    if server_group_id is not None:
        server_group = service.getByID(server_group_id)
        if server_group is None:
            module.fail_json(
                msg="Failed to retrieve server group ID: '%s'" % (id))
        server_groups = [server_group]
    elif server_group_name is not None:
        server_group = service.getByName(server_group_name)
        if server_group is None:
            module.fail_json(
                msg="Failed to retrieve server group Name: '%s'" % (server_group_name))
        server_groups = [server_group]
    else:
        server_groups = service.getAll()
    module.exit_json(changed=False, data=server_groups)


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
