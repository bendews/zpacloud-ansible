from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)


class IDPControllerService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        idp = None
        if id is not None:
            idp = self.getByID(id)
        if idp is None and name is not None:
            idp = self.getByName(name)
        return idp

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/idp/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/idp" % (self.customer_id), data_key_name="list")
        idps = []
        for idp in list:
            idps.append(self.mapRespJSONToApp(idp))
        return idps

    def getByName(self, name):
        idps = self.getAll()
        for idp in idps:
            if idp.get("name") == name:
                return idp
        return None

    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "id": resp_json.get("id"),
            "name": resp_json.get("name"),
        }

    def mapAppToJSON(self, idp):
        if idp is None:
            return {}
        return {
            "id": idp.get("id"),
            "name": idp.get("name"),
        }
