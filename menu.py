
import sys, sqlite3, re, os, pandas as pd, csv
from sqlite3 import Error
from datetime import datetime, timedelta
import openpyxl


base_datos = 'TALLER_MECANICO.db'
if not os.path.isfile(base_datos):
    try:
        with sqlite3.connect("TALLER_MECANICO.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS NOTAS \
            (clave INTEGER PRIMARY KEY, fecha TEXT NOT NULL, nombre_Cliente TEXT NOT NULL, rfc_cliente TEXT NOT NULL, correo_cliente TEXT NOT NULL, total REAL, cancelada INT NOT NULL);")
            if mi_cursor:
                print("Tabla NOTAS creada exitosamente")
    except Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

fechaHoy = datetime.today()

def registrar_nota():
    while True:
        print("*" * 30)
        print("Agregar una nota")
        print("*" * 30)
        try:
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT clave, nombre FROM CLIENTES;")
            listado = cursor.fetchall()
            print("Listado de clientes registrados:")
            for i, j in listado:
                print(f"Clave: {i}\tNombre: {j}")
            print("*" * 30)
            conn.close()

            try:
                clave2 = int(input("Ingresa la clave de cliente. (Vacio para regresar al menu Notas).\n>>"))
            except:
                print("Regresando al menu Notas...")
                menuNotas()
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM CLIENTES WHERE clave={clave2}")
            resultado = cursor.fetchone()
            conn.close()
            if resultado is not None:
                print("*" * 30)
                print(f"Clave: {resultado[0]}")
                print(f"Nombre: {resultado[1]}")
                print(f"RFC: {resultado[2]}")
                print(f"Correo: {resultado[3]}")
                print("*" * 30)

                clave_cliente = resultado[0]
            else:
                print("No existe el cliente con esa clave.")
                continue
        except Exception as e:
            print("Error en la captura de la clave.")
            continue

        while True:
            try:
                fechaUser = input("Ingrese la fecha con formato 'dd/mm/aaaa'\n>>")
                fechaUser = datetime.strptime(fechaUser, '%d/%m/%Y')

                if fechaUser > fecha2:
                    print("No puede ser posterior a la fecha actual.")
                    continue
                else:
                    fechaUser = datetime.strftime(fechaUser, '%d/%m/%Y')
            except:
                print("Error en la entrada de informacion (Fecha).")
                continue
            break

        conn = sqlite3.connect("TALLER_MECANICO.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(folio) FROM NOTAS;")
        folio = cursor.fetchone()
        if folio[0] is None:
            folio = 0
        else:
            folio = folio[0] + 1
        conn.commit()
        conn.close()

        while True:
            try:
                serviciosList()
                while True:
                    try:
                        clave_servicio = int(input("Ingrese la clave del servicio a realizar: "))
                        conn = sqlite3.connect("TALLER_MECANICO.db")
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM SERVICIOS WHERE clave = {clave_servicio};")
                        resultado = cursor.fetchone()
                        print(f"Se agregó: {resultado[1]}")

                        conn = sqlite3.connect("TALLER_MECANICO.db")
                        cursor = conn.cursor()
                        cursor.execute("SELECT MAX(id_nota) FROM NOTAS;")
                        id = cursor.fetchone()
                        if id[0] is None:
                            id[0] = 0
                        else:
                            id = id[0] + 1
                        conn.commit()
                        conn.close()

                        if resultado is None:
                            print("No existe esa clave de servicio. Intente de nuevo")
                            continue
                        else:
                            costo = resultado[2]
                            conn = sqlite3.connect("TALLER_MECANICO.db")
                            cursor = conn.cursor()
                            try:
                                cursor.execute(
                                    f"INSERT INTO NOTAS VALUES({id}, {folio}, '{fechaUser}', '{clave_cliente}', {clave_servicio}, {costo}, 0);")
                                conn.commit()
                            except sqlite3.Error as e:
                                print("Error al agregar la nota:", e)
                            conn.close()
                            print("*" * 30)
                            try:
                                resp = int(input("¿Agregar mas servicios? (1)Si | (2)No\n>>"))
                                if not resp in (1, 2):
                                    print("Elija una opcion correcta.")
                                    continue
                                elif resp == 1:
                                    serviciosList()
                                    continue
                                elif resp == 2:
                                    exit()
                            except Exception as e:
                                print(f"1No debe dejar vacio.{sys.exc_info()[0]}")
                                print(e)
                    except Exception as e:
                        print(f"2No debe dejar vacio.{sys.exc_info()[0]}")
                        print(e)
                        continue
                    break
            except Exception as e:
                print(f"3No debe dejar vacio.{sys.exc_info()[0]}")
                print(e)
            break
        break

def menuNotas():
    print("*" * 30)
    try:
        while True:
            op = int(input("(1) Registrar una nota."
                           "\n(2) Cancelar una nota."
                           "\n(3) Recuperar una nota."
                           "\n(4) Consultas y reportes."
                           "\n(5) Volver al menu principal.\n>>"))
            if not op in (1, 2, 3, 4, 5):
                print("No es una opcion valida.")
                continue
            elif op == 1:
                registrar_nota()
                break
            elif op == 2:
                cancelar_nota()
                break
            elif op == 3:
                recuperar_nota()
                break
            elif op == 4:
                menuConsultasYReportesNOTAS()
                break
            elif op == 5:
                menu_principal()
                break
    except Exception as e:
        print("No es una opcion valida!")
        menuNotas()

def serviciosList():
    print("*" * 30)
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM SERVICIOS")
    resultado = cursor.fetchall()
    conn.close()
    print("*" * 30)
    for i in resultado:
        print(f"Clave: {i[0]}\t-- {i[1]}\tCosto: ${i[2]}")
    print("*" * 30)

def cancelar_nota():
    folio_cancelar = int(input("Ingresa el folio de la nota a cancelar\n>>"))
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM NOTAS WHERE folio={folio_cancelar} AND cancelada = 0;')
    resultado = cursor.fetchone()
    if resultado is None:
        print("*" * 30)
        print("No está disponible ese folio o fue cancelado con anterioridad.")
        print("*" * 30)
        cancelar_nota()
    else:
        cursor.execute(
            f'SELECT folio, fecha, clave_cliente, clave_servicio, SUM(total) FROM NOTAS WHERE cancelada = 0 AND folio = {folio_cancelar};')
        nota = cursor.fetchone()
        cursor.execute(f'SELECT nombre FROM CLIENTES WHERE clave={nota[2]}')
        nombre = cursor.fetchone()
        print("*" * 30)
        print(f"Folio: {nota[0]}")
        print(f"Fecha: {nota[1]}")
        print(f"Nombre del cliente: {nombre[0]}")

        listaClaves = []
        listaServicios = []
        cursor.execute(f"SELECT * FROM NOTAS WHERE folio = {folio_cancelar};")
        res = cursor.fetchall()
        for i in res:
            listaClaves.append(i[4])

        for j in listaClaves:
            cursor.execute(f"SELECT nombreServicio FROM SERVICIOS WHERE clave = {j};")
            result = cursor.fetchone()
            listaServicios.append(result[0])
        print("Servicios: ")
        for k in listaServicios:
            print(f"\t-- {k}")
        print(f"Total a pagar: ${nota[4]}")
        try:
            while True:
                print("*" * 30)
                print("¿Está seguro en cancelar la nota?")
                resp = int(input("(1) SI | (2) NO\n>>"))
                print("*" * 30)
                listaClaves = []
                listaServicios = []
                if not resp in (1, 2):
                    print("No es una opcion válida.")
                    continue
                elif resp == 1:
                    cursor.execute(f'UPDATE NOTAS SET cancelada = 1 WHERE folio = {folio_cancelar};')
                    print("Nota cancelada con exito.")
                    conn.commit()
                    conn.close()
                    break
                elif resp == 2:
                    print("La nota no se ha cancelado. Volviendo al menu de Notas.")
                    menuNotas()
            menuNotas()
        except:
            print(f"Error: {sys.exc_info()[0]}")
        print("*" * 30)
    menuNotas()

def recuperar_nota():
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM NOTAS WHERE cancelada=1;')
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        print("No hay ninguna nota cancelada. Regresando al menu de notas.")
        menuNotas()
    folios = []
    print("*" * 60)
    for i in resultado:
        cursor.execute(f'SELECT SUM(total) FROM NOTAS WHERE folio = {i[1]};')
        totalPagar = cursor.fetchone()

        if i[1] not in folios:
            print(f"Folio: {i[1]}\tFecha: {i[2]}\tMonto a pagar: ${totalPagar[0]}")
            folios.append(i[1])
        else:
            continue
    print("*" * 60)
    try:
        while True:

            try:
                folio_recuperar = int(input("Ingrese el folio a recuperar. (Vacio para regresar al menu Notas).\n>>"))
            except:
                print("Regresando al menu de notas...")
                menuNotas()

            cursor.execute(f'SELECT folio FROM NOTAS WHERE folio={folio_recuperar} AND cancelada = 1;')
            resultado = cursor.fetchall()
            if len(resultado) < 1:
                print("*" * 30)
                print("No existe ese folio.")
                print("*" * 30)
                recuperar_nota()
                conn.commit()
                conn.close()
            else:
                while True:
                    try:
                        op = int(input("¿Está seguro que desea recuperar la nota seleccionada?\n(1) Si\t(2) No.\n>>"))
                        if op not in (1, 2):
                            print("Opcion incorrecta, vuelva a intentarlo.")
                        elif op == 1:
                            cursor.execute(f'UPDATE NOTAS SET cancelada = 0 WHERE folio = {folio_recuperar};')
                            print("*" * 30)
                            print("Nota recuperada exitosamente.")
                            conn.commit()
                            conn.close()
                        elif op == 2:
                            print("No se recuperó la nota.")
                            break
                    except:
                        print("Error en la opcion seleccionada. Vuelva a intentarlo.")
                    break
                break
    except Exception as e:
        print("Error en la captura de datos.", e)

    menuNotas()

def consulta_por_periodoNOTAS():
    print("*" * 30)
    print("Consulta por periodo.")
    datos_excel=[('Folio', 'Fecha', 'Monto a Pagar')]
    try:
        while True:
            while True:
                fecha_inicial = input("Ingrese la fecha inicial en formato dd/mm/aaaa \nENTER para especificar 01/01/2000 \n>>")
                if fecha_inicial.strip()=='':
                    fecha_inicial_format = '01/01/2000'
                    fecha_inicial_format1 = datetime.strptime(fecha_inicial_format, '%d/%m/%Y')
                else:
                    fecha_inicial_format1 = datetime.strptime(fecha_inicial, '%d/%m/%Y')
                    fecha_inicial_format = datetime.strftime(fecha_inicial_format1, '%d/%m/%Y')
                if fecha_inicial_format1 > fechaHoy:
                    print("No debe ser posterior a la fecha actual.")
                    continue
                break
            while True:
                fecha_final = input("Ingrese la fecha final en formato dd/mm/aaaa\n ENTER para especificar la fecha actual.\n>>")
                if fecha_final.strip()=='':
                    fecha_final_format = datetime.strftime(fechaHoy, '%d/%m/%Y')
                    fecha_final_format2 = fechaHoy
                else:
                    fecha_final_format2 = datetime.strptime(fecha_final, '%d/%m/%Y')
                    fecha_final_format = datetime.strftime(fecha_final_format2, '%d/%m/%Y')
                if fecha_final_format2 < fecha_inicial_format1 or fecha_final_format2 > fechaHoy:
                    print("No es correcta o es posterior a la fecha actual, ingrese una fecha valida.")
                    continue
                break
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT folio, fecha, SUM(total) FROM NOTAS WHERE (cancelada = 0) AND (fecha BETWEEN '{fecha_inicial_format}' AND '{fecha_final_format}') GROUP BY folio;")
            res = cursor.fetchall()
            conn.commit()
            conn.close()
            print("*" * 30)
            for i in res:
                print(f"Folio: {i[0]}\tFecha: {i[1]}\tMonto a pagar: {i[2]}")
                datos_excel.append((i[0],i[1],i[2]))
            print("*" * 30)
            if len(res)>0:
                print("Exportar")
                op = int(input("1. CSV\n"
                               "2. EXCEL\n"
                               "3. No exportar, regresar al menu de reportes\n"
                               ">>"))

                if op == 2:
                    df = pd.DataFrame(datos_excel[1:], columns=datos_excel[0])
                    fecha_inicial_format1 = datetime.strftime(fecha_inicial_format1, '%m-%d-%Y')
                    fecha_final_format2 = datetime.strftime(fecha_final_format2, '%m-%d-%Y')
                    df.to_excel(f'ReportePorPeriodo_{fecha_inicial_format1}_{fecha_final_format2}.xlsx', index=False)
                    print("Exportado correctamente.")
                    menuNOTAS()
                elif op == 1:
                    fecha_inicial_format = datetime.strftime(fecha_inicial_format1, '%m-%d-%Y')
                    fecha_final_format = datetime.strftime(fecha_final_format2, '%m-%d-%Y')
                    with open(f'ReportePorPeriodo_{fecha_inicial_format}_{fecha_final_format}.csv', 'w', newline='', encoding='utf-8') as archivo_csv:
                        escritor_csv = csv.writer(archivo_csv)
                        escritor_csv.writerows(datos_excel)
                        print("*"*30)
                        print("Exportado correctamente.")
                        print("*" * 30)
                    menuNotas()
                elif op == 3:
                    print("No se exportaron los datos. Regresando...")
                    menuConsultasYReportesNOTAS()
                    break
            else:
                print("No se econtraron notas.")
                menuNotas()

            break
    except Exception as e:
        print("Debe ser con formato dd/mm/aaaa.", e)

def menuConsultasYReportesNOTAS():
    try:
        while True:
            op = int(input("Seleccione una opcion:\n"
                           "1.Consulta por periodo.\n"
                           "2.Consulta por folio\n"
                           "3.Volver la menu principal\n>>"))
            if op not in (1, 2, 3):
                print("Opción no válida.")
                continue
            elif op == 1:
                consulta_por_periodoNOTAS()
                break
            elif op == 2:
                consulta_por_folioNOTAS()
                break
            elif op == 3:
                menu_principal()
                break
    except Exception as e:
        print("Error en la captura de opcion. Error:", e)

def consulta_por_folioNOTAS():
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT folio, fecha, clave_cliente, x FROM NOTAS WHERE cancelada = 0 ORDER BY folio ASC;")
    resultado = cursor.fetchall()

    print("*" * 30)
    print("Listado:\n")
    for i in resultado:
        cursor.execute(f"SELECT nombre FROM CLIENTES WHERE clave = {i[2]} ;")
        nombreCliente = cursor.fetchone()
        print(f"Folio: {i[0]}\tFecha: {i[1]}\tNombre: {nombreCliente[0]}")
    print("*" * 30)
    conn.close()
    try:
        solicito = int(input("Ingrese el folio a consultar:\n>>"))

        conn = sqlite3.connect("TALLER_MECANICO.db")
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT folio, fecha, clave_cliente, clave_servicio, SUM(total) FROM NOTAS WHERE cancelada = 0 AND folio = {solicito};')
        nota = cursor.fetchone()
        if nota[0] is None:
            print("*" * 30)
            print("¡" * 10, "No existe ese folio.", "!" * 10)
            consulta_por_folioNOTAS()
        cursor.execute(f'SELECT nombre FROM CLIENTES WHERE clave={nota[2]}')
        nombre = cursor.fetchone()
        print("*" * 30)
        print(f"Folio: {nota[0]}")
        print(f"Fecha: {nota[1]}")
        print(f"Nombre del cliente: {nombre[0]}")

        listaClaves = []
        listaServicios = []
        cursor.execute(f"SELECT * FROM NOTAS WHERE folio = {solicito};")
        res = cursor.fetchall()
        for i in res:
            listaClaves.append(i[4])

        for j in listaClaves:
            cursor.execute(f"SELECT nombreServicio FROM SERVICIOS WHERE clave = {j};")
            result = cursor.fetchone()
            listaServicios.append(result[0])
        print("Servicios: ")
        for k in listaServicios:
            print(f"\t-- {k}")
        print(f"Total a pagar: ${nota[4]}")
        conn.close()
        menuNotas()
    except sqlite3.Error as s:
        print("Error: ", s)
    except Exception as e:
        print("Error en la entrada del folio. Intente nuevamente y no deje vacio.", e)
        consulta_por_folioNOTAS()

def menuClientes():
    print("*" * 30)
    print("\tMenu Clientes\n")
    while True:
        print("*" * 30)
        print("1. Agregar un cliente")
        print("2. Suspender un cliente")
        print("3. Recuperar cliente")
        print("4. Consultas y reportes")
        print("5. Volver al menú principal")

        try:
            opcion = int(input("Seleccione una opción: "))
        except Exception as e:
            print("Error en la opcion elegida. Detalle: ", e)
            menuClientes()
        if opcion == "1":
            agregar_cliente()
            break
        elif opcion == '2':
            suspenderCliente()
            break
        elif opcion == '3':
            recuperarCliente()
            break
        elif opcion == "4":
            menuConsultasyReportesCLIENTES()
            break
        elif opcion == "5":
            menu_principal()
            break

def agregar_cliente():
    print("*" * 30)
    print("\tAgregar cliente\n")
    while True:
        patronNombre = r'[A-Za-z ]{2,}'
        C_nombreCliente = input("Ingrese su nombre completo\n>>")
        if not bool(re.match(patronNombre, C_nombreCliente.lower())) or len(C_nombreCliente.split()) == 0:
            print("!" * 30)
            print("No debe estar vacio, no debe contener numeros, espacios en blanco, ni sólo una letra.")
            continue
        C_nombreCliente = C_nombreCliente.upper()
        break
    while True:
        C_RFC = input("Ingresa tu RFC->")
        if len(C_RFC.split()) == 0:
            print("No debe ser vacio, ni debe tener solo espacios en blanco.")
            continue
        C_RFC = C_RFC.upper()
        if not bool(re.match("[A-Z]{4}[0-9]{6}[A-Z0-9]{3}", C_RFC)):
            print("!" * 30)
            print("Formato incorrecto o incompleto. Ingrese nuevamente.")
            continue
        else:
            break
    while True:
        C_correo = input("Ingresa tu correo->")
        if len(C_correo.split()) == 0:
            print("!" * 30)
            print("No debe ser vacio, ni debe tener solo espacios en blanco.")
            continue
        patron = r'[\w\._\-\d]+@(gmail|hotmail|outlook|yahoo|uanl|live)\.[a-z]{1,2}'
        if not bool(re.match(patron, C_correo.lower())):
            print("!" * 30)
            print("Formato incorrecto o incompleto. Ingrese nuevamente.")
            continue
        else:
            break

    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(clave) FROM CLIENTES")
    resultado = cursor.fetchone()
    if resultado[0] is None:
        claveMax = 0
    else:
        claveMax = resultado[0] + 1
    cursor.execute(f"INSERT INTO CLIENTES VALUES({claveMax},'{C_nombreCliente}','{C_RFC}','{C_correo}')")
    conn.commit()
    conn.close()
    print("Cliente agregado correctamente.")
    menuClientes()

def suspenderCliente():
    print("REPORTE TABULAR")
    print("CLAVE Y NOMBRE")
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT clave, nombre FROM CLIENTES WHERE suspendido = 0;")
    res = cursor.fetchall()
    if len(res)>0:
        print("*" * 30)
        for i in res:
            print(f"Clave: {i[0]}\tNombre: {i[1]}")
        print("*" * 30)
    else:
        print("No hay clientes o fueron suspendidos anteriormente.")
    conn.commit()
    conn.close()

    while True:
        try:
            llave = input("Ingresa la clave del cliente que deseas suspender.\n\tIngrese O para no suspender a ningún cliente.\n>>")
            if str(llave).upper() == 'O':
                print("No se suspendió ningun cliente. Regresando...")
                menuClientes()
            else:
                conn = sqlite3.connect("TALLER_MECANICO.db")
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM CLIENTES WHERE clave={llave} AND suspendido = 0;")
                res = cursor.fetchall()
                print("*" * 30)
                for i in res:
                    print(f"Clave: {i[0]}\tNombre: {i[1]}\tRFC: {i[2]}\tCORREO: {i[3]}")
                print("*" * 30)
                conn.commit()
                conn.close()
                while True:
                    try:
                        resp = int(input("¿Está seguro de suspender al cliente seleccionado? (1). SI / (2). NO\n>>"))
                    except:
                        print("Debe ingresar un dato correcto. Debe ser numerico, y no debe estar vacio.")
                        continue
                    if resp not in (1, 2):
                        print("Opcion incorrecta, seleccione 1 o 2.")
                        continue
                    if resp == 1:
                        conn = sqlite3.connect("TALLER_MECANICO.db")
                        cursor = conn.cursor()
                        cursor.execute(f"UPDATE CLIENTES SET suspendido = 1 WHERE clave = {llave};")
                        if cursor:
                            print("Cliente suspendido.")
                        conn.commit()
                        conn.close()
                        break
                    elif resp == 2:
                        print("El cliente no ha sido suspendido. Regresando...")
                        menuClientes()
                        break
        except Exception as e:
            print("Error: ", e)
        break

def recuperarCliente():
    print("REPORTE TABULAR")
    print("CLAVE Y NOMBRE")
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT clave, nombre FROM CLIENTES WHERE suspendido = 1;")
    res = cursor.fetchall()
    if len(res) > 0:
        print("*" * 30)
        for i in res:
            print(f"Clave: {i[0]}\tNombre: {i[1]}")
        print("*" * 30)
    else:
        print("No hay clientes suspendidos")
    conn.commit()
    conn.close()

    while True:
        try:
            llave = input("Ingresa la clave del cliente que recuperar.\n\tIngrese O para no recuperar a ningún cliente.\n>>")
            if str(llave).upper() == 'O':
                print("No se recuperó ningun cliente. Regresando...")
                menuClientes()
            else:
                conn = sqlite3.connect("TALLER_MECANICO.db")
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM CLIENTES WHERE clave={llave} AND suspendido = 1;")
                res = cursor.fetchall()
                print("*" * 30)
                for i in res:
                    print(f"Clave: {i[0]}\tNombre: {i[1]}\tRFC: {i[2]}\tCORREO: {i[3]}")
                print("*" * 30)
                conn.commit()
                conn.close()
                while True:
                    try:
                        resp = int(input("¿Está seguro de recuperar al cliente seleccionado? (1). SI / (2). NO\n>>"))
                    except:
                        print("Debe ingresar un dato correcto. Debe ser numerico, y no debe estar vacio.")
                        continue
                    if resp not in (1, 2):
                        print("Opcion incorrecta, seleccione 1 o 2.")
                        continue
                    if resp == 1:
                        conn = sqlite3.connect("TALLER_MECANICO.db")
                        cursor = conn.cursor()
                        cursor.execute(f"UPDATE CLIENTES SET suspendido = 0 WHERE clave = {llave};")
                        if cursor:
                            print("Cliente recuperado.")
                        conn.commit()
                        conn.close()
                        break
                    elif resp == 2:
                        print("El cliente no ha sido suspendido. Regresando...")
                        menuClientes()
                        break
        except Exception as e:
            print("Error: ", e)
        break

def menuConsultasyReportesCLIENTES():
    while True:
        print("*" * 30)
        print("\tMenu Consultas y Reportes\n")
        print("1. Listado de clientes registrados")
        print("2. Busqueda por clave")
        print("3. Busqueda por nombre")
        print("4. Volver al menú de clientes")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listado_clientes_registrados()
            break
        elif opcion == "2":
            busquedaPorClave()
            break
        elif opcion == "3":
            busquedaPorNombre()
            break
        elif opcion == "4":
            menuClientes()
            break
        else:
            print("No es una opcion valida.")
            continue

def busquedaPorClave():
    print("*" * 30)
    print("\tBusqueda por clave\n")
    datos_excel=[]
    try:
        while True:
            print("Ingresa la clave del cliente a buscar")
            try:
                claveBuscar = int(input(">>"))
            except:
                print("Regresando...")
                menuConsultasyReportesCLIENTES()

            datos_excel = [('Clave', 'Nombre', 'RFC', 'CORREO')]

            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM CLIENTES WHERE clave={claveBuscar}")
            resultado = cursor.fetchall()
            for clave, nombre, rfc, correo in resultado:
                datos_excel.append((clave, nombre, rfc, correo))
            if resultado is None or len(resultado) == 0:
                print("No hay datos de la clave ingresada, intenta con una existente")
                continue



            print("*" * 30)
            print(f"Clave: {resultado[0][0]}")
            print(f"Nombre: {resultado[0][1]}")
            print(f"RFC: {resultado[0][2]}")
            print(f"Correo: {resultado[0][3]}")
            print("*" * 30)

            conn.commit()
            conn.close()

            print("Exportar")
            op = int(input("1. CSV\n"
                           "2. EXCEL\n"
                           "3. No exportar, regresar al menu de reportes\n"
                           ">>"))

            if op == 2:
                df = pd.DataFrame(datos_excel[1:], columns=datos_excel[0])
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                df.to_excel(f'ReporteClientesActivosPorClave_{fechahoy}.xlsx', index=False)
                print("Exportado correctamente.")
            elif op == 1:
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                with open(f'ReporteClientesActivosPorClave_{fechahoy}.csv', 'w', newline='',
                          encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerows(datos_excel)
                    print("Exportado correctamente.")
            elif op==3:
                print("No se exportaron los datos. Regresando...")
                menuConsultasyReportesCLIENTES()
                break
    except Exception as e:
        print("!" * 30)
        print("Debe ser un valor numerico, y no debe estar vacio.", e)

def busquedaPorNombre():
    print("*" * 30)
    print("\tBusqueda por nombre\n")
    try:
        while True:
            print("Ingresa el nombre del cliente a buscar")
            nombre = input(">>")
            if len(nombre.split()) == 0:
                print("Regresando...")
                menuConsultasyReportesCLIENTES()
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()

            datos_excel = [('Clave', 'Nombre', 'RFC', 'CORREO')]
            consulta = "SELECT * FROM clientes WHERE nombre LIKE ?"
            cursor.execute(consulta, ('%' + nombre + '%',))
            resultado = cursor.fetchall()
            if resultado[0] is None:
                print("No hay datos del nombre ingresado, intenta con uno existente")
                continue
            print("*" * 30)
            for i in resultado:
                print(f"Clave: {i[0]}\t| Nombre: {i[1]}\t| RFC: {i[2]}\t| Correo: {i[3]}")
            print("*" * 30)

            for clave, nombre, rfc, correo in resultado:
                datos_excel.append((clave, nombre, rfc, correo))

            print("Exportar")
            op = int(input("1. CSV\n"
                           "2. EXCEL\n"
                           "3. No exportar, regresar al menu de reportes\n"
                           ">>"))

            if op == 2:
                df = pd.DataFrame(datos_excel[1:], columns=datos_excel[0])
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                df.to_excel(f'ReporteClientesActivosPorNombre_{fechahoy}.xlsx', index=False)
                print("Exportado correctamente.")
            elif op == 1:
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                with open(f'ReporteClientesActivosPorNombre_{fechahoy}.csv', 'w', newline='',
                          encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerows(datos_excel)
                    print("Exportado correctamente.")
            elif op==3:
                menuConsultasyReportesCLIENTES()

            conn.commit()
            conn.close()
    except Exception as e:
        print("!" * 30)
        print("No se encontró el nombre.", e)
    pass

def listado_clientes_registrados():
    print("*" * 30)
    datos_excel = [('Clave', 'Nombre', 'RFC', 'CORREO')]
    print("Selecciona.")
    try:
        try:
            op = int(input("1. Ordenado por clave\n"
                       "2. Ordenados por nombre de servicio\n"
                       "3. Volver al menú anterior\n>>"))
        except Exception as e:
            print("No fue posible continuar con espacios en blanco, ni letras ni simbolos. Intentalo de nuevo.")
            listado_clientes_registrados()
        if op == 1:
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CLIENTES ORDER BY clave")
            resultado = cursor.fetchall()
            print("*" * 30)
            for clave, nombre, rfc, correo in resultado:
                print(f"Clave: {clave}\t|\t{nombre}\t|\t{rfc}\t|\t{correo}")
                datos_excel.append((clave, nombre, rfc, correo))
            print("*" * 30)
            conn.commit()
            conn.close()

            print("Exportar")
            op = int(input("1. CSV\n"
                           "2. EXCEL\n"
                           "3. No exportar, regresar al menu de reportes\n"
                           ">>"))

            if op == 2:
                df = pd.DataFrame(datos_excel[1:], columns=datos_excel[0])
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')

                df.to_excel(f'ReporteClientesActivosPorClave_{fechahoy}.xlsx', index=False)
                print("Exportado correctamente.")
                menuConsultasyReportesCLIENTES()
            elif op == 1:
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                with open(f'ReporteClientesActivosPorClave_{fechahoy}.csv', 'w', newline='',
                          encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerows(datos_excel)
                    print("Exportado correctamente.")
                    menuConsultasyReportesCLIENTES()
            elif op == 3:
                menuConsultasyReportesCLIENTES()

        elif op == 2:
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CLIENTES ORDER BY nombre")
            resultado = cursor.fetchall()
            print("*" * 30)
            for clave, nombre, rfc, correo in resultado:
                print(f"Clave: {clave}\t|\t{nombre}\t|\t{rfc}\t|\t{correo}")
                datos_excel.append((clave, nombre, rfc, correo))
            print("*" * 30)
            conn.commit()
            conn.close()

            print("Exportar")
            op = int(input("1. CSV\n"
                           "2. EXCEL\n"
                           "3. No exportar, regresar al menu de reportes\n"
                           ">>"))

            if op == 2:
                df = pd.DataFrame(datos_excel[1:], columns=datos_excel[0])
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')

                df.to_excel(f'ReporteClientesActivosPorNombre_{fechahoy}.xlsx', index=False)
                print("Exportado correctamente.")
            elif op == 1:
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                with open(f'ReporteClientesActivosPorNombre_{fechahoy}.csv', 'w', newline='',
                          encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerows(datos_excel)
                    print("Exportado correctamente.")
            elif op == 3:
                menuConsultasyReportesCLIENTES()
        elif op == 3:
            menuConsultasyReportesCLIENTES()

        listado_clientes_registrados()
    except Exception as e:
        print("!" * 30)
        print("Error en la entrada de datos. Vuelva a intentarlo con los numeros 1, 2 o 3.")
        print(e)
    pass

def mostrarServicios():
    while True:
        print("*" * 30)
        print("\tBusqueda por clave")
        conn = sqlite3.connect("TALLER_MECANICO.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SERVICIOS ORDER BY clave")
        resultado = cursor.fetchall()
        print("*" * 30, "\nListado:")
        for clave, nombreServicio, costo, x in resultado:
            print(f"Clave: {clave}\t{nombreServicio}")
        print("*" * 30)
        conn.commit()
        conn.close()
        break

def agregar_servicio():
    while True:
        validar = r'\d'
        print("*" * 30)
        print("\tAgregar Servicio")
        S_nombre = input("Ingrese nombre del servicio: ")
        if len(S_nombre.split()) == 0:
            print("No puede quedar vacio.")
            continue
        numeros = re.search(validar, S_nombre)
        if not numeros is None:
            print("No debe tener numeros el nombre del servicio.")
            continue
        break
    while True:
        try:
            costo = float(input("Ingrese el costo del servicio: "))
            if len(str(costo).split()) == 0 or costo + costo == 0.0:
                print("No debe estar vacio, ni tampoco debe ser 0 (cero).")
        except:
            print("Debe ser un valor con o sin decimal, no letras ni simbolos.\nNo debe estar vacio.")
        break

    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(clave) FROM SERVICIOS")
    resultado = cursor.fetchone()
    if resultado[0] is None:
        claveMax = 0
    else:
        claveMax = resultado[0] + 1
    cursor.execute(f"INSERT INTO SERVICIOS VALUES({claveMax},'{S_nombre}','{costo}')")
    conn.commit()
    conn.close()
    print("Servicio agregado correctamente.")
    menuServicios()

def suspenderServicio():
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT clave, nombreServicio FROM SERVICIOS WHERE suspendidoServicio=0;")
    res = cursor.fetchall()
    if len(res) > 0:
        print("*" * 30)
        for i in res:
            print(f"Clave: {i[0]}\tServicio: {i[1]}")
        print("*" * 30)
    else:
        print("No hay servicios o fueron suspendidos anteriormente.")
        menuServicios()
    conn.commit()
    conn.close()

    while True:
        try:
            llave = input(
                "Ingresa la clave del servicio que deseas suspender.\n\tIngrese O para no suspender ningun servicio.\n>>")
            if str(llave).upper() == 'O':
                print("No se suspendió ningun servicio. Regresando...")
                menuServicios()
            else:
                conn = sqlite3.connect("TALLER_MECANICO.db")
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM SERVICIOS WHERE clave={llave} AND suspendidoServicio = 0;")
                res = cursor.fetchall()
                print("*" * 30)
                for i in res:
                    print(f"Clave: {i[0]}\tServicio: {i[1]}\tCosto: {i[2]}")
                print("*" * 30)
                conn.commit()
                conn.close()
                while True:
                    resp = input("¿Está seguro de suspender el servicio seleccionado? (1). SI / (2). NO\n>>")
                    if resp.strip() == '':
                        print("No debe ser un valor vacio.")
                        continue
                    elif resp not in ("1", "2"):
                        print("Opcion incorrecta, seleccione 1 o 2.")
                        continue
                    elif resp == '1':
                        conn = sqlite3.connect("TALLER_MECANICO.db")
                        cursor = conn.cursor()
                        cursor.execute(f"UPDATE SERVICIOS SET suspendidoServicio = 1 WHERE clave = {llave};")
                        print("Servicio suspendido.")
                        conn.commit()
                        conn.close()
                        menuServicios()
                        break
                    elif resp == '2':
                        print("El servicio no ha sido suspendido. Regresando...")
                        menuServicios()
                    break
        except Exception as e:
            print("Error: ", e)
        break


def recuperarServicio():
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT clave, nombreServicio FROM SERVICIOS WHERE suspendidoServicio=1;")
    res = cursor.fetchall()
    if len(res) > 0:
        print("*" * 30)
        for i in res:
            print(f"Clave: {i[0]}\tServicio: {i[1]}")
        print("*" * 30)
    else:
        print("No hay servicios suspendidos.")
        menuServicios()
    conn.commit()
    conn.close()

    while True:
        try:
            llave = input(
                "Ingresa la clave del servicio que deseas recuperar.\n\tIngrese O para no recuperar ningun servicio.\n>>")
            if str(llave).upper() == 'O':
                print("No se recuperó ningun servicio. Regresando...")
                menuServicios()
            else:
                conn = sqlite3.connect("TALLER_MECANICO.db")
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM SERVICIOS WHERE clave={llave} AND suspendidoServicio = 1;")
                res = cursor.fetchall()
                print("*" * 30)
                for i in res:
                    print(f"Clave: {i[0]}\tServicio: {i[1]}\tCosto: {i[2]}")
                print("*" * 30)
                conn.commit()
                conn.close()
                while True:
                    resp = input("¿Está seguro de recuperar el servicio seleccionado? (1). SI / (2). NO\n>>")
                    if resp.strip() == '':
                        print("No debe ser un valor vacio.")
                        continue
                    elif resp not in ("1", "2"):
                        print("Opcion incorrecta, seleccione 1 o 2.")
                        continue
                    elif resp == '1':
                        conn = sqlite3.connect("TALLER_MECANICO.db")
                        cursor = conn.cursor()
                        cursor.execute(f"UPDATE SERVICIOS SET suspendidoServicio = 0 WHERE clave = {llave};")
                        print("Servicio recuperado.")
                        conn.commit()
                        conn.close()
                        menuServicios()
                        break
                    elif resp == '2':
                        print("El servicio no ha sido recuperado. Regresando...")
                        menuServicios()
                    break
        except Exception as e:
            print("Error: ", e)
        break

def busquedaPorClaveSERVICIOS():
    try:
        try:
            print("Ingresa la clave del servicio a buscar")
            claveBuscar = int(input(">>"))
        except Exception as e:
            print("Regresando...")
            menuConsultasyReportesSERVICIOS()

        conn = sqlite3.connect("TALLER_MECANICO.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM SERVICIOS WHERE clave={claveBuscar}")
        resultado = cursor.fetchall()
        if not len(resultado) == 0:
            print("\n", "*" * 30)
            print(f"Clave: {resultado[0][0]}")
            print(f"Servicio: {resultado[0][1]}")
            print(f"Costo: ${resultado[0][2]}")
            print("*" * 30, "\n")
        else:
            print("No hay datos de la clave ingresada, intenta con una existente")
            busquedaPorClaveSERVICIOS()
        conn.commit()
        conn.close()
        busquedaPorClaveSERVICIOS()
    except Exception as e:
        print("!" * 30)
        print("Debe ser un valor numerico, y no debe estar vacio.", e)

def busquedaPorNombreSERVICIOS():
    print("*" * 30)
    print("\tBusqueda por nombre de servicio\n")
    try:
        while True:
            print("Ingresa el nombre del servicio a buscar")
            nombre = input(">>")
            if len(nombre.split()) == 0:
                print("Regresando...")
                menuConsultasyReportesSERVICIOS()
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()

            consulta = "SELECT * FROM SERVICIOS WHERE nombreServicio LIKE ?"
            cursor.execute(consulta, ('%' + nombre + '%',))
            resultado = cursor.fetchall()
            if len(resultado) < 1:
                print("\t - No hay datos del servicio ingresado, intenta con uno existente")
                continue
            print("*" * 30)
            for i in resultado:
                print(f"Clave: {i[0]}\t| Servicio: {i[1]}\t| Costo: ${i[2]}\t")
            print("*" * 30)
            conn.commit()
            conn.close()
    except Exception as e:
        print("!" * 30)
        print("No se encontró el servicio.", e)

def menuConsultasyReportesSERVICIOS():
    while True:
        print("*" * 30)
        print("\tMenu Consultas y Reportes\n")
        print("1. Busqueda por clave de servicio")
        print("2. Busqueda por nombre del servicio")
        print("3. Listado de servicios")
        print("4. Volver al menú de servicios")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrarServicios()
            busquedaPorClaveSERVICIOS()
            break
        elif opcion == "2":
            busquedaPorNombreSERVICIOS()
            break
        elif opcion == "3":
            listado_servicios_registrados()
            break
        elif opcion == "4":
            menuServicios()
            break
        else:
            print("No es una opcion valida.")
            continue

def listado_servicios_registrados():
    print("*" * 30)
    datos_excel = [('Clave', 'Servicio', 'Costo')]
    print("Selecciona.")
    try:
        try:
            op = int(input("1. Ordenado por clave\n"
                       "2. Ordenados por nombre de servicio\n"
                       "3. Volver al menú anterior\n>>"))
        except Exception as e:
            print("No fue posible continuar con espacios en blanco, ni letras ni simbolos. Intentalo de nuevo.")
            listado_servicios_registrados()
        if op == 1:
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM SERVICIOS ORDER BY clave")
            resultado = cursor.fetchall()
            print("*" * 30)
            for clave, nombreServicio, costo, x in resultado:
                print(f"Clave: {clave}\t|\t{nombreServicio}\t|\t${costo}")
                datos_excel.append((clave, nombreServicio, costo))
            print("*" * 30)
            conn.commit()
            conn.close()

            print("Exportar")
            op = int(input("1. CSV\n"
                           "2. EXCEL\n"
                           "3. No exportar, regresar al menu de reportes\n"
                           ">>"))

            if op == 2:
                df = pd.DataFrame(datos_excel[1:], columns=datos_excel[0])
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                df.to_excel(f'ReporteServiciosPorClave_{fechahoy}.xlsx', index=False)
                print("Exportado correctamente.")
            elif op == 1:
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                with open(f'ReporteServiciosPorNombre_{fechahoy}.csv', 'w', newline='',
                          encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerows(datos_excel)
                    print("Exportado correctamente.")
            elif op == 3:
                menuConsultasyReportesSERVICIOS()
        elif op == 2:
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM SERVICIOS ORDER BY nombreServicio")
            resultado = cursor.fetchall()
            print("*" * 30)
            for clave, nombreServicio, costo, x in resultado:
                print(f"Clave: {clave}\t|\t{nombreServicio}\t|\t${costo} ")
                datos_excel.append((clave, nombreServicio, costo))
            print("*" * 30)
            conn.commit()
            conn.close()

            print("Exportar")
            op = int(input("1. CSV\n"
                           "2. EXCEL\n"
                           "3. No exportar, regresar al menu de reportes\n"
                           ">>"))

            if op == 2:
                df = pd.DataFrame(datos_excel[1:], columns=datos_excel[0])
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')

                df.to_excel(f'ReporteServiciosPorNombre_{fechahoy}.xlsx', index=False)
                print("Exportado correctamente.")
            elif op == 1:
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                with open(f'ReporteServiciosPorNombre_{fechahoy}.csv', 'w', newline='',
                          encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerows(datos_excel)
                    print("Exportado correctamente.")
            elif op == 3:
                menuConsultasyReportesSERVICIOS()
        elif op == 3:
            menuConsultasyReportesSERVICIOS()
        listado_servicios_registrados()
    except Exception as e:
        print("!" * 30)
        print("Error en la entrada de datos. Vuelva a intentarlo con los numeros 1, 2 o 3.")
        print(e)
    pass

def menuServicios():
    print("*" * 30)
    print("\tMenu Servicios\n")
    while True:
        print("1. Agregar un servicio")
        print("2. Suspender un servicio")
        print("3. Recuperar un servicio")
        print("4. Consultas y reportes")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_servicio()
            break
        if opcion == "2":
            suspenderServicio()
            break
        if opcion == "3":
            recuperarServicio()
            break
        elif opcion == "4":
            menuConsultasyReportesSERVICIOS()
            break
        elif opcion == "5":
            menu_principal()
            break

def serviciosMasPrestados():
    conexion = sqlite3.connect("TALLER_MECANICO.db")
    consulta_servicios = "SELECT clave, nombreServicio FROM SERVICIOS WHERE suspendidoServicio = 0"
    df_servicios = pd.read_sql_query(consulta_servicios, conexion)

    while True:
        try:
            fecha_inicial_str = input("Ingrese la fecha inicial del período a reportar (mm/dd/aaaa): ")
            fecha_final_str = input("Ingrese la fecha final del período a reportar (mm/dd/aaaa): ")

            fecha_inicial = datetime.strptime(fecha_inicial_str, '%m/%d/%Y')
            fecha_final = datetime.strptime(fecha_final_str, '%m/%d/%Y')
        except Exception as e:
            print("Error: ", e)
            continue
        break

    consulta_notas = f"SELECT id_nota, folio, fecha, clave_cliente, clave_servicio FROM Notas WHERE cancelada = 0 AND fecha BETWEEN '{fecha_inicial_str}' AND '{fecha_final_str}'"
    df_notas = pd.read_sql_query(consulta_notas, conexion)

    conexion.close()

    cantidad_servicios = int(input("Ingrese la cantidad de servicios más prestados a identificar: "))

    df_notas['fecha'] = pd.to_datetime(df_notas['fecha'], format='%m/%d/%Y')
    df_notas_periodo = df_notas[(df_notas['fecha'] >= fecha_inicial) & (df_notas['fecha'] <= fecha_final)]

    top_servicios = df_notas_periodo['clave_servicio'].value_counts().head(cantidad_servicios)

    top_servicios_nombres = df_servicios.set_index('clave').loc[top_servicios.index, 'nombreServicio']

    reporte = pd.DataFrame({'Servicio': top_servicios_nombres, '   Veces Prestado': top_servicios})
    print(" *"*70)
    if len(reporte)<1:
        print("No hay datos.")
        serviciosMasPrestados()
    else:
        print(reporte)
    print(" *" * 70)
    exportar = input("\n¿Desea exportar el reporte? (1) SI  (2) NO\n>>")
    if exportar == '1':
        nombre_archivo = f"ReporteServiciosMasPrestados_{fecha_inicial.strftime('%m_%d_%Y')}_{fecha_final.strftime('%m_%d_%Y')}"

        while True:
            formato_exportacion = input("Elija el formato de exportación: (1) CSV  (2) EXCEL \n>>")
            if formato_exportacion not in ("1", "2"):
                print("No es correcta la opcion seleccionada. Intente nuevamente.")
                continue
            elif formato_exportacion == '1':
                reporte.to_csv(f"{nombre_archivo}.csv", index=False)
                print(f"Se ha exportado correctamente")
            elif formato_exportacion == '2':
                reporte.to_excel(f"{nombre_archivo}.xlsx", index=False)
                print(f"Se ha exportado correctamente")
            break
    else:
        print("El reporte no ha sido exportado.")


def clientesConMasNotas():
    conexion = sqlite3.connect("TALLER_MECANICO.db")

    consulta_clientes = "SELECT clave, nombre FROM CLIENTES WHERE suspendido = 0"
    df_clientes = pd.read_sql_query(consulta_clientes, conexion)

    cantidad_clientes = int(input("Ingrese la cantidad de clientes con más notas a identificar: "))
    fecha_inicial_str = input("Ingrese la fecha inicial del período a reportar (mm/dd/aaaa): ")
    fecha_final_str = input("Ingrese la fecha final del período a reportar (mm/dd/aaaa): ")

    fecha_inicial = datetime.strptime(fecha_inicial_str, '%m/%d/%Y')
    fecha_final = datetime.strptime(fecha_final_str, '%m/%d/%Y')

    consulta_notas = f"SELECT id_nota, clave_cliente FROM NOTAS WHERE fecha BETWEEN '{fecha_inicial_str}' AND '{fecha_final_str}'"
    df_notas = pd.read_sql_query(consulta_notas, conexion)

    top_clientes = df_notas['clave_cliente'].value_counts().head(cantidad_clientes)

    top_clientes_nombres = df_clientes.set_index('clave').loc[top_clientes.index, 'nombre']
    reporte_clientes = pd.DataFrame({'Cliente': top_clientes_nombres, 'Cantidad de Notas': top_clientes})
    print(" *"*70)
    if len(reporte_clientes)<1:
        print("No hay datos.")
        clientesConMasNotas()
    else:
        print(reporte_clientes)
    print(" *" * 70)
    exportar = input("\n¿Desea exportar el reporte? (1) SI  (2) NO\n>>")
    if exportar == '1':
        nombre_archivo = f"ReporteClientesConMasNotas_{fecha_inicial.strftime('%m_%d_%Y')}_{fecha_final.strftime('%m_%d_%Y')}"

        while True:
            formato_exportacion = input("Elija el formato de exportación: (1) CSV  (2) EXCEL \n>>")
            if formato_exportacion not in ("1", "2"):
                print("No es correcta la opción seleccionada. Intente nuevamente.")
                continue
            elif formato_exportacion == '1':
                reporte_clientes.to_csv(f"{nombre_archivo}.csv", index=False)
                print(f"Se ha exportado correctamente.")
            elif formato_exportacion == '2':
                reporte_clientes.to_excel(f"{nombre_archivo}.xlsx", index=False)
                print(f"Se ha exportado correctamente.")
            break
    else:
        print("El reporte no ha sido exportado.")
    conexion.close()


def montoPromedio():
    conexion = sqlite3.connect("TALLER_MECANICO.db")
    while True:
        try:
            fecha_inicial_str = input("Ingrese la fecha inicial del período a reportar (mm/dd/aaaa): ")
            fecha_final_str = input("Ingrese la fecha final del período a reportar (mm/dd/aaaa): ")

            fecha_inicial = datetime.strptime(fecha_inicial_str, '%m/%d/%Y')
            fecha_final = datetime.strptime(fecha_final_str, '%m/%d/%Y')
        except Exception as e:
            print(f"Error: {e}")
            continue
        break
    consulta_notas = f"SELECT total FROM NOTAS WHERE cancelada = 0 AND fecha BETWEEN '{fecha_inicial_str}' AND '{fecha_final_str} '"
    df_notas = pd.read_sql_query(consulta_notas, conexion)

    monto_promedio = df_notas['total'].mean()

    print(
        f"\nEl monto promedio de las notas para el período {fecha_inicial_str} - {fecha_final_str} es: ${monto_promedio:.2f}")
    conexion.close()

def menuEstadisticas():
    print("\nElige una opcion del menu:")
    while True:
        try:
            op = int(input("\n1. Servicios más prestados.\n2. Clientes con más notas.\n3.Promedio de los montos de las notas.\n>>"))
            if op == 1:
                serviciosMasPrestados()
                break
            elif op == 2:
                clientesConMasNotas()
            elif op == 3:
                montoPromedio()
        except Exception as e:
            print("Error:", e)



def menu_principal():
    while True:
        print("*" * 30)
        print("Menú Principal")
        print("1. Menú Notas")
        print("2. Menú Clientes")
        print("3. Menú Servicios")
        print("4. Menú Estadísticas")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menuNotas()
            break
        elif opcion == "2":
            menuClientes()
            break
        elif opcion == "3":
            menuServicios()
            break
        elif opcion == "4":
            menuEstadisticas()
        elif opcion == "5":
            confirmacion = int(input("¿Está seguro que desea salir? (1. Sí/2. No): "))
            if confirmacion == 1:
                print("Saliendo del programa...")
                exit()
            elif confirmacion == 2:
                continue
            else:
                print("Opción no válida. Regresando al menú principal.")
        else:
            print("Opción no válida. Intente de nuevo.")

menu_principal()