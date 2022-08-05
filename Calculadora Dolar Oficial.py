import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import tkinter

def GetData(url,token):
    hed = {'Authorization': f'BEARER {token}'}
    url = url
    response = requests.get(url, headers=hed)
    response_jason = json.loads(response.text)
    df = pd.json_normalize(response_jason)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0]).dt.date
    return df

def BlueCalculator(texto):
    fecha = texto
    fecha2 = pd.to_datetime(fecha,format='%d/%m/%Y')
    fecha2 = datetime.toordinal(fecha2)
    fecha2 = np.array(fecha2)

    token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA4OTY5MDksInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJhcm5vbmVtaWd1ZWwxQGdtYWlsLmNvbSJ9.GgyyImnK-3JrATb7hip0QweSPr0K3X3LJWQx-5pmys2X0qYtOpYxc32wokliIjfSci8_U3BDkEelG5aI3pg8Sw'
    url_dol_blue = 'https://api.estadisticasbcra.com/usd_of'
    lr_blue = GetData(url_dol_blue,token)
    years_4_before = date.today() - timedelta(days=365*4)
    lr_blue = lr_blue[lr_blue['d'] > years_4_before]
    

    # Converting date to numerical so we can make an input of it for our model
    lr_blue['fecha_numeric'] = lr_blue['d'].map(datetime.toordinal)

    # Feature and response
    X = lr_blue['fecha_numeric']
    y = lr_blue['v']

    # Fitting the model
    # ===============================================================================
    X_scaled = X.values.reshape(-1,1)
    y_scaled = y.values.reshape(-1,1)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size = 0.2, random_state=123)

    lr = LinearRegression()

    modelo = lr.fit(X_train, y_train)

    prediction = lr.predict((fecha2.reshape(-1,1)))

    return round(prediction[0][0],2)

# Inicio la ventana
ventana = tkinter.Tk()
ventana.geometry('240x100')

# Primer titulo
titulo = tkinter.Label(ventana, text = 'Ingresa una fecha dd/mm/aaaa')
titulo.grid(row = 0, column = 0)

# Caja de texto para ingresar la fecha
cajaTexto = tkinter.Entry(ventana)
cajaTexto.grid(row = 1, column = 0)

# Capturo el valor de la caja de texto y realizo el calculo con la funcion BlueCalculator
def textoDeLaCaja():
    texto = cajaTexto.get()
    resultado = BlueCalculator(texto)
    etiqueta['text'] = resultado

# Segundo titulo
titulo2 = tkinter.Label(ventana, text = 'El valor del dolar oficial sera')
titulo2.grid(row = 2, column = 0)

# Respuesta final (valor del dolar)
etiqueta = tkinter.Label(ventana)
etiqueta.grid(row = 3, column = 0)

# Boton para calcular -> con la funcion de textoDeLaCaja asignado
boton1 = tkinter.Button(ventana, text='calcula', command = textoDeLaCaja)
boton1.grid(row = 1, column = 1)

ventana.mainloop()