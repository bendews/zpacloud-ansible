#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_provisioning_key import ProvisioningKeyService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_provisioning_key
short_description: Create/ an Provisioning Key
description:
  - This module will create, retrieve, update or delete a specific Provisioning Key
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  enabled:
    type: bool
    required: False
    description: "Whether the provisioning key is enabled or not. Supported values: true, false"
    default: true
  max_usage:
    type: str
    required: True
    description: "The maximum number of instances where this provisioning key can be used for enrolling an App Connector or Service Edge."
  enrollment_cert_id:
    type: str
    required: True
    description: "ID of the enrollment certificate that can be used for this provisioning key."
  ui_config:
    type: str
    required: False
    description: ""
  provisioning_key:
    type: str
    description: "read only field. Ignored in PUT/POST calls."
  association_type:
    type: str
    required: True
    description: "Specifies the provisioning key type for App Connectors or ZPA Private Service Edges. The supported values are CONNECTOR_GRP and SERVICE_EDGE_GRP."
  id:
    type: str
    required: False
    description: ""
  name:
    type: str
    required: True
    description: "Name of the provisioning key."
  usage_count:
    type: str
    required: False
    description: "The provisioning key utilization count."
  zcomponent_id:
    type: str
    required: True
    description: "ID of the existing App Connector or Service Edge Group."
  zcomponent_name:
    type: str
    required: False
    description: "Read only property. Applicable only for GET calls, ignored in PUT/POST calls."
  enrollment_cert_name:
    type: str
    description: "Read only property. Applicable only for GET calls, ignored in PUT/POST calls."
  app_connector_group_id:
    type: str
    required: False
    description: ""
  app_connector_group_name:
    type: str
    description: "Read only property. Applicable only for GET calls, ignored in PUT/POST calls."
  ip_acl:
    type: list
    elements: str
    description: ""
    required: False
"""

EXAMPLES = '''
- name: App Provisioning Key
  hosts: localhost
  tasks:
    - name: Create/update/delete a Provisioning Key
      willguibr.zpacloud_ansible.zpa_provisioning_key:
        name             : "New York Provisioning Key"
        association_type : "CONNECTOR_GRP"
        max_usage        : "10"
        enrollment_cert_id : 92828292
        zcomponent_id : 2828227
      register: key
    - name: created key
      debug:
        msg: "{{ key }}"

'''

RETURN = r"""
data:
    description: Provisioning Key
    returned: success
    type: dict
    sample:
        {
            "app_connector_group_id": null,
            "app_connector_group_name": "USA App Connector Group",
            "creation_time": "1639693617",
            "enabled": true,
            "enrollment_cert_id": "6573",
            "enrollment_cert_name": "Connector",
            "expiration_in_epoch_sec": null,
            "id": "8691",
            "ip_acl": null,
            "max_usage": "2",
            "modified_by": "216196257331282070",
            "modified_time": null,
            "name": "USA App Connector Group",
            "provisioning_key": "3|api.private.zscaler.com|Wy3HzPKWJr88i6uA...",
            "ui_config": null,
            "usage_count": "0",
            "zcomponent_id": "216196257331291906",
            "zcomponent_name": "USA App Connector Group",
        }

"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = ProvisioningKeyService(module, customer_id)
    provisioning_key = dict()
    params = [
        "app_connector_group_id",
        "app_connector_group_name",
        "creation_time",
        "enabled",
        "expiration_in_epoch_sec",
        "id",
        "ip_acl",
        "max_usage",
        "modified_by",
        "modified_time",
        "name",
        "provisioning_key",
        "enrollment_cert_id",
        "enrollment_cert_name",
        "ui_config",
        "usage_count",
        "zcomponent_id",
        "zcomponent_name",
        "association_type"
    ]
    association_type = module.params.get("association_type")
    for param_name in params:
        provisioning_key[param_name] = module.params.get(param_name, None)
    existing_key = service.getByIDOrName(
        provisioning_key.get("id"), provisioning_key.get("name"), association_type)
    if existing_key is not None:
        id = existing_key.get("id")
        existing_key.update(provisioning_key)
        existing_key["id"] = id
    if state == "present":
        if existing_key is not None:
            """Update"""
            existing_key = service.update(existing_key, association_type)
            module.exit_json(changed=True, data=existing_key)
        else:
            """Create"""
            provisioning_key = service.create(
                provisioning_key, association_type)
            module.exit_json(changed=False, data=provisioning_key)
    elif state == "absent":
        if existing_key is not None:
            service.delete(existing_key.get("id"), association_type)
            module.exit_json(changed=False, data=existing_key)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        app_connector_group_id=dict(type="str", required=False),
        app_connector_group_name=dict(type="str", required=False),
        creation_time=dict(type="str", required=False),
        enabled=dict(type="bool", default=True, required=False),
        expiration_in_epoch_sec=dict(type="str", required=False),
        id=dict(type="str", required=False),
        ip_acl=dict(type="str", required=False),
        max_usage=dict(type="str", required=True),
        modified_by=dict(type="str", required=False),
        modified_time=dict(type="str", required=False),
        name=dict(type="str", required=True),
        provisioning_key=dict(type="str", required=False),
        enrollment_cert_id=dict(type="str", required=True),
        enrollment_cert_name=dict(type="str", required=False),
        ui_config=dict(type="str", required=False),
        usage_count=dict(type="str", required=False),
        zcomponent_id=dict(type="str", required=True),
        zcomponent_name=dict(type="str", required=False),
        association_type=dict(type="str", choices=[
                              "CONNECTOR_GRP", "SERVICE_EDGE_GRP"], required=True),
        state=dict(type="str", choices=[
                   "present", "absent"], default="present"),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
