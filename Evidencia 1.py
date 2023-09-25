from datetime import datetime
import re
import csv
def cargar_datos_csv():
    try:
        with open('notasDict.csv', 'r') as archivocsv:
            reader = csv.DictReader(archivocsv)
            for fila in reader:
                # Convierte los valores a los tipos adecuados (por ejemplo, fecha y total a flotante)
                fila['folio'] = int(fila['folio'])
                fila['fecha'] = datetime.strptime(fila['fecha'], '%d/%m/%Y')
                fila['total'] = float(fila['total'])
                fila['servicios'] = eval(fila['servicios'])
                notasDict.append(fila)

        with open('recuperar.csv', 'r') as archivocsv:
            reader = csv.DictReader(archivocsv)
            for fila in reader:
                # Convierte los valores a los tipos adecuados (por ejemplo, fecha y total a flotante)
                fila['folio'] = int(fila['folio'])
                fila['fecha'] = datetime.strptime(fila['fecha'], '%d/%m/%Y')
                fila['total'] = float(fila['total'])
                fila['servicios'] = eval(fila['servicios'])
                recuperar.append(fila)

        print("Datos cargados desde archivos CSV existentes.")
    except Exception as e:
        print("No se encontraron archivos CSV existentes. Comenzando desde un estado vacío.", e)

cargar_datos_csv()

fechaActual1 = datetime.today()
fechaActual = datetime.strftime(fechaActual1, '%d/%m/%Y')
fechaHoy = datetime.strptime(fechaActual, '%d/%m/%Y')

notasDict = []
recuperar = []
folios = []
adquiridosFinal = {}

listaRFC =  []
'''
ESTRUCTURA DE notasDict

notasDict = [(folio, fecha que ingresa usuario, cliente, total a pagar, {folio: [(servicio, costo)]}, RFC_Cliente, correo)]
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
            elige = int(input("->"))
            if elige==0: break
            for i in notasDict:
                if i[0] == elige:
                    print(f"\nFolio: {i[0]}")
                    print(f"Fecha: {i[1]}")
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
        except Exception:
            print("No existe el folio indicado en el sistema.")


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

'''


REALIZAR REPORTE TABULAR CON INFORMACION DE NOTASDICT.



'''
def consultaCliente():
    global notasDict, listaRFC
    print("FOLIO\t\t\tFECHA\t\tCLIENTE\t\t\t\tRFC\t\tCORREO\t\t\t\tMONTO A PAGAR")
    for i in notasDict:
        fechaFormato = i[1].strftime("%d/%m/%Y")
        print(f"{i[0]}\t\t\t{fechaFormato}\t\t\t{i[2]}\t\t\t{i[5]}\t{i[6]}\t\t\t{i[3]}")


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
            elige = int(input("\n(1) Consulta por periodo\n(2) Consulta por folio\n(3) Consulta por cliente\n(4) Regresar\n->"))
            if not elige in (1, 2, 3):
                continue
            elif elige == 2:
                consultaXfolio()
            elif elige==3:
                consultaCliente()
            elif elige == 4:
                menu()
        except Exception:
            print("Ingrese un valor correcto.")
        break

        while True:
            try:
                    # Solicitar las fechas de inicio y fin al usuario
                    inicio_str = input("Ingrese la fecha de inicio en el formato dd/mm/aaaa. (Indique 0 para regresar al menu de consultas)\n-> ")
                    if inicio_str == "":
                        inicio_str = "01/01/2000"  # Formato: año, mes, día
                        print("La fecha de inicio se asignó autommáticamente a: 01/01/2000")

                    if inicio_str in ("0","00","000","0000"):
                        consultas()

                    fin_str = input("Ingrese la fecha de fin en el formato dd/mm/aaaa\n-> ")
                    if fin_str == "":
                        fin_str = str(fechaActual)

                        fechaFormato = fechaHoy.strftime("%d/%m/%Y")
                        print(f"La fecha fin se asignó autommáticamente a: {fechaHoy}")

                    if fin_str in ("0","00","000","0000"):
                        consultas()

                    inicio = datetime.strptime(inicio_str, '%d/%m/%Y')
                    #inicio = inicio.strftime("%d/%m/%Y")
                    fin = datetime.strptime(fin_str, '%d/%m/%Y')
                    #fin = fin.strftime("%d/%m/%Y")

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
                            print("*******************************************")
                    if not Existe:
                        print("*******************************************")
                        print("No existe ningun dato dentro del rango proporcionado.")
                        print("*******************************************")
                        continue
            except Exception:
                print("Error al buscar por fechas.")
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
                    if not bool(re.match("[A-Z]{4}[0-9]{6}[A-Z]{2}[0-9]{1}", RFC_Cliente)):
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
                        costo = input("¿Cual es el costo del servicio?: ")
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
                        print(adquiridosFinal)
                        break
                notasDict.append((folio, fechaUsuario, cliente, montoPagar, adquiridosFinal[folio], RFC_Cliente, correo))

        except Exception:
            print(
                "**********************\nError en la ejecucion de su solicitud. Intente de "
                "nuevo.\n**********************")
        else:

            g = 1
            print()
            for i in notasDict:
                fecha_str2 = datetime.strftime(i[1], '%d/%m/%Y')
                print("----------------------------------------")
                print(f"Nota: {g}")
                print(f"Fecha: {fecha_str2}")
                print(f"Cliente: {i[2]}")
                print(f"Monto a pagar: ${i[3]}")
                print(f"Servicios:")

                h = 0
                for k in notasDict:
                    if k[h] == g:
                        for i in adquiridosFinal[k[0]]:
                            print(f"\t- {i[0]} ---- ${i[1]}")
                        h += 1
                g += 1
            print("----------------------------------------")

            menu()

def guardar_datos_csv():
    with open('notasDict.csv', 'w', newline='') as archivocsv:
        campo_nombres = ['folio', 'fecha', 'cliente', 'total', 'servicios', 'RFC', 'correo']
        writer = csv.DictWriter(archivocsv, fieldnames = campo_nombres)

        writer.writeheader()
        for nota in notasDict:
            writer.writerow({
                'folio': nota[0],
                'fecha': nota[1].strftime('%d/%m/%Y'),
                'cliente': nota[2],
                'total': nota[3],
                'servicios': str(nota[4]),
                'RFC': nota[5],
                'correo': nota[6]
            })

    with open('recuperar.csv', 'w', newline='') as archivocsv:
        campo_nombres = ['folio', 'fecha', 'cliente', 'total', 'servicios', 'RFC', 'correo']
        writer = csv.DictWriter(archivocsv, fieldnames=campo_nombres)

        writer.writeheader()
        for nota in recuperar:
            writer.writerow({
                'folio': nota[0],
                'fecha': nota[1].strftime('%d/%m/%Y'),
                'cliente': nota[2],
                'total': nota[3],
                'servicios': str(nota[4]),
                'RFC': nota[5],
                'correo': nota[6]
            })


def menu():
    global fecha_str, cliente, montoPagar, adquiridos, folio, adquiridos, costo, recuperar, RFC_Cliente, correo
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
                    exit()
                elif resp == 2:
                    menu()
        except Exception:
            print("Error, favor de intentar de nuevo.")


menu()
