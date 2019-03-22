import yaml
from skautis import SkautisApi
with open("config.yml", "r") as config:
    cfg = yaml.load(config)


# API call
skautis = SkautisApi(appId=cfg['key'], test=True)


# children units IDs
unit_id = int()


def unit_ids():
    units_id = skautis.OrganizationUnit.UnitAllUnit(ID_Login=cfg['login'], ID_Unit=cfg['unit'])
    return units_id


# list
def person_list():
    plist = skautis.OrganizationUnit.PersonAllExport(ID_Login=cfg['login'], ID_Unit=unit_id)
    return plist
