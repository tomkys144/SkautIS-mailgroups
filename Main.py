from skautis import SkautisApi

#API call
from .Config import APIKEY

skautis = SkautisApi(APIKEY, test=True)

#list
from .Config import uni
from .Config import login

class Peli(self):
    list = skautis.OrganizationUnit.PersonAllExport(ID_Login=login, ID_Unit=uni)
    return list