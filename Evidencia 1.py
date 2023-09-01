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


def consultas():
    global fechaHoy, folio, fechaUsuario
    global fecha_str, cliente, montoPagar, adquiridos, costo  # diccionario main
    global adquiridosFinal

    global servicio

    while True:
        try:
            elige = int(input("\n(1) Consulta por folio\n(2) Consulta por rango de fechas.\n->"))
            if not elige in (1, 2):continue
            elif elige==1: consultaXfolio()
        except Exception:
            print("Ingrese un valor correcto.")
        break


    while True:
        try:
            for j in notasDict:
                # Solicitar las fechas de inicio y fin al usuario
                inicio_str = input("Ingrese la fecha de inicio en el formato aaaa/mm/dd (Vacio para regresar)\n-> ")
                if inicio_str == "":
                    print("Regresando...")
                    continue

                fin_str = input("Ingrese la fecha de fin en el formato aaaa/mm/dd (Vacio para regresar)\n-> ")
                if fin_str == "":
                    print("Regresando...")
                    continue

                inicio = datetime.strptime(inicio_str, '%Y/%m/%d')
                fin = datetime.strptime(fin_str, '%Y/%m/%d')

                Existe=False
                if j[1]>=inicio and j[1]<=fin:
                    Existe=True
                    print(f"\nFolio: {j[0]}")
                    print(f"Fecha: {j[1]}")
                    print(f"Cliente: {j[2]}")
                    print(f"Monto a pagar: {j[3]}")
                    print("Servicios:")
                    for i in adquiridosFinal[j[0]]:
                        print(f"\t- {i[0]} ---- ${i[1]}")
                if not Existe:
                    print("No existe ningun dato dentro del rango proporcionado.")
                    continue


        except Exception:
            print("Error al buscar por fechas.")
        else: break
