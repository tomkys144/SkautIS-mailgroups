from skautis import SkautisApi


# API call
from .Config import key

skautis = SkautisApi(appId=key, test=True)


# children units IDs
unit_id = int()


def unit_ids():
    from .Config import login
    from .Config import unit
    units_id = skautis.OrganizationUnit.UnitAllUnit(ID_Login=login, ID_Unit=unit)
    return units_id


# list
def person_list():
    from .Config import login
    plist = skautis.OrganizationUnit.PersonAllExport(ID_Login=login, ID_Unit=unit_id)
    return plist
