from skautis import SkautisApi


# API call
from .Config import APIKEY

skautis = SkautisApi(APIKEY, test=True)


# list
def peli():
    from .Config import uni
    from .Config import login
    perlis = skautis.OrganizationUnit.PersonAllExport(ID_Login=login, ID_Unit=uni)
    return perlis
