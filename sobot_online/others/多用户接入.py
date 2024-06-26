import threading
import time
import requests, random
from urllib.parse import urlencode
from faker import Faker
fake = Faker(locale="zh_CN")
from sobot_online.Bs_layer.bs_WorkBranche import WorkBranch
from threading import Thread


class Chat:
    def __init__(self):
        pass

    @classmethod
    def chat(cls,host="https://api-c.sobot.com/text",
             sysNum="cfd4681074ce4bed904928fb609fc824",
             groupId="75e16546892a4c5fa9fe07bbf9763e3b",
             partnerId=None):
        url = host + "/chat-visit/user/init/v6"
        if partnerId is None:
            partnerId = "admin-ali--" + str(random.randint(10000, 99999))
        payload = f'sysNum={sysNum}&source=0&groupId={groupId}&uname={partnerId}&partnerId={partnerId}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        uid = response.json()["uid"]
        cid = response.json()["cid"]
        puid = response.json()["puid"]

        url = host + "/chat-web/user/chatconnect.action"
        payload = f'sysNum={sysNum}&uid={uid}&cid={cid}&chooseAdminId=&tranFlag=0&current=false&groupId={groupId}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded', }
        response1 = requests.request("POST", url, headers=headers, data=payload)
        print(f"response1   >>>>{response1.text}")

        for i in range(1, 803):
            time.sleep(0.5)
            content = fake.text() + fake.text()
            # time.sleep(30)  # 每隔30秒发送一条信息给客服
            url = host + "/chat-web/message/user/send.action"
            data = urlencode({
                "puid": str(puid),
                "cid": str(cid),
                "uid": str(uid),
                "content": content,
                "objMsgType": "",
                "msgType": "0",
                "fileName": "undefined"
            })
            headers = {
                'bno': sysNum,
                'content-type': 'application/x-www-form-urlencoded',
            }
            response = requests.post(url=url, headers=headers, data=data)
            print(f"这是第{i}次，访客端返回数据response.text>>>：{response.text}")
        return uid, cid, puid

    @classmethod
    def customer_out(cls,host, uid):
        """
        客户离线
        :param host:
        :param uid:
        :return:
        """
        url = host + "chat-web/user/out.action"
        payload = f'uid={uid}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)


if __name__ == '__main__':
    pass
    obj = Chat()

    # for i in range(2,3):
    #     obj.chat(
    #         # host="https://sg-grey.sobot.io",
    #         # sysNum="826683f48d7244ada08a67bb37b26cf3",
    #         # groupId="285b3628fb28424aa5716ccf409306cf",
    #         partnerId="msgover" + str(i)
    #     )

    t1 = threading.Thread(target=Chat().chat,args=("https://api-c.soboten.com/text","5105b359aa37444284f5b0660a6fed24","c0ea210d47a945fbb125deddd245d602",'msgover1'))
    t2 = threading.Thread(target=obj.chat,args=("https://sg.sobot.com","826683f48d7244ada08a67bb37b26cf3","636b94224bb04b87ba1da42a16e278ea",'msgover1'))
    t3 = threading.Thread(target=obj.chat,args=("https://us.sobot.com","3837cca3bda44f88b5a065c72c0ba62d","0564047dd77945718aba3671fbfce50f",'msgover1'))
    t1.start()
    t2.start()
    t3.start()
