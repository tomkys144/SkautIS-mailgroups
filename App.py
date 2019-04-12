import yaml
from skautis import SkautisApi
with open("config.yml", "r") as config:
    cfg = yaml.load(config)


# API call
skautis = SkautisApi(appId=cfg['key'], test=True)


# person list
def person_list(login, unit, direct):
    plist = skautis.OrganizationUnit.PersonAll(
        ID_Login=login, ID_Unit=unit, OnlyDirectMember=direct,ID=None, ID_FunctionType=None, ID_QualificationType=None
    )
    return plist


def id_list(person_list, login):
    idlist = []
    for x in person_list:
        units = skautis.OrganizationUnit.MembershipAllPerson(
            ID_Login=login, ID_Person=x['ID']
        )
        for y in units:
            Unit = y['Unit']
            ID_Unit = y['ID_Unit']
        idlist.append([x['ID'], Unit, ID_Unit])
    return idlist


print(person_list(cfg['login'], cfg['unit'], True))
