import yaml
from skautis import SkautisApi
from array import array
with open("config.yml", "r") as config:
    cfg = yaml.load(config)


# API call
skautis = SkautisApi(appId=cfg['key'], test=True)


# person list
def person_list():
    plist = skautis.OrganizationUnit.PersonAll(ID_Login=cfg['login'], ID_Unit=cfg['unit'], OnlyDirectMember=False)
    return plist
