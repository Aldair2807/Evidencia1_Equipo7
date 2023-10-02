from datetime import datetime
import re
import csv
import os
import ast

notasDict = []  # MANEJAR LOS DATOS EN CONSOLA, ES DECIR, INTERNAMENTE
notasDict_OUT = []  # MANEJAR DATOS EN EXCEL, ES DECIR, EXTERNAMENTE (DICCIONARIO

recuperar = []
folios = []
adquiridosFinal = {}
listaRFC = {}

fechaActual1 = datetime.today()
fechaActual = datetime.strftime(fechaActual1, '%d/%m/%Y')
fechaHoy = datetime.strptime(fechaActual, '%d/%m/%Y')

'''
ESTRUCTURA DE notasDict

notasDict = [(folio, fecha que ingresa usuario, cliente, total a pagar, {folio: [(servicio, costo)]}, RFC_Cliente, correo)]
---------------------------------------------------------------------------------------------------------------------------

ESTRUCTURA DE notasDict_OUT

notasDict_OUT = [
    {
    'folio': notasDict[0], 
    'fecha': notasDict[1], 
    'cliente': notasDict[2], 
    'total': notasDict[3], 
    'servicio': notasDict[4][0], 
    'costo': notasDict[4][1], 
    'rfc': notasDict[5], 
    'correo': notasDict[6]
    }
    
Para lograr guardar un diccionario por cada cliente:
    cont = 0
    for i in notasDict:
        notasDict_OUT.append(
            {
            'folio': notasDict[0], 
            'fecha': notasDict[1], 
            'cliente': notasDict[2], 
            'total': notasDict[3], 
            'servicio': notasDict[4][0], 
            'costo': notasDict[4][1], 
            'rfc': notasDict[5], 
            'correo': notasDict[6]
            }

    cont2 = 0
    for i in recuperar:
        notasDict_OUT.append(
            {
            'folio': notasDict[0], 
            'fecha': notasDict[1], 
            'cliente': notasDict[2], 
            'total': notasDict[3], 
            'servicio': notasDict[4][0], 
            'costo': notasDict[4][1], 
            'rfc': notasDict[5], 
            'correo': notasDict[6]
            }
'''

archivo_csv = 'notasDict.csv'

# Verificar si el archivo existe
if os.path.isfile(archivo_csv):
    # Si el archivo existe, leer los datos desde el archivo CSV
    datos_leidos = []
    with open(archivo_csv, mode='r') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)

        for fila in lector_csv:
            datos_leidos.append(fila)
            #fila['fecha'] = datetime.datetime(fila['fecha'])
            #fila['servicios'] = list(fila['servicios'])
            folio = int(fila['folio'])
            fecha = fila['fecha']
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            cliente = fila['cliente']
            total = float(fila['total'])
            servicios = fila['servicios']
            servicios = ast.literal_eval(servicios)
            rfc = fila['rfc']
            correo = fila['correo']
            notasDict.append((folio,fecha,cliente,total,servicios,rfc,correo))
            for i in notasDict:
                adquiridosFinal[folio] = servicios





    # Imprimir "Se han cargado los datos"
    print("Se han cargado los datos")

else:
    # Si el archivo no existe, imprimir un mensaje indicando que no se encontraron datos
    print("No hay datos en memoria. Iniciando desde cero.")

def cancelarFolio():
    global fechaHoy, folio, fechaUsuario
    global fecha_str, cliente, montoPagar, adquiridos, costo  # diccionario main
    global adquiridosFinal
    global consultaFolio
    global servicio, recuperar

    while True:
        try:
            print("Ingrese el folio de la nota a cancelar.")
            elige = int(input("->"))
            if elige == 0: break
            for i in notasDict:
                if i[0] == elige:
                    fecha_formateada = datetime.strftime(i[1], "%d/%m/%Y")
                    print(f"\nFolio: {i[0]}")
                    print(f"Fecha: {fecha_formateada}")
                    print(f"Cliente: {i[2]}")
                    print(f"RFC: {i[5]}")
                    print(f"Correo: {i[6]}")
                    print(f"Monto a pagar: ${i[3]}")
                    print("Servicios:")
                    for i in adquiridosFinal[i[0]]:
                        print(f"\t- {i[0]} ---- ${i[1]}")

                    while True:
                        respuesta = int(input("\n¿Está seguro que desea cancelar la nota? / (1) Si  /  (2) No\n->"))

                        if respuesta not in (1, 2):
                            print("Escriba 1 o 2, según sea el caso.")
                            continue
                        elif respuesta == 2:
                            print("No se canceló la nota.")
                            break
                        elif respuesta == 1:
                            print(f"Se canceló la nota.")
                            cont = 0
                            for i in notasDict:
                                if i[0] == elige:
                                    notasDict.pop(cont)
                                    recuperar.append(i)
                                else:
                                    cont += 1
                            break

                    menu()
        except Exception as e:
            print("No existe el folio indicado en el sistema.", e)


def recuperarnota():
    global notasDict, recuperar
    if len(recuperar) == 0:
        print("No hay notas para recuperar.")
        menu()
    try:
        while True:
            print("FOLIO\t\t\tFECHA\t\t\t\t\tCLIENTE\t\t\tTOTAL A PAGAR")
            for i in recuperar:
                fecha_str = datetime.strftime(i[1], '%Y/%m/%d')
                print(f"{i[0]}\t\t\t{fecha_str}\t\t\t\t{i[2]}\t\t\t{i[3]}")
            break

        print("\nIngrese el número de folio a recuperar (Vacio para regresar al menu):")
        folio_recuperar = int(input("->"))
        if str(folio_recuperar).strip() == "": menu()

        nota_recuperada = None  # nota_recuperada como None

        f_n1 = False
        for nota in recuperar:
            if nota[0] == folio_recuperar:
                nota_recuperada = nota
                f_n1 = True
                '''
                IMPRIMIR TODOS LOS SERVICIOS REALIZADOS
                '''
                print("*************************************")
                for i in recuperar:
                    print("Servicios:")
                    for i in adquiridosFinal[i[0]]:
                        print(f"\t- {i[0]} ---- ${i[1]}")
                print("*************************************")

                while True:
                    resp = int(input("\nElija: 1- Confirmar / 2- Cancelar operación.\n->"))
                    if not resp in (1, 2):
                        continue
                    elif resp == 1:
                        if nota_recuperada:
                            notasDict.append(nota_recuperada)
                            cont = 0
                            for i in recuperar:
                                if i[0] == folio_recuperar:
                                    recuperar.pop(cont)
                                else:
                                    cont += 1
                            print("Nota recuperada con éxito.")
                            break
                        else:
                            print("No se encontró ninguna nota con el folio introducido.")
                    else:
                        print("No se recuperó la nota.")
                        menu()

            if not f_n1:
                print("******")
                print("No existe ese folio en el sistema. Ingrese uno válido.")
                print("******")
                recuperarnota()

    except ValueError:
        print("Regresando...")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    menu()

def consultaCliente():
    global notasDict, listaRFC

    serviciosXcliente = []
    j = 1
    for i in notasDict:
        fechaFormato = i[1].strftime("%d/%m/%Y")
        rfcCliente = i[5]
        listaRFC[f"{rfcCliente}"] = j
        j += 1

    keys = listaRFC.keys()
    sorted_keys = sorted(keys)
    rfc_ordenados = {}
    for key in sorted_keys:
        rfc_ordenados[key] = listaRFC[key]

    flag = False
    for i in notasDict:
        if i[5] in rfc_ordenados:
            flag = True
            break  # Rompe el bucle cuando se encuentra una coincidencia

    if flag:
        print("***************")
        for clave, valor in rfc_ordenados.items():
            print(f"RFC: {clave}\tFolio: {valor}")
        print("***************")
    if not flag:
        print("No hay datos.")
        consultas()

    while True:
        try:
            print("\nIngresa el folio a consultar. ('X' para ir al menú)")
            consultaFolio = input("->")
            if consultaFolio in ("x", "X"):
                menu()
        except Exception:
            print("Ingrese una opcion correcta.")
            consultaXfolio()

        consultaFolio = int(consultaFolio)
        existeFolio = False
        print("\n***************")
        for k in notasDict:
            if k[0] == consultaFolio:
                existeFolio = True
                fechaAsignada = datetime.strftime(k[1], '%d-%m-%Y')
                print(f"Folio: {k[0]}")
                _folio = k[0]
                print(f"Fecha: {fechaAsignada}")
                print(f"Cliente: {k[2]}")
                _cliente = k[2]
                print(f"RFC: {k[5]}")
                _rfc = k[5]
                print(f"Correo: {k[6]}")
                _correo = k[6]
                print(f"Monto a pagar: ${k[3]}")
                _total = k[3]
                print("Servicios:")
                for i in adquiridosFinal[k[0]]:
                    print(f"\t- {i[0]} ---- ${i[1]}")
                    serviciosXcliente.append((i[0], i[1]))
                print("***************")
                print("")
        if not existeFolio:
            print(f"No existe el folio {consultaFolio}")
            consultaFolio = 0

        confirmacion = input("¿Desea exportar la información a un archivo de Excel? (1) Si // (2) No)\n->")
        if confirmacion == "1":
            # Preservar el estado de la aplicación mediante un archivo CSV
            with open(f"{k[5]}_{fechaAsignada}.csv", "w") as archivo:
                # Escribir el estado de la aplicación en el archivo CSV
                archivo.write(f"{_folio, fechaAsignada, _cliente, _total, serviciosXcliente, _rfc, _correo}")

            target = f"{k[5]}_{fechaAsignada}.csv"
            initial_dir = 'C:\\'

            path = ''
            for root, _, files in os.walk(initial_dir):
                if target in files:
                    path = os.path.join(root, target)
                    break
            print("*********************************")
            print("Exportación completada con exito.")
            print(f"La ruta del archivo es: ", path, "\n")
            print("*********************************")
        break
    consultaCliente()


def consultaXfolio():
    global fechaHoy, folio, fechaUsuario
    global fecha_str, cliente, montoPagar, adquiridos, costo  # diccionario main
    global adquiridosFinal
    global consultaFolio

    global servicio

    while True:
        try:
            print("Ingresa el folio a consultar")
            consultaFolio = int(input("->"))
        except Exception:
            print("Ingrese una opcion correcta.")
            consultaXfolio()

        existeFolio = False
        for k in notasDict:
            if k[0] == consultaFolio:
                existeFolio = True
                fechaAsignada = datetime.strftime(k[1], '%d/%m/%Y')
                print(f"\nFolio: {k[0]}")
                print(f"Fecha: {fechaAsignada}")
                print(f"Cliente: {k[2]}")
                print(f"RFC: {k[5]}")
                print(f"Correo: {k[6]}")
                print(f"Monto a pagar: ${k[3]}")
                print("Servicios:")
                for i in adquiridosFinal[k[0]]:
                    print(f"\t- {i[0]} ---- ${i[1]}")

        if not existeFolio:
            print(f"No existe el folio {consultaFolio}")
            consultaFolio = 0
        break
    menu()


def consultas():
    global fechaHoy, folio, fechaUsuario
    global fecha_str, cliente, montoPagar, adquiridos, costo  # diccionario main
    global adquiridosFinal
    global servicio

    while True:
        try:
            elige = int(
                input("\n(1) Consulta por periodo\n(2) Consulta por folio\n(3) Consulta por cliente\n(4) Regresar\n->"))
            if not elige in (1, 2, 3, 4):
                continue
            elif elige == 1:
                break
            elif elige == 2:
                consultaXfolio()
            elif elige == 3:
                consultaCliente()
            elif elige == 4:
                menu()
        except Exception as e:
            print("Ingrese un valor correcto.", e)
        break

    while True:
        try:
            # Solicitar las fechas de inicio y fin al usuario
            inicio_str = input(
                "Ingrese la fecha de inicio en el formato dd/mm/aaaa. (Indique 0 para regresar al menu de consultas)\n-> ")
            if inicio_str == "":
                inicio_str = "01/01/2000"  # Formato: año, mes, día
                print("La fecha de inicio se asignó autommáticamente a: 01/01/2000")

            if inicio_str in ("0", "00", "000", "0000"):
                consultas()

            fin_str = input("Ingrese la fecha de fin en el formato dd/mm/aaaa\n-> ")
            if fin_str == "":
                fin_str = str(fechaActual)

                fechaFormato = fechaHoy.strftime("%d/%m/%Y")
                print(f"La fecha fin se asignó automáticamente a: {fechaHoy}")

            if fin_str in ("0", "00", "000", "0000"):
                consultas()

            inicio = datetime.strptime(inicio_str, '%d/%m/%Y')
            # inicio = inicio.strftime("%d/%m/%Y")
            fin = datetime.strptime(fin_str, '%d/%m/%Y')
            # fin = fin.strftime("%d/%m/%Y")

            Existe = False
            for j in notasDict:
                if j[1] >= inicio and j[1] <= fin:
                    print("*******************************************")
                    Existe = True
                    fecha_formateada = j[1]
                    fecha_formateada = fecha_formateada.strftime("%d/%m/%Y")
                    print(f"\nFolio: {j[0]}")
                    print(f"Fecha: {fecha_formateada}")
                    print(f"Cliente: {j[2]}")
                    print(f"RFC: {j[5]}")
                    print(f"Correo: {j[6]}")
                    print(f"Monto a pagar: ${j[3]}")
                    print("Servicios:")
                    for i in adquiridosFinal[j[0]]:
                        print(f"\t- {i[0]} ---- ${i[1]}")
            print("\n*******************************************")
            if not Existe:
                print("*******************************************")
                print("No existe ninguna nota dentro del rango proporcionado.")
                print("*******************************************")
                continue
        except AttributeError as r:
            print("Error al buscar por fechas.", r)
        else:
            break


def registro():
    global fechaHoy, folio, fechaUsuario
    global fecha_str, cliente, montoPagar, adquiridos, costo  # diccionario main
    global adquiridosFinal
    global RFC_Cliente, correo
    global servicio

    adquiridos = []

    print("╔═══════════════════════════════════╗")
    print("║             REGISTRO              ║")
    print("║═══════════════════════════════════║")
    print("╚═══════════════════════════════════╝")
    while True:
        try:
            print("Ingresa la fecha de registro. Formato (DD/MM/AAAA)")
            fecha_str = input("->")
            if fecha_str.strip() == "":
                print("**********************\nFecha no válida. Vuelva a intentarlo.\n**********************")
                continue
            fechaUsuario = datetime.strptime(fecha_str, '%d/%m/%Y')
            if fechaUsuario > fechaHoy:
                print(
                    f"**********************\nIngrese una fecha hasta {fechaHoy}. No debe ser "
                    f"posterior.\n**********************")
                continue
            else:
                folio = 1
                while True:
                    if folio in folios:
                        folio += 1
                        continue
                    else:
                        folios.append(folio)
                        break
                while True:
                    cliente = input("Ingrese su nombre: ").capitalize()
                    if cliente.strip() == "":
                        print("**********************\nNo deje vacio su nombre.\n**********************")
                        continue
                    else:
                        break
                while True:
                    RFC_Cliente = input("Ingresa tu RFC->")
                    RFC_Cliente = RFC_Cliente.upper()
                    if not bool(re.match("[A-Z]{4}[0-9]{6}[A-Z0-9]{3}", RFC_Cliente)):
                        print("Formato incorrecto o incompleto. Ingrese nuevamente.")
                        continue
                    else:
                        break
                while True:
                    correo = input("Ingresa tu correo->")
                    patron = r'[\w\._\-\d]+@(gmail|hotmail|outlook|yahoo|uanl|live)\.[a-z]{1,2}'
                    if not bool(re.match(patron, correo.lower())):
                        print("Formato incorrecto o incompleto. Ingrese nuevamente.")
                        continue
                    else:
                        break
                while True:
                    servicio = input("¿Que servicio va a realizar?: ")
                    if servicio.strip() == "":
                        print("**********************\nNo deje vacio el campo de servicio.\n**********************")
                        continue
                    while True:
                        try:
                            costo = input("¿Cual es el costo del servicio?: ")
                        except Exception:
                            continue
                        if costo.strip() == "":
                            print(
                                "**********************\nNo debe dejar vacio y deberá ser número entero o "
                                "decimal. Intenta de nuevo.\n**********************")
                            continue
                        elif float(costo) < 0:
                            print(
                                "**********************\nNo debe ser negativo. Vuelva a "
                                "intentarlo.\n**********************")
                            continue

                        patron_decimales = r'^\d+(\.\d{1,2})?$'
                        if not bool(re.match(patron_decimales, costo)):
                            print("No debe tener mas de dos decimales. Intente nuevamente.")
                            continue

                        break

                    montoPagar += float(costo)
                    adquiridos.append((servicio.capitalize(), costo))

                    masServicios = input("¿Adquirir mas servicios? 1. Si / 2. No\n->")

                    if masServicios == "1":
                        continue
                    elif masServicios == "2":
                        print("Nota creada con éxito.")
                        adquiridosFinal[folio] = adquiridos
                        break
                notasDict.append(
                    (folio, fechaUsuario, cliente, montoPagar, adquiridosFinal[folio], RFC_Cliente, correo))

        except Exception:
            print(
                "**********************\nError en la ejecucion de su solicitud. Intente de "
                "nuevo.\n**********************")

        menu()


def menu():
    global fecha_str, cliente, montoPagar, adquiridos, folio, adquiridos, costo, recuperar, RFC_Cliente, correo
    global notasDict, notasDict_OUT
    while True:
        try:
            print(
                f"\n\t<--- TALLER MECANICO --->\n1. Registrar nota\n2. Consulta y reportes\n3. Cancelar nota\n4. "
                f"Recuperar nota\n5. Salir")
            opcion = int(input("->"))
            if opcion == 1:

                fecha_str = ""
                cliente = ""
                montoPagar = 0
                adquiridos = []
                folio = 0
                costo = 0
                RFC_Cliente = ""
                correo = ""
                registro()
            elif opcion == 2:
                consultas()
            elif opcion == 3:
                cancelarFolio()
            elif opcion == 4:
                recuperarnota()
            elif opcion == 5:
                resp = int(input("¿Seguro que quiere salir? 1-Si / 2-No\n->"))
                if resp not in (1, 2):
                    menu()
                elif resp == 1:
                    print("********************** Saliendo... **********************")

                    for i in notasDict:
                        diccionario = {
                                'folio': i[0],
                                'fecha': i[1],
                                'cliente': i[2],
                                'total': i[3],
                                'servicios': (i[4]),
                                'rfc': i[5],
                                'correo': i[6]
                            }
                        notasDict_OUT.append(diccionario)
                        print(i)


                    with open('notasDict.csv', mode='w', newline='') as archivo_csv:
                        campos = ['folio', 'fecha', 'cliente', 'total', 'servicios', 'rfc', 'correo']
                        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)

                        escritor_csv.writeheader()
                        for dato in notasDict_OUT:
                            escritor_csv.writerow(dato)

                    exit()
                elif resp == 2:
                    menu()
        except IndexError as e:
            print("Error, favor de intentar de nuevo.", e)


menu()
