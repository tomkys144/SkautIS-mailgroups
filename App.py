import yaml
from skautis import SkautisApi
with open("config.yml", "r") as config:
    cfg = yaml.load(config)


# API call
skautis = SkautisApi(appId=cfg['key'], test=True)


# person list
def person_list(login, unit, direct):
    plist = skautis.OrganizationUnit.PersonAll(ID_Login=login, ID_Unit=unit, OnlyDirectMember=direct,ID=None, ID_FunctionType=None, ID_QualificationType=None)
    return plist
