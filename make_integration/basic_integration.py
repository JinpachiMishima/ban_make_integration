from datetime import date
import logging

from nigma_integration.lib.dbms import (
    Owners,
    AmoIntegrationData,
    WazzapIntegrationData
)
from nigma_integration.lib.amo_integration import Amo as amocrm
from nigma_integration.lib.wz_integration import Wazzup as wazzup

logger = logging.getLogger(__name__)

class Integration:
    
    def __init__(
            self,
            amo_integration_id=None,
            wz_integration_id=None
    ):
        self.amo_integration_id = amo_integration_id
        self.amo = amocrm(integration_data=AmoIntegrationData.getData(id=amo_integration_id))
        self.wz = wazzup(integration=WazzapIntegrationData.getData(id=wz_integration_id))
    
    def authorization(self):
        if self.amo.checkConnection() == True: #1) если access token действителен
            logger.debug(msg="access_token is correct")
            pass
        else:   #2)   если access_token недействителен
            logger.debug(msg="uncorrect access_token")
            response = self.amo.requestTokens(request_type="refresh_token")
            if response != False:   #3)   если refresh_token действителен
                logger.debug(msg="update tokens with refresh_token")
                refresh_token,access_token = response
                self.amo.integration.refresh_token = refresh_token
                self.amo.integration.access_token = access_token
                self.updateTokens()
            else:   #4)   если refresh_token недействителен
                logger.debug(msg="uncorrect refresh_token")
                response = self.amo.requestTokens(request_type="authorization_code")
                if response != False:   #5) если authorization_code действителен
                    logger.debug(msg="update tokens with authorization_code")
                    refresh_token,access_token = response
                    self.amo.integration.refresh_token = refresh_token
                    self.amo.integration.access_token = access_token
                    self.updateTokens()
                else:
                    logger.debug(msg="need to update authorization code")
                    return False
    
    def updateTokens(self):
        AmoIntegrationData.updateData(
            id=self.amo_integration_id,
            code="None",
            refresh_token=self.amo.integration.refresh_token,
            access_token=self.amo.integration.access_token,
            token_receipt_date=date.today()
        )