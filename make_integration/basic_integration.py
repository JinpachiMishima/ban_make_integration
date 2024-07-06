

def updateTokens(amo,response,amo_integration_id):
    amo.integration.code = "None",
    amo.integration.refresh_token=response["refresh_token"],
    amo.integration.access_token=response["access_token"],
    amo.integration.token_receipt_date=datetime.now().date()
    AmoIntegrationData.updateData(
        id=amo_integration_id,
        code="None",
        refresh_token=response["refresh_token"],
        access_token=response["access_token"],
        token_receipt_date=datetime.now().date()
        )

def authorization(amo,amo_integration_id):
    if (amo.checkConnection() // 100) == 4: # если access token не действителен
        print("access token не действителен")
        status_code, response = amo.requestTokens(request_type="refresh_token")
        if (status_code // 100) == 4:   # если refresh_token недействителен
            print("refresh token недействителен")
            status_code, response = amo.requestTokens(request_type="authorization_code")
            if (status_code // 100) == 4:   # если  authorization_code недействителен
                print("authorization token недействителен")
                raise Exception("Недействительные ключи доступа")
            else:   # если authorization code действителен
                updateTokens(amo,response,amo_integration_id)
                print("refresh token действителен")
        else:   # если refresh token действителен, обновить токены
            updateTokens(amo,response,amo_integration_id)
    else:   # если access_token действителен
        pass
