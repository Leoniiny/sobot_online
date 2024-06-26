# !/usr/bin python3                                 
# encoding: utf-8 -*-
# @Function：CRM相关业务
from sobot_online.Bs_layer.bs_OnlineAgent import ConsoleSetting
import json
from sobot_online.Bs_layer.bs_login import Login


class CRM(Login):
    def __init__(self):
        super().__init__()

    def get_blacklist(self,searchType="6",searchValue=None,pageSize="15",pageNo="1",userid=None):
        '''
        :param userid:
        :param pageNo:
        :param pageSize:
        :param searchType: 查询方式；6：对接ID
        :param searchValue:
        :return:
        '''
        url = self.host + "/crm-user-service/userBlack/listByPage"
        params = {
            "searchType": searchType,
            "searchValue": searchValue,
            "pageSize": pageSize,
            "pageNo": pageNo,
            "sortField": "blackTime",
            "sortType": "desc"
        }
        headers = {
            'bno': self.bno,
            'temp-id': self.tempid
        }
        response = self.session.get(url, headers=headers, params=params)
        if json.loads(response.text).get("items"):
            print(f"get_blacklist  的值为>>> ：{json.loads(response.text).get('items')}")
            userid = json.loads(response.text).get("items")[-1].get('userId')
            return userid
        else:
            print("黑名单不存在")
            return userid

    def remove_blacklist(self,userid=None):
        if userid is None:
            pass
        else:
            url = self.host + f"/crm-user-service/userBlack/remove/{userid}"
            data = json.dumps({})
            headers = {
                'bno': self.bno,
                'content-type': 'application/json;charset=UTF-8',
                'temp-id': self.tempid
            }
            response = self.session.post(url, headers=headers, data=data)
            print(f"remove_blacklist response.text 的值为>>>：{response.text}")

    def del_label(self):
        url = self.host + "/crm-user-service/userLabel/remove/cd551799f627416c883b8b3faa42ffef"
        data = {

        }
        headers = {
            'bno': self.bno,
            'content-type': 'application/x-www-form-urlencoded',
            'temp-id': self.tempid,
        }

        response = requests.request("POST", url, headers=headers, data=data)

        print(response.text)


if __name__ == '__main__':
    pass
    obj = CRM()
    userid = obj.get_blacklist()
    obj.remove_blacklist(userid)

