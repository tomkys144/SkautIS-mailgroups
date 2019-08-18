import yaml
from skautis import SkautisApi
from converter import converter
from google.oauth2 import service_account
import googleapiclient.discovery
with open("config.yml", "r") as config:
    cfg = yaml.load(config)


# API call
skautis = SkautisApi(appId=cfg['key'], test=True)


# person list
def person_list(login, unit, direct):
    plist = skautis.OrganizationUnit.PersonAll(
        ID_Login=login, ID_Unit=unit, OnlyDirectMember=direct, ID=None, ID_FunctionType=None, ID_QualificationType=None
    )
    return plist


def id_list(person_list, login):
    idlist = []
    for person in person_list:
        units = skautis.OrganizationUnit.MembershipAllPerson(
            ID_Login=login, ID_Person=person['ID'], ID_Unit=None, ShowHistory=False, IsValid=True
        )
        memberships = []
        for unt in units:
            unit = unt['Unit']
            id_unit = unt['ID_Unit']
            memberships.append([unit, id_unit])
        idlist.append([person['ID'], memberships])
    return idlist


def contacts(idlist, login):
    cnts = []
    for person in idlist:
        ID = person['ID']
        con_list = skautis.OrganizationUnit.PersonContactAll(
            ID_Login=login, ID_Person=ID, IsCatalog=None, IsMain=None, ID_ContactType=None
        )
        mails = []
        for cnt in con_list:
            mails.append(cnt['ID_ContactType', 'Value'])
        cnts.append([person, mails])
    return cnts


def ggroups(login, unit, path_key, contacts, domain):
    group_list = skautis.GoogleApps.GoogleGroupAll(
        ID_Login=login, ID_Unit=unit, IncludeChildUnits=True, ID=None, DisplayName=None
    )
    for grp in group_list: # simplifies group list
        grp.remove('Unit', 'RegistrationNumber', 'DateCreate', 'Valid', 'AliasCount')

    credentials = service_account.Credentials.from_service_account_file(path_key)
    gservice = googleapiclient.discovery.build('admin', 'directory_v1', credentials=credentials)

    for cnt in contacts:  # takes every person in contact list
        for ID in cnt['idlist']:  # gets every person's info in contact
            for mems in ID['memberships']:  # gets every membership of a person
                for grp in group_list:  # takes every group from group list
                    if ID['Unit'] == mems['DisplayName']:
                        for cnt in contacts['mails']:  # takes every contact of a person
                            if cnt['ID_ContactType'] == 'email_hlavni':
                                request = gservice.members().hasMember(groupKey=grp['ID'], memberKey=cnt['Value'])
                                response = request.get()
                                if response["isMember"] == False:
                                    skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                        ID_Login=login, ID=grp['ID'], EmailArray=cnt['Value']
                                    )
                    elif "Rodiče - "+ID['Unit'] == mems['DisplayName']:
                        for cnt in contacts['mails']:
                            if cnt['ID_ContactType']=="email_otec" or cnt['ID_ContactType']=="email_matka":
                                request = gservice.members().hasMember(groupKey=grp['ID'], memberKey=cnt['Value'])
                                response = request.get()
                                if response["isMember"] == False:
                                    skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                        ID_Login=login, ID=grp['ID'], EmailArray=cnt['Value']
                                    )
                    else:
                        mail = converter(ID['Unit'])
                        new_id = skautis.GoogleApps.GoogleGroupInsert(
                            ID_Login=login, ID_Unit=unit, DisplayName=ID['Unit'], Email=mail+"@"+domain
                        )
                        for cnt in contacts['mails']:
                            if cnt['ID_ContactType']=="email_hlavni":
                                skautis.GoogleApps.GoogleGroupDeleteMember(
                                    ID_Login=login, ID=new_id, Email=cnt['Value']
                                )
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=new_id, EmailArray=cnt['Value']
                                )
                        new_id = skautis.GoogleApps.GoogleGroupInsert(
                            ID_Login=login, ID_Unit=unit, DisplayName="Rodiče - "+ID['Unit'], Email="rodice-"+mail+"@"+domain
                        )
                        for cnt in contacts['mails']:
                            if cnt['ID_ContactType']=="email_hlavni":
                                skautis.GoogleApps.GoogleGroupDeleteMember(
                                    ID_Login=login, ID=new_id, Email=cnt['Value']
                                )
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=new_id, EmailArray=cnt['Value']
                                )


def run():
    perl = person_list(cfg['login'],cfg['unit'], False)
    idl = id_list(perl, cfg['login'])
    cnts = contacts(idl, cfg['login'])
    ggroups(cfg['login'], cfg['unit'],cfg['gkey'], cnts, cfg['domain'])
