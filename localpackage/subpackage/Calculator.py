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
      'YOUR API KEY HERE'
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
