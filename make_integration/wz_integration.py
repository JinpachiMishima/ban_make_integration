import requests
import logging

logger = logging.getLogger(__name__)

def checkResponse(response):
    if (response.status_code // 100) == 4:
        return False
    elif (response.status_code // 100) == 2:
        if response.status_code == 204:
            return False
        else:
            return response.json()
    else:
        return None


class Wazzup:
    request_api = {
        "send_message":"v3/message",

    }
    def __init__(self,integration):
        self.integration = integration
        self.basic_url = "https://api.wazzup24.com/"
        self.headers = {
            "Authorization":f"Bearer {self.integration.access_token}",
            "Content-Type": "application/json"
            }

    def sendMessage(self,chennal_id,chat_id,text):
        message_url = f"{self.basic_url}{Wazzup.request_api["send_message"]}"
        data = {
            "channelId":chennal_id,
            "chatId":chat_id,
            "chatType":"whatsapp",
            "text":text
            }
        response = requests.post(url=message_url,headers=self.headers,json=data)
        logger.info("send message to {}".format(chat_id))
        return response.status_code
    @staticmethod
    def correctPhone(phone):
        """Функция меняет все номера на +7"""
        # плохой парсер, не разпознает номера не 89...
        correct_phone = ""
        for num in phone[::-1]:
            if num in ["1","2","3","4","5","6","7","8","9","0"]:
                correct_phone += num
        if len(correct_phone) == 11:
            correct_phone = "+7" + correct_phone[:10][::-1]
            return correct_phone
        else:
            return False