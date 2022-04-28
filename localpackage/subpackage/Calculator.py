from localpackage.SCRAPPING import get_city_emission, get_data, obtain_params
import pandas as pd
import gspread
def execute():
    Vd=''
    Ct=''
    At=''
    At_1=''
    R=''
    latitud= obtain_params()[0]
    longitud=  	obtain_params()[1]
    get_data(latitud,longitud).to_csv('data.csv')
    documento=open('data.csv')
    documento2=open('localpackage/MainParameters.csv')
    
    #iniciar API google sheets
    credentials = {
      "type": "service_account",
      "project_id": "datatree-348017",
      "private_key_id": "0375b3f9533742012a3f3db1219dc84c15536e8f",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDEzrfyDVPruTWQ\n4tPIjE1hldmfGuRfUUpp+EKMBtd4XbxxElfAh8ZuIq4UbXRXTEZIn2UxhkFruZ61\ni29KBMwwgQQ2lt9U3i4cL0lI6KMeh0jXxGbhQsos+h2l/2nYO4O9e1Mf0Zv2O8h4\nCYvSGEIVgZzJ5YnWKc6tIy74I9lViK14JZawx+IGRa6wCk5LdyB38yWW838B1IcA\nMNjtC5vx7Ut/Mnyae/jkIyAA5U56uQsSY58NAsWyaQsZ6Jbgz0BMGMgRk20Yjd6/\nxSfOEb0+WAtkKXYHcFEgsaV91PTrKYue/jqOMy1xBwTuN/3hAGJQUGaHUpGD0LMb\ndbGqnNmzAgMBAAECggEAKfCbhnuMnLk1TxDnbN9pRhh27c7/R8i9AOQk2k5C8KWZ\nGMd958uHX8UIL9Y7arcYazV8jRc9LcW6qplyN+XZ1aRIz5FLOny2es8g4OaijEjs\nHv79pZdkGj2av9s0JR5ZrrFvP2Kdx9VpnRr7ruP4gTjDvsqpmvgB0SekRMDu+ajs\ntNLDWkt2vtDxDFLi31+xjXFt4Ti9A6bqx7uO+boCCW86fhfWRxDlT/VlNcX6qOx4\n65vCsb5GCR6Z7pXP9i0dr+MmV4oLRTpJefSWsZBFgb0/P9zBhbbyPMvhUhFswI2z\nDimXPR0th1553q1PdslrZTDq/g9B+mrSQzEuTtXPUQKBgQD1H7Ixz8BbG/LcqDBF\n/BkAxaZRUkqqvDN9otVQrru2pdf61nmxRw12GfrHGb7XpOCdnnVBjGdeL1BBVqai\ngxqeOfT3TDzxJWnQ96aRwfcbWGQs/xClR7JtdNAgfmYxSDMaGm/7/8gQOHPwoNl+\nYw0HLgsQG2GPDuvzFydvHE/pZQKBgQDNijVvRW1sjSNrwu5kzLMMk1c3bD3QH0iR\nJKM6IhDFTYbH0WivMNbgVN4pZ/1u5m6OFEWAaYel/h4fDMQ8Xg1tXxMq3qBgd7/1\nNvrBx8m0AiF0yt3ERptkiaNN+KxpfShPDzr2eAxDAgYPeoNgOAXdvnBM3zvn/mRt\nDc+bdQoRNwKBgQCs7gaN464l2KrWhwU/amHNTKNQPckVeJ6u5OCvAgbGDWw4t3S0\n35acmil0qzIa+mPIbxD0BHSsWp646cO3ZNyzgdnTWYKo8accWIq3y+pj7VEG+Y8p\nu1IirEVklyfLXs9GfB5C3ymqX9lTinbGFmULiq0dWOPTxEgrgEs+tO+fjQKBgBcs\ndvvVqxGrFAxJTRGGVsWbMyEnjgySCl967wBV6Ogl5oVO4eumqQNf7jBi7hr71gkk\n1fU1cLrRXNoJWXKo9ACZ0JJryU83ESh3i2wft2kZOGZvnPNNNqXuMsBOwjmeh9Xq\nFK7HODKx3rcODBPkHR00JHs2TA3LC82T2g1f88OfAoGACRWZSQfDegGYquRt/vq6\nxVGm3ZgeQmSTwsOW2HBYmmQiz7YzqqUZ+SRTPBdD/8X1O0Z63ohJqbaEy6FNTHwQ\n1bAkVjyZfK5ttw5tv1VIXop4zR3dj754yqyQKFSdaTno87eEV7RpVMbM9IOD8adq\naaeb1vM/w/DRc2c7QzmamTA=\n-----END PRIVATE KEY-----\n",
      "client_email": "datatree@datatree-348017.iam.gserviceaccount.com",
      "client_id": "104017387312798195807",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/datatree%40datatree-348017.iam.gserviceaccount.com"
    }
    
    
    gc = gspread.service_account_from_dict(credentials)
    
    sh = gc.open_by_key('1XdFKMIWL5kynBP_NDO7rZL6rs6yBAhMfpaAIugVuryk')
    wks=sh.worksheet('output')
    #hacer un diccionario con los datos de cada día
    n=1
    dates={}
    for line in documento:
        if n==1:
            n=0
            continue
        line=line.strip('\n')
        
        line=line.split(',')
        
        day=line[0]
        
        
        viento=float(line[1])*0.2777777778
        
        lluvia=float(line[2])
        Ct=float(line[3])
        
        dates[day]=[round(viento),lluvia,Ct]
    
    #hacer diccionario de viento y valores de Vd y R
    n=1
    valores={}
    for line in documento2:
        if n==1:
            n=0
            continue
        line=line.strip('\n')
        line= line.replace(',', '.')
        
        line=line.split(';')
        viento=int(line[0])
        Vd=float(line[1])
        R=float(line[2])
        valores[viento]=[Vd,R]
    
    #modelo de calculo de la absorción
    def calcular_amount_w_LAI(dates,LAI):
        At=0
        Abs=0
        for day in dates.keys():
            viento=dates[day][0]
            if viento not in valores.keys():
                Vd=2.11
                rr=0.23
            else:
                Vd=valores[viento][0]
                rr=valores[viento][1]
            Ct=dates[day][2]
            mm=dates[day][1]
            At_1=At
            F=Vd*Ct*3600*24
            pcp=LAI*(0.2)
            if (mm/24) >= pcp:
                At=0
                Abs+=At_1
                continue
            R=(At_1+F)*rr
            Ft=F-R
            
            At+=Ft  
        Abs+=At
        return Abs
    
    #cambios concentración
    def cambios_concentracion(Ct,tons,emitions):
        change=tons/emitions
        newCt=Ct-Ct*change
        return newCt
    #datos del parque
    areaverde=obtain_params()[2]
    n=1
    especiedict={}
    for especie in areaverde.keys():
        if especie=='area':
            total=float(areaverde[especie])
        else:
            n+=1
            porc=float(areaverde[especie])
            areaspp=porc*total
            especiedict[especie]=areaspp
            wks.update(f'E{n}',especie)
    
    #LAIdict
    dataset=open('localpackage/LAI dataset.csv')
    n=1
    LAIset={}
    for line in dataset:
        
        line=line.strip('\n')
        line=line.replace(',', '.')
        line=line.split(';')
    
        especie=line[0]
        LAI=line[1]
        LAIset[especie]=LAI
    #datos de la ciudad
    a= get_city_emission(latitud,longitud)
    cities=a[0]
    name=a[1]
    
    #calculo absorción área verde 
    tons=0  
    n=1
    for especie in especiedict.keys():
        n+=1
        area=especiedict[especie]
        LAI=float(LAIset[especie])
        Abs=calcular_amount_w_LAI(dates,LAI)     
        especieabs=LAI*Abs*area*0.000001
        wks.update(f'f{n}',especieabs)
        wks.update(f'g{n}',area)
        tons+=especieabs
    
    emitions=cities[name]
    n=0
    change= pd.DataFrame(columns=['Día','Ct','NewCt'])
    
    
    
    
    
    #update the first sheet with df, starting at cell B2. 
    
    for day in dates.keys():
        
        Ct=dates[day][2]
        newCt=cambios_concentracion(Ct, tons, emitions)
        Ct=Ct
        newCt=newCt
        change= change.append({'Día':day,'Ct':Ct, 'NewCt':newCt},ignore_index=True)
    
    wks.update([change.columns.values.tolist()] + change.values.tolist())
    wks.update('D2',name)
    return print('done')