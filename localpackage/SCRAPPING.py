# Import Meteostat library and dependencies

from datetime import datetime
from dateutil.deltatime import deltatime
from meteostat import Point, Daily
import localpackage.modified_ozone as ooo
import pandas as pd
import localpackage.fetch_city as fc
from citipy import citipy

#API key AQICN
o3 = ooo.Ozone('d8a099d2492a444219a00713bddafb693699c53f')

#obtener las coordenadas elegidas en tableau en el point location
def obtain_params():
    sheet_id = '1rjx1D0tLXRb3c01ezuaQwfi2LAq5ybR1R1el9V1anMM'
    sheet_name = 'areaverde'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    a=pd.read_csv(url)
    lat=a['lat'][0]
    lon=a['lon'][0]
    especiedict={'area': a['area'][1],a['especie1'][1]:a['especie1'][2],a['especie2'][1]:a['especie2'][2],a['especie3'][1]:a['especie3'][2]}
    return lat, lon, especiedict
def point(latitud, longitud):
    location = Point(latitud, longitud)
    city=o3.get_city_id(latitud,longitud)
    return location, city
#obtener la poblacion
def population_data(latitud, longitud):
    city = citipy.nearest_city(latitud, longitud).city_name
    if city== 'new york':
        city='New York City'
    data=fc.obtain_data(city)[0]
    return data
#obtener la fecha actual
def date():
    end = datetime.today()
    end = end.replace(hour=0, minute=0, second=0, microsecond=0)
    start = end- relativedelta(years=1)
    return start, end
#obtener datos diarios del último año
def last_year_weather(latitud,longitud):
    start=date()[0]
    end=date()[1]
    location = point(latitud,longitud)[0]
    data = Daily(location, start, end)
    data = data.fetch().drop(['tmin','tmax','snow','wdir','wpgt','pres','tsun'], axis=1)
    data=data[['wspd','prcp','tavg']]
    return data

def historical_Ct(latitud,longitud):
    city=point(latitud, longitud)[1]
    data = o3.get_historical_data(city_id=city)
    return data
def get_data(latitud,longitud):
    df=last_year_weather(latitud,longitud)
    start=date()[0]
    end=date()[1]
    rawdata=historical_Ct(latitud,longitud).fillna(method='ffill').fillna(method='bfill')
    Ct=rawdata['pm25']
    data=pd.concat([df,Ct],axis=1).fillna(method='ffill').fillna(method='bfill')[start:end]
    data=data[['wspd','prcp','pm25','tavg']]
    return data
def get_city_emission(latitud,longitud):
    city= list(population_data(latitud, longitud))
    contrydict=pd.read_csv('localpackage/Emission_inventory.csv', sep=';').set_index('Pais').T.to_dict('list')
    dict={}
    name=city[0]
    Chab=float(city[1])
    pais=city[4]
    Et=contrydict[pais][0]
    Et=float(Et.replace(',','.'))
    hab=float(city[5])
    Ehab=Et/hab
    Ecity=Ehab*Chab
    dict[name]=Ecity
    return dict, name
