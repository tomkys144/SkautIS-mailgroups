import yaml
from skautis import SkautisApi
from Converter import converter
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
    for x in person_list:
        units = skautis.OrganizationUnit.MembershipAllPerson(
            ID_Login=login, ID_Person=x['ID'], ID_Unit=None, ShowHistory=False, IsValid=True
        )
        memberships = []
        for y in units:
            unit = y['Unit']
            id_unit = y['ID_Unit']
            memberships.append([unit, id_unit])
        idlist.append([x['ID'], memberships])
    return idlist


def contacts(idlist, login):
    cnts = []
    for x in idlist:
        person = x['ID']
        con_list = skautis.OrganizationUnit.PersonContactAll(
            ID_Login=login, ID_Person=person, IsCatalog=None, IsMain=None, ID_ContactType=None
        )
        mails = []
        for y in con_list:
            mails.append(y['ID_ContactType', 'Value'])
        cnts.append([idlist, mails])
    return cnts


def ggroups(login, unit, contacts, domain):
    group_list = skautis.GoogleApps.GoogleGroupAll(
        ID_Login=login, ID_Unit=unit, IncludeChildUnits=True, ID=None, DisplayName=None
    )
    for n in group_list:
        n.remove('Unit', 'RegistrationNumber', 'DateCreate', 'Valid', 'AliasCount')
    for x in contacts:
        for y in x['idlist']:
            for z in y['memberships']:
                for a in group_list:
                    if y['Unit'] == z['DisplayName']:
                        for b in contacts['mails']:
                            if b['ID_ContactType']=="email_hlavni":
                                skautis.GoogleApps.GoogleGroupDeleteMember(
                                    ID_Login=login, ID=a['ID'], Email=b['Value']
                                )
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=a['ID'], EmailArray=b['Value']
                                )
                    elif "Rodiče - "+y['Unit'] == z['DisplayName']:
                        for b in contacts['mails']:
                            if b['ID_ContactType']=="email_otec" or b['ID_ContactType']=="email_matka":
                                skautis.GoogleApps.GoogleGroupDeleteMember(
                                    ID_Login=login, ID=a['ID'], Email=b['Value']
                                )
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=a['ID'], EmailArray=b['Value']
                                )
                    else:
                        mail = converter(y['Unit'])
                        new_id = skautis.GoogleApps.GoogleGroupInsert(
                            ID_Login=login, ID_Unit=unit, DisplayName=y['Unit'], Email=mail+"@"+domain
                        )
                        for b in contacts['mails']:
                            if b['ID_ContactType']=="email_hlavni":
                                skautis.GoogleApps.GoogleGroupDeleteMember(
                                    ID_Login=login, ID=new_id, Email=b['Value']
                                )
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=new_id, EmailArray=b['Value']
                                )
                        new_id = skautis.GoogleApps.GoogleGroupInsert(
                            ID_Login=login, ID_Unit=unit, DisplayName="Rodiče - "+y['Unit'], Email="rodice-"+mail+"@"+domain
                        )
                        for b in contacts['mails']:
                            if b['ID_ContactType']=="email_hlavni":
                                skautis.GoogleApps.GoogleGroupDeleteMember(
                                    ID_Login=login, ID=new_id, Email=b['Value']
                                )
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=new_id, EmailArray=b['Value']
                                )


def run():
    perl = person_list(cfg['login'],cfg['unit'], False)
    idl = id_list(perl, cfg['login'])
    cnts = contacts(idl, cfg['login'])
    ggroups(cfg['login'], cfg['unit'], cnts, cfg['domain'])