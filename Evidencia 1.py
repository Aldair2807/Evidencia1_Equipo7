import random as r
from datetime import datetime

fechaHoy = datetime.today()

notasDict = []
recuperar = []
'''
ESTRUCTURA DE notasDict

notasDict = [(folio, fecha que ingresa usuario, cliente, total a pagar, {folio: [(servicio, costo)]})]
'''
folios = []
adquiridosFinal ={}

def consultaXfolio():
    global fechaHoy, folio, fechaUsuario
    global fecha_str, cliente, montoPagar, adquiridos, costo  # diccionario main
    global adquiridosFinal
    global consultaFolio

    global servicio

    while True:
        try:
            print("Ingresa el folio a consultar")
            consultaFolio=int(input("->"))
        except Exception:
            print("Ingrese una opcion correcta.")

        for k in notasDict:
            if k[0]==consultaFolio:
                print(f"\nFolio: {k[0]}")
                print(f"Fecha: {k[1]}")
                print(f"Cliente: {k[2]}")
                print(f"Monto a pagar: {k[3]}")
                print("Servicios:")
                for i in adquiridosFinal[k[0]]:
                    print(f"\t- {i[0]} ---- ${i[1]}")
        break
    menu()
