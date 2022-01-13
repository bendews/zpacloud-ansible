#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_scim_attribute_header import ScimAttributeHeaderService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
author: William Guilherme (@willguibr)
description:
  - Provides details about a specific scim attribute header from a given IDP
module: zpa_scim_attribute_header_info
short_description: Provides details about a specific scim attribute header from a given IDP
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the scim attribute.
    required: false
    type: str
  idp_name:
    description:
      - Name of the IDP, required when ID is not sepcified.
    required: false
    type: str
  id:
    description:
      - ID of the scim attribute.
    required: false
    type: str

"""

EXAMPLES = """
    - name: Gather information about all SCIM Attribute of an IDP
      willguibr.zpacloud.zpa_scim_attribute_header_info:
        idp_name: IdP_Name

    - name: Gather information about the SCIM Attribute by Name
      willguibr.zpacloud.zpa_scim_attribute_header_info:
        name: costCenter
        idp_name: SGIO-User-Okta

    - name: Gather information about the SCIM Attribute by ID
      willguibr.zpacloud.zpa_scim_attribute_header_info:
        id: 216196257331285842
        idp_name: SGIO-User-Okta
"""

RETURN = """
data:
    description: saml attribute information
    returned: success
    elements: dict
    type: list
    data: [
            {
              "canonical_values": null,
              "case_sensitive": false,
              "creation_time": "1631718085",
              "data_type": "String",
              "description": null,
              "id": "216196257331285842",
              "idp_id": "216196257331285825",
              "modified_by": "216196257331281958",
              "modified_time": null,
              "multivalued": false,
              "mutability": "readWrite",
              "name": "costCenter",
              "required": false,
              "returned": "default",
              "schema_uri": "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User",
              "uniqueness": false
            }
    ]
"""


def core(module):
    scim_attr_name = module.params.get("name", None)
    idp_name = module.params.get("idp_name", None)
    scim_attr_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ScimAttributeHeaderService(module, customer_id)
    attributes = []
    if scim_attr_id is not None:
        attribute = service.getByID(scim_attr_id, idp_name)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve scim attribute header ID: '%s'" % (id))
        attributes = [attribute]
    elif scim_attr_name is not None:
        attribute = service.getByName(scim_attr_name, idp_name)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve scim attribute header Name: '%s'" % (scim_attr_name))
        attributes = [attribute]
    else:
        attributes = service.getAllByIDPName(idp_name)
    module.exit_json(changed=False, data=attributes)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
        idp_name=dict(type="str", required=True)
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
