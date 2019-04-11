import yaml
from skautis import SkautisApi
from array import array
with open("config.yml", "r") as config:
    cfg = yaml.load(config)


# API call
skautis = SkautisApi(appId=cfg['key'], test=True)


# children units IDs
def unit_ids():
    uids = []
    units_info = array(skautis.OrganizationUnit.UnitAllUnit(ID_Login=cfg['login'], ID_Unit=cfg['unit']))
    i = 0
    for x in units_info:
        uids[i] = x[ID]
        i = i+1
    return uids


# list
def person_list():
    plist = skautis.OrganizationUnit.PersonAllExport(ID_Login=cfg['login'], ID_Unit=unit_id)
    return plist
