#Volání API
from skautis import SkautisApi

skautis = SkautisApi("APIKEY")

from Person_list import person_list
print(person_list("APIKEY"))