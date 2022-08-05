import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def GetData(url,token):
    hed = {'Authorization': f'BEARER {token}'}
    url = url
    response = requests.get(url, headers=hed)
    response_jason = json.loads(response.text)
    df = pd.json_normalize(response_jason)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0]).dt.date
    return df

def OficialCalculator():
    fecha = input('Selecciona una fecha dd/mm/aaaa')
    fecha2 = pd.to_datetime(fecha,format='%d/%m/%Y')
    fecha2 = datetime.toordinal(fecha2)
    fecha2 = np.array(fecha2)

    token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA4OTY5MDksInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJhcm5vbmVtaWd1ZWwxQGdtYWlsLmNvbSJ9.GgyyImnK-3JrATb7hip0QweSPr0K3X3LJWQx-5pmys2X0qYtOpYxc32wokliIjfSci8_U3BDkEelG5aI3pg8Sw'
    url_dol_oficial = 'https://api.estadisticasbcra.com/usd_of'
    lr_oficial = GetData(url_dol_oficial,token)
    years_4_before = date.today() - timedelta(days=365*4)
    lr_oficial = lr_oficial[lr_oficial['d'] > years_4_before]
    

    # Converting date to numerical so we can make an input of it for our model
    lr_oficial['fecha_numeric'] = lr_oficial['d'].map(datetime.toordinal)

    # Feature and response
    X = lr_oficial['fecha_numeric']
    y = lr_oficial['v']

    # Fitting the model
    # ===============================================================================
    X_scaled = X.values.reshape(-1,1)
    y_scaled = y.values.reshape(-1,1)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size = 0.2, random_state=123)

    lr = LinearRegression()

    modelo = lr.fit(X_train, y_train)

    prediction = lr.predict((fecha2.reshape(-1,1)))

    return print(f'El valor del dolar oficial para el dia {fecha} sera de ${round(prediction[0][0],2)}')

OficialCalculator()