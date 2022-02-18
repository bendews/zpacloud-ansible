from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
    camelcaseToSnakeCase,
)


class LSSClientTypesService:
    def __init__(self, module):
        self.module = module
        self.rest = ZPAClientHelper(module)

    def getAll(self):
        response = self.rest.get("/mgmtconfig/v2/admin/lssConfig/clientTypes")
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSON(response.json)

    def mapRespJSON(self, resp_json):
        if resp_json is None:
            return {}
        return camelcaseToSnakeCase(resp_json)
