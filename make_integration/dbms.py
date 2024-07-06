from logging import getLogger
from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
    ForeignKey,
    create_engine
)
from sqlalchemy.orm import (
    Session, 
    mapped_column, 
    Mapped
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()
engine = create_engine("sqlite:///database\\dataBase.db")
logger = getLogger(__name__)

class Owners(Base):
    """"""
    __tablename__ = "Owners"
    
    id: Mapped[int] = mapped_column(primary_key=True,
                autoincrement=True,
                nullable=True,
                unique=True) 
    name: Mapped[str] = mapped_column(String(50),
                                      nullable=True)

    def createOwner(name:str):
        with Session(engine) as session:
            with session.begin():
                new_owner = Owners(name=name)
                session.add(new_owner)
    
    def updateOwner(id:int,name:str):
        with Session(engine) as session:
            with session.begin():
                session.query(Owners).filter(Owners.id == id).update(
                    {"name":name}
                )
                
    def deleteOwner(id:int):
        with Session(engine) as session:
            with session.begin():
                owner = session.get(Owners,id)
                session.delete(owner)
    
    def getOwner(id:int):
        with Session(engine) as session:
            owner = session.get(Owners,id)
        return owner

    def getOwners():
        with Session(engine) as session:
            owners = session.query(Owners).all()
        return owners


class AmoIntegrationData(Base):
    __tablename__ = "AmoIntegrationData"
    
    id: Mapped[int] = mapped_column(primary_key=True,
                autoincrement=True,
                nullable=True,
                unique=True)
    owner_id = mapped_column(ForeignKey(Owners.id))
    integration_name: Mapped[str] = mapped_column(String(50))
    sub_domain: Mapped[str] = mapped_column(String(50))
    client_id: Mapped[str] = mapped_column(String(50))
    client_secret: Mapped[str] = mapped_column(String(50))
    redirect_uri: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(String(1000))
    refresh_token: Mapped[str] = mapped_column(String(1000))
    access_token: Mapped[str] = mapped_column(String(1000))
    token_receipt_date = Column(Date)

    def createData(owner_id,
                   integration_name,
                   sub_domain,
                   client_id,
                   client_secret,
                   redirect_uri,
                   code,
                   refresh_token,
                   access_token,
                   token_receipt_date):
        with Session(engine) as session:
            with session.begin():
                integration = AmoIntegrationData(owner_id=owner_id,
                                                integration_name=integration_name,
                                                sub_domain=sub_domain,
                                                client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                code=code,
                                                refresh_token=refresh_token,
                                                access_token=access_token,
                                                token_receipt_date=token_receipt_date)
                session.add(integration)

    def updateData(id,owner_id=None,
                   integration_name=None,
                   sub_domain=None,
                   client_id=None,
                   client_secret=None,
                   redirect_uri=None,
                   code=None,
                   refresh_token=None, 
                   access_token=None,
                   token_receipt_date=None):
        data = AmoIntegrationData.getData(id=id)
        if owner_id != None:
            data.owner_id = owner_id
        if integration_name != None:
            data.integration_name = integration_name
        if sub_domain != None:
            data.sub_domain = sub_domain
        if client_id != None:
            data.client_id = client_id
        if client_secret != None:
            data.client_secret = client_secret
        if redirect_uri != None:
            data.redirect_uri = redirect_uri
        if code != None:
            data.code = code
        if refresh_token != None:
            data.refresh_token = refresh_token
        if access_token != None:
            data.access_token = access_token
        if token_receipt_date != None:
            data.token_receipt_date = token_receipt_date
        
        with Session(engine) as session:
            with session.begin():
                session.query(AmoIntegrationData).filter(AmoIntegrationData.id == id).update(
                    {"owner_id":data.owner_id,
                     "integration_name":data.integration_name,
                     "sub_domain":data.sub_domain,
                     "client_id":data.client_id,
                     "client_secret":data.client_secret,
                     "redirect_uri":data.redirect_uri,
                     "code":data.code,
                     "refresh_token":data.refresh_token,
                     "access_token":data.access_token,
                     "token_receipt_date":data.token_receipt_date}
                )

    def getData(id):
        with Session(engine) as session:
            integration = session.get(AmoIntegrationData,id)
        return integration

    def getAllData():
        with Session(engine) as session:
            all_data = session.query(AmoIntegrationData).all()
        return all_data

    def deleteData(id):
        with Session(engine) as session:
            with session.begin():
                integration = session.get(AmoIntegrationData,id)
                session.delete(integration)


class WazzapIntegrationData(Base):
    __tablename__ = "WazzapIntegrationData"

    id: Mapped[int] = mapped_column(primary_key=True,
                autoincrement=True,
                nullable=True,
                unique=True)
    owner_id = Column(ForeignKey(Owners.id))
    integration_name: Mapped[str] = mapped_column(String(50))
    access_token: Mapped[str] = mapped_column(String(100))

    def createData(owner_id,integration_name,access_token):
        with Session(engine) as session:
            with session.begin():
                integration =  WazzapIntegrationData(owner_id=owner_id,
                                                     integration_name=integration_name,
                                                     access_token=access_token)
                session.add(integration)
    
    def updateData(id,owner_id=None,integration_name=None,access_token=None):
        data = WazzapIntegrationData.getData(id=id)
        if owner_id != None:
            data.owner_id = owner_id
        if integration_name != None:
            data.integration_name = integration_name
        if access_token != None:
            data.access_token = access_token
        
        with Session(engine) as session:
            with session.begin():
                session.query(WazzapIntegrationData).filter(WazzapIntegrationData.id == id).update(
                    {"owner_id":data.owner_id,
                     "integration_name":data.integration_name,
                     "access_token":data.access_token
                    }
                )

    def getData(id):
        with Session(engine) as session:
            integration = session.get(WazzapIntegrationData,id)
        return integration
    
    def getAllData():
        with Session(engine) as session:
            all_data = session.query(WazzapIntegrationData).all()
        return all_data

    def deleteData(id):
        with Session(engine) as session:
            with session.begin():
                integration = session.get(WazzapIntegrationData,id)
                session.delete(integration)


if __name__ == "__main__":
    pass
    # Base.metadata.create_all(engine)
    AmoIntegrationData.updateData(
        id=3,
        access_token="None"
    )