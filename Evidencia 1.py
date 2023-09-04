import random as r
from datetime import datetime

fechaHoy = datetime.today()

notasDict = []
recuperar = []
folios = []
adquiridosFinal ={}

'''
ESTRUCTURA DE notasDict

notasDict = [(folio, fecha que ingresa usuario, cliente, total a pagar, {folio: [(servicio, costo)]})]
'''

def cancelarFolio():
    global fechaHoy, folio, fechaUsuario
    global fecha_str, cliente, montoPagar, adquiridos, costo  # diccionario main
    global adquiridosFinal
    global consultaFolio
    global servicio, recuperar

    while True:
        try:
            print("Ingrese el folio de la nota a cancelar.")
            elige=int(input("->"))


            for i in notasDict:
                if i[0]==elige:
                    print(f"\nFolio: {i[0]}")
                    print(f"Fecha: {i[1]}")
                    print(f"Cliente: {i[2]}")
                    print(f"Monto a pagar: {i[3]}")
                    print("Servicios:")
                    for i in adquiridosFinal[i[0]]:
                        print(f"\t- {i[0]} ---- ${i[1]}")

                    while True:
                        respuesta=int(input("\n¿Está seguro que desea cancelar la nota? / (1) Si  /  (2) No\n->"))

                        if not respuesta in (1,2):
                            print("Escriba 1 o 2, según sea el caso.")
                            continue
                        elif respuesta==2:
                            print("No se borro la nota.")
                            break
                        elif respuesta==1:
                            print(f"Se borró la nota.")
                            cont=0
                            for i in notasDict:
                                if i[0]==elige:
                                    notasDict.pop(cont)
                                    recuperar.append(i)
                                else:
                                    cont+=1

                        break
                    menu()
        except Exception:
            print("No existe el folio indicado en el sistema.")

def recuperarnota():
    global notasDict, recuperar

    try:
        print("Ingrese el número de folio a recuperar :")
        folio_recuperar = int(input("->"))

        nota_recuperada = 0

        for nota in recuperar:
            if nota[0] == folio_recuperar:
                nota_recuperada = nota
                break

        if nota_recuperada:
            notasDict.append(nota_recuperada)
            print("Nota recuperada con éxito.")
        else:
            print("No se encontró ninguna nota con el folio introducido.")

    except ValueError:
        print("Error: Por favor, ingrese un número válido para el folio.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    menu()
    
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

        existeFolio=False
        for k in notasDict:
            if k[0]==consultaFolio:
                existeFolio=True
                print(f"\nFolio: {k[0]}")
                print(f"Fecha: {k[1]}")
                print(f"Cliente: {k[2]}")
                print(f"Monto a pagar: {k[3]}")
                print("Servicios:")
                for i in adquiridosFinal[k[0]]:
                    print(f"\t- {i[0]} ---- ${i[1]}")

        if not existeFolio:
            print(f"No existe el folio {consultaFolio}")
            consultaFolio=0
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


def registro():
    global fechaHoy, folio, fechaUsuario
    global fecha_str, cliente, montoPagar, adquiridos, costo  #diccionario main
    global adquiridosFinal

    global servicio

    adquiridos=[]
    print("╔═══════════════════════════════════╗")
    print("║             REGISTRO              ║")
    print("║═══════════════════════════════════║")
    print("╚═══════════════════════════════════╝")
    while True:
        try:
            print("Ingresa la fecha de registro. Formato (AAAA/MM/DD)")
            fecha_str = input("->")
            if fecha_str.strip()=="": break

            fechaUsuario = datetime.strptime(fecha_str, '%Y/%m/%d')

            if fechaUsuario>fechaHoy:
                print(f"Ingrese una fecha desde {fecha}, hacia atrás.")
                continue
            else:
                while True:
                    folio = r.randint(11111,99999)
                    if folio in folios:
                        continue
                    else:
                        folios.append(folio)
                        break
                cliente = input("Ingrese su nombre: ").capitalize()
                if cliente.strip() == "": print("No deje vacio su nombre."); continue

                while True:

                    servicio = input("¿Que servicio va a realizar?: ")
                    if servicio.strip() == "": print("No deje vacio el campo de servicio."); continue

                    try:
                        costo = float(input("¿Cual es el costo del servicio?: "))
                    except Exception:
                        print("Debe ser un numero flotante. Con decimales. Intenta de nuevo")
                    else:
                        montoPagar += costo

                    adquiridos.append((servicio.capitalize(), costo))

                    masServicios = input("¿Adquirir mas servicios? 1. Si / 2. No\n->")

                    if masServicios == "1":
                        continue
                    else:
                        adquiridosFinal[folio] = adquiridos
                        break

                notasDict.append((folio, fechaUsuario, cliente, montoPagar, adquiridosFinal[folio]))

        except:
            print("Error en la ejecucion de su solicitud. Intente de nuevo.")
        else:

            for i in notasDict:
                print(i)

            menu()

def recuperarnota():
    global notasDict, recuperar

    try:
        print("Ingrese el número de folio a recuperar :")
        folio_recuperar = int(input("->"))

        nota_recuperada = None  # nota_recuperada como None

        for nota in notasDict:
            if nota[0] == folio_recuperar:
                nota_recuperada = nota
                break

        if nota_recuperada:
            recuperar.append(nota_recuperada)
            print("Nota recuperada con éxito.")
        else:
            print("No se encontró ninguna nota con el folio introducido.")

    except ValueError:
        print("Error: Por favor, ingrese un número válido para el folio.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    menu()


def menu():
    global fecha_str, cliente, montoPagar, adquiridos, folio, adquiridos, costo
    while True:
        try:
            print(f"\n\t<--- TALLER MECANICO --->\n1. Registrar factura\n2. Consulta y reportes\n3. Cancelar\n4. Recuperar\n5. Salir")
            opcion = int(input("->"))
            if opcion == 1:

                fecha_str = ""
                cliente = ""
                montoPagar = 0
                adquiridos = []
                folio=0
                costo=0
                registro()
            elif opcion == 2:
                consultas()
            elif opcion==3:
                cancelarFolio()
            elif opcion==4:
                recuperarnota()
            elif opcion==5:
                empieza()
        except Exception:
            print("Error, favor de intentar de nuevo.")

def empieza():

    print("╔═══════════════════════════════════╗")
    print("║            BIENVENIDO             ║")
    print("║═══════════════════════════════════║")
    print("╚═══════════════════════════════════╝")


    try:
        while True:
            opcion = int(input("1. Nuevo registro.\n2.Salir del registro.\n->"))

            if not opcion in (1,2):
                continue
            if opcion==2: exit()
            menu()
            break
    except Exception:
        print("Error, favor de verificar la opcion elegida.")

empieza()
