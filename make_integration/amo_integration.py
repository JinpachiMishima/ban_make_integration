import requests
from logging import getLogger

logger = getLogger(__name__)

class Amo:
    def __init__(self,integration_data):
        self.integration = integration_data
        self.header = {"Authorization":f"Bearer {self.integration.access_token}"}
        self.basic_url = "https://" + self.integration.sub_domain + "." + "amocrm.ru/" 
        
        self.contact = Contact(
            basic_url=self.basic_url,
            header=self.header
        )

        self.Lead = Lead(
            basic_url=self.basic_url,
            header=self.header
        )
    
    def checkConnection(self):
        url = self.basic_url + f"api/v4/account"
        response = requests.get(url=url,headers=self.header)
        return response.status_code
     
    def requestTokens(self,request_type):
        if request_type not in ["authorization_code","refresh_token"]:
            return False
        elif request_type == "authorization_code":
            req_type = "code"
            token = self.integration.code
        elif request_type == "refresh_token":
            req_type = "refresh_token"
            token = self.integration.refresh_token
        url = self.basic_url + "oauth2/access_token"
        
        data = {
            "client_id":f"{self.integration.client_id}",
            "client_secret":f"{self.integration.client_secret}",
            "grant_type":f"{request_type}",
            f"{req_type}":f"{token}",
            "redirect_uri":f"{self.integration.redirect_uri}"
        }
        response = requests.post(url=url,
                                 headers={"Content-Type":"application/json"},
                                 json=data)
        return response.status_code, response.json()

    def requestAccount(self):
        url = self.basic_url + f"api/v4/account"
        response = requests.get(url=url,headers=self.header)
        return response.json()


class Contact:
    def __init__(self, basic_url, header) -> None:
        self.basic_url = basic_url
        self.header = header

    def requestContact(self,contact_id):
        url = self.basic_url + f"api/v4/contacts/{contact_id}"
        response = requests.get(url=url,headers=self.header)
        return response.json()

    def requestContacts(self,**kwargs):
        url = ""
        for key in kwargs.keys():
            url += f"?filter[{key}]={kwargs[key]}"
        url = self.basic_url + "api/v4/contacts" + url
        response = requests.get(url=url,headers=self.header)
        return response.json()


class Lead:
    def __init__(self, basic_url, header) -> None:
        self.basic_url = basic_url
        self.header = header

    def requestLead(self,lead_id):
        url = self.basic_url + f"api/v4/leads/{lead_id}"
        response = requests.get(url=url,headers=self.header)
        return response.json()
    
    def requestLeads(
            self,
            _page:int=None,
            _limit:int=None,
            _with:list=None,
            _filter:dict=None,
    ):
        
        url = f"{self.basic_url}api/v4/leads?"
        if _limit != None:
            url += f"limit={_limit}"
        if _with != None:
            url = url + "&with=" + "&with=".join(_with)
        if _filter != None:
            url = url + "&" + "&".join([str(f"filter[{key}]={_filter[key]}") for key in _filter.keys()])
        
        if _page == None:
            page = 0
            request_page = []
            while True:
                page += 1
                response = requests.get(url=url+f"&page={page}",headers=self.header)
                print(f"страница: {page} {response.status_code}")
                if response.status_code == 200:
                    request_page += response.json()["_embedded"]["leads"]
                else:
                    break
        return request_page
