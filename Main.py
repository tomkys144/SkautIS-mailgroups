from skautis import SkautisApi

#Volání Api
from .Config import APIKEY
skautis = SkautisApi(APIKEY, test=True)

from .Person_list import person_list

print(person_list(APIKEY))