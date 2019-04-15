import yaml
from skautis import SkautisApi
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


def ggroups(login, unit, contacts):
    group_list = skautis.GoogleApps.GoogleGroupAll(
        ID_Login=login, ID_Unit=unit, IncludeChildUnits=True, ID=None, DisplayName=None
    )
    for n in group_list:
        n.remove('Unit', 'RegistrationNumber', 'DateCreate', 'Valid', 'AliasCount')
    for x in contacts:
        for y in x['idlist']:
            for z in y['memberships']
                for a in group_list:
                    if y['unit'] == z['DisplayName']:
                        for b in contacts['mails']:
                            if b['ID_ContactType']=="email_hlavni":
                                skautis.GoogleApps.GoogleGroupDeleteMember(
                                    ID_Login=login, ID=a['ID'], Email=b['Value']
                                )
                                skautis.GoogleApps.GoogleGroupUpdateMemberEmail(
                                    ID_Login=login, ID=a['ID'], EmailArray=b['Value']
                                )
