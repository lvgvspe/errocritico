import pycep_correios
from geopy.geocoders import Nominatim

# R. Dragão do Mar, 81 - Praia de Iracema, Fortaleza - CE, 60060-390
endereco = pycep_correios.get_address_from_cep('75071710')

geolocator = Nominatim(user_agent="test_app")
#location = geolocator.geocode("Rua PP 10, Anápolis - Parque dos Pirineus")
location = geolocator.geocode(endereco['logradouro'].split('-')[0] + ", " + endereco['bairro'] + ", " + endereco['cidade'])

print(location)
#print(location.latitude, location.longitude)