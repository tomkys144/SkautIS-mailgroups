import yaml
from skautis import SkautisApi
from converter import converter
from google.oauth2 import service_account
import googleapiclient.discovery
import json
with open('config.yml', 'r') as config:
    cfg = yaml.load(config)
with open('./conf/gkey.json', 'r') as google_key:
    gkey = json.loads(google_key)

credentials = service_account.Credentials.from_service_account_file(google_key)
gservice = googleapiclient.discovery.build('admin', 'directory_v1', credentials=credentials)

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


def ggroups_first(login, unit, contacts, domain):
    group_list = skautis.GoogleApps.GoogleGroupAll(
        ID_Login=login, ID_Unit=unit, IncludeChildUnits=True, ID=None, DisplayName=None
    )
    for group in group_list: # simplifies group list
        group.remove('Unit', 'RegistrationNumber', 'DateCreate', 'Valid', 'AliasCount')

    for contact in contacts:  # takes every person in contact list
        for ID in contact['idlist']:  # gets every person's info in contact
            for mems in ID['memberships']:  # gets every membership of a person
                for group in group_list:  # takes every group from group list
                    if ID['Unit'] == mems['DisplayName']:
                        for email in contacts['mails']:  # takes every contact of a person
                            if email['ID_ContactType'] == 'email_hlavni':
                                request = gservice.members().hasMember(groupKey=group['ID'], memberKey=email['Value'])
                                response = request.get()
                                answer = json.loads(response)
                                if answer["isMember"] == False:
                                    skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                        ID_Login=login, ID=group['ID'], EmailArray=email['Value']
                                    )
                    elif "Rodiče - "+ID['Unit'] == mems['DisplayName']:
                        for email in contacts['mails']:
                            if email['ID_ContactType']=="email_otec" or email['ID_ContactType']=="email_matka":
                                request = gservice.members().hasMember(groupKey=group['ID'], memberKey=email['Value'])
                                response = request.get()
                                answer = json.loads(response)
                                if answer["isMember"] == False:
                                    skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                        ID_Login=login, ID=group['ID'], EmailArray=email['Value']
                                    )
                    else:
                        mail = converter(ID['Unit'])
                        new_id = skautis.GoogleApps.GoogleGroupInsert(
                            ID_Login=login, ID_Unit=unit, DisplayName=ID['Unit'], Email=mail+"@"+domain
                        )
                        skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                            ID_Login=login, ID=new_id, EmailArray=gkey['client_email']
                        )
                        skautis.GoogleApps.GoogleGroupUpdateMemberRole(
                            ID_Login=login, ID=new_id, Email=gkey['client_email'], IsOwner=True
                        )
                        for email in contacts['mails']:
                            if email['ID_ContactType']=='email_hlavni':
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=new_id, EmailArray=email['Value']
                                )
                        new_id = skautis.GoogleApps.GoogleGroupInsert(
                            ID_Login=login, ID_Unit=unit, DisplayName="Rodiče - "+ID['Unit'], Email="rodice-"+mail+"@"+domain
                        )
                        skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                            ID_Login=login, ID=new_id, EmailArray=gkey['client_email']
                        )
                        skautis.GoogleApps.GoogleGroupUpdateMemberRole(
                            ID_Login=login, ID=new_id, Email=gkey['client_email'], IsOwner=True
                        )
                        for email in contacts['mails']:
                            if email['ID_ContactType']=="email_otec" or email['ID_ContactType']=="email_matka":
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=new_id, EmailArray=email['Value']
                                )


def ggroups_second(login, unit, contacts):
    group_list = skautis.GoogleApps.GoogleGroupAll(
        ID_Login=login, ID_Unit=unit, IncludeChildUnits=True, ID=None, DisplayName=None
    )
    for group in group_list:
        group.remove('Unit', 'RegistrationNumber', 'DateCreate', 'Valid', 'AliasCount')

    for group in group_list:
        request = gservice.members().list(groupKey=group['ID'])
        response = request.get()
        answer = json.loads(response)
        group_mails = []
        for member in answer['members']:
            member_info = json.load(member)
            if member_info['email'] != gkey['client_email']:
                group_mails.append(member_info['email'])
            elif member_info['email'] == gkey['client_email'] and member_info['role'] != 'OWNER':
                skautis.GoogleApps.GoogleGroupUpdateMemberRole(
                    ID_Login=login, ID=group['ID'], Email=gkey['client_email'], IsOwner=True
                )
                unit_mails = []
        for contact in contacts:
            if group['DisplayName'] in contact['person']['memberships']['unit'] and 'Rodiče' not in group['DisplayName']:
                for email in contact['mails']:
                    if email['ID_ContactType'] == 'email_hlavni':
                        unit_mails.append(email['Value'])
            elif group['DisplayName'] in contact['person']['memberships']['unit'] and 'Rodiče' in group['DisplayName']:
                for email in contact['mails']:
                    if email['ID_ContactType'] == "email_otec" or email['ID_ContactType'] == "email_matka":
                        unit_mails.append(email['Value'])

        difference = set(group_mails) ^ set(unit_mails)
        if difference:
            for mail in difference:
                skautis.GoogleApps.GoogleGroupDeleteMember(
                    ID_Login=login, ID=group['ID'], Email=mail
                )


def run():
    perl = person_list(cfg['login'],cfg['unit'], False)
    idl = id_list(perl, cfg['login'])
    cnts = contacts(idl, cfg['login'])
    ggroups_first(cfg['login'], cfg['unit'], cnts, cfg['domain'])
