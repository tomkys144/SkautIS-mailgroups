import yaml
from skautis import SkautisApi
from converter import converter
from google.oauth2 import service_account
import googleapiclient.discovery
import json
import logging
import datetime
with open('config.yml', 'r') as config:
    cfg = yaml.load(config)
with open('./conf/gkey.json', 'r') as google_key:
    gkey = json.loads(google_key)

today = datetime.date.today()
ftoday = today.strftime("%d/%m/%Y")
now = datetime.time.now()
fnow = now.strftime("%H/%M/%S")


name = '/log/log_{0}_{1}'.format(ftoday, fnow)
log = logging.getLogger(__name__)
fhandler = logging.FileHandler(name)
log.setLevel(logging.INFO)
log.addHandler(fhandler)

credentials = service_account.Credentials.from_service_account_file(google_key)
gservice = googleapiclient.discovery.build('admin', 'directory_v1', credentials=credentials)

# API call
skautis = SkautisApi(appId=cfg['key'], test=True)


def personlister(login, unit):
    plist = skautis.OrganizationUnit.PersonAll(
        ID_Login=login, ID_Unit=unit, OnlyDirectMember=True, ID=None, ID_FunctionType=None, ID_QualificationType=None
    )
    return plist


def contactlister(login, unit):
    clist = {}
    persons = personlister(login, unit)
    for person in persons:
        ID = person['ID']
        contacts = skautis.OrganizationUnit.PersonContactAll(
            ID_Login=login, ID_Person=ID, IsCatalog=None, IsMain=None, ID_ContactType=None
        )
        members = []
        parents = []
        for contact in contacts:
            if contact['ID_ContactType'] == 'email_hlavni':
                members.append(contact['Value'])
            elif contact['ID_ContactType'] == 'email_otec' or contact['ID_ContactType'] == 'email_matka':
                parents.append(contact['Value'])
        clist['members'] = members
        clist['parents'] = parents
    return clist


def unitlister(login, unit):
    ulist = []
    units = skautis.OrganizationUnit.UnitAllUnit(
        ID_Login=login, ID_Unit=unit, SearchStredisko=True
    )
    for unt in units:
        del unt['ID_UnitType'], unt['RegistrationNumber'], unt['SortName']
        ulist.append(unt)
    return ulist


def grouplister(login, unit):
    glist = []
    groups = skautis.GoogleApps.GoogleGroupAll(
        ID_Login=login, ID_Unit=unit, ID=None, DisplayName=None, IncludeChildUnits=False
    )
    for group in groups:
        del group['Unit'], group['RegistrationNumber'], group['DateCreate'], group['Valid'], group['AliasCount']
        glist.append(group)
    return glist


def checker(login, unit):
    units = unitlister(login, unit)
    for unt in units:
        contacts = contactlister(login, unt['ID'])
        groups = grouplister(login, unt)
        for group in groups:
            if group:
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
                        log.info('Service account {0} set as owner of group {1}'.format(gkey['client_email'], group['DisplayName']))
                if 'Rodiče' not in group['DisplayName']:
                    missing = set(contacts['members']).difference(group_mails)
                    for email in missing:
                        skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                            ID_Login=login, ID=group['ID'], EmailArray=email
                        )
                        log.info('Email {0} added to group {1]'.format(email, group['DisplayName']))
                    additional = set(group_mails).difference(contacts['members'])
                    for email in additional:
                        skautis.GoogleApps.GoogleGroupDeleteMember(
                            ID_Login=login, ID=group['ID'], Email=email
                        )
                        log.info('Email {0} removed from group {1]'.format(email, group['DisplayName']))
                elif 'Rodiče' in group['DisplayName']:
                    missing = set(contacts['parents']).difference(group_mails)
                    for email in missing:
                        skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                            ID_Login=login, ID=group['ID'], EmailArray=email
                        )
                        log.info('Email {0} added to group {1]'.format(email, group['DisplayName']))
                    additional = set(group_mails).difference(contacts['parents'])
                    for email in additional:
                        skautis.GoogleApps.GoogleGroupDeleteMember(
                            ID_Login=login, ID=group['ID'], Email=email
                        )
                        log.info('Email {0} removed from group {1]'.format(email, group['DisplayName']))
                else:
                    log.error(
                        'Invalid name of Ggroup! | unit: {0} | group name: {1}'.format(unt['DisplayName'], group['DisplayName'])
                                    )
            else:
                mail = converter(unt['DisplayName'])
                new_id = skautis.GoogleApps.GoogleGroupInsert(
                    ID_Login=login, ID_Unit=unt['ID'], DisplayName="Rodiče - " + unt['DisplayName'],
                    Email="rodice-" + mail + "@" + cfg['domain']
                )
                log.info('Created group {}'.format("Rodiče - " + unt['DisplayName']))
                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                    ID_Login=login, ID=new_id, EmailArray=contacts['parents']
                )
                log.info('Added these emails to the group {0}: {1}'.format(
                    "Rodiče - " + unt['DisplayName'], contacts['parents']
                ))
                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                    ID_Login=login, ID=new_id, EmailArray=gkey['client_email']
                )
                skautis.GoogleApps.GoogleGroupUpdateMemberRole(
                    ID_Login=login, ID=group['ID'], Email=gkey['client_email'], IsOwner=True
                )
                log.info('Added {0} into group {1} as owner'.format(
                    gkey['client_email'], "Rodiče - " + unt['DisplayName']
                ))
                new_id = skautis.GoogleApps.GoogleGroupInsert(
                    ID_Login=login, ID_Unit=unt['ID'], DisplayName=unt['DisplayName'],
                    Email=mail + "@" + cfg['domain']
                )
                log.info('Created group {}'.format(unt['DisplayName']))
                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                    ID_Login=login, ID=new_id, EmailArray=contacts['members']
                )
                log.info('Added these emails to the group {0}: {1}'.format(
                    unt['DisplayName'], contacts['parents']
                ))
                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                    ID_Login=login, ID=new_id, EmailArray=gkey['client_email']
                )
                skautis.GoogleApps.GoogleGroupUpdateMemberRole(
                    ID_Login=login, ID=group['ID'], Email=gkey['client_email'], IsOwner=True
                )
                log.info('Added {0} into group {1} as owner'.format(
                    gkey['client_email'], unt['DisplayName']
                ))

