# BASE DE DATOS
import sys, sqlite3, re, os, pandas as pd, csv
from sqlite3 import Error
from datetime import datetime
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
fecha = datetime.strftime(fechaHoy, '%d/%m/%Y')
fecha2 = datetime.strptime(fecha, '%d/%m/%Y')

idnota = 0

# Menú Notas
def registrar_nota():
    while True:
        print("*" * 30)
        print("Agregar una nota")
        print("*" * 30)
        try:
            # INGRESA LA CLAVE, SI EXISTE, CONTINUA INGRESANDO DATOS
            # SI NO EXISTE SE REPITE LA SOLICITUD
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT clave, nombre FROM CLIENTES;")
            listado = cursor.fetchall()
            print("Listado de clientes registrados:")
            for i, j in listado:
                print(f"Clave: {i}\tNombre: {j}")
            print("*" * 30)
            conn.close()

            clave2 = int(input("Ingresa la clave de cliente\n>>"))
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

        # AQUI INGRESA LA FECHA EN FORMATO DD/MM/YYYY, SI ES
        # INCORRECTA O POSTERIOR A LA ACTUAL NO DEJA AVANZAR
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

        # SOLICITANDO LA CLAVE DEL SERVICIO
        # PARA IR AGREGANDO A LA TABLA NOTAS EN "claveServicio" SOLO SI EXISTE

        # VER EL FOLIO QUE VAMOS A UTILIZAR PARA LA NOTA Y TODOS LOS SERVICIOS QUE ELIJA
        # SI ELIJE MAS DE 1 SERVICIO, LA CLAVE O FOLIO SERA EL MISMO

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
                        cursor.execute(f"SELECT * FROM SERVICIOS WHERE clave = {clave_servicio}")
                        resultado = cursor.fetchone()
                        print(f"Se agregó: {resultado[1]}")

                        #############
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
                        #############
                        if resultado is None:
                            print("No existe esa clave de servicio. Intente de nuevo")
                            continue
                        else:
                            costo = resultado[2]
                            # HACER EL INSERT EN ESTA LINEA CON TODOS LOS DATOS AL MOMENTO
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
    print("*"*30)
    try:
        while True:
            op = int(input("(1) Registrar una nota."
                           "\n(2) Cancelar una nota."
                           "\n(3) Recuperar una nota."
                           "\n(4) Consultas y reportes."
                           "\n(5) Volver al menu principal.\n>>"))
            if not op in (1,2,3,4,5):
                print("No es una opcion valida.")
                continue
            elif op == 1:
                registrar_nota()
                break
            elif op==2:
                cancelar_nota()
                break
    except sqlite3.Error as e:
        print("Error en la entrada de datos. ", e)

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
    folio_cancelar = int(input("Ingresa el folio a cancelar\n>>"))
    conn = sqlite3.connect("TALLER_MECANICO.db")
    cursor = conn.cursor()
    #cursor.execute(f'UPDATE NOTAS SET cancelada = 1 WHERE folio = {folio_cancelar};')

    #print("Nota cancelada con exito.")

    cursor.execute(f'SELECT ')
    conn.commit()
    conn.close()


    menuNotas()

def recuperar_nota():
    # Lógica para recuperar una nota cancelada
    pass


def consulta_por_periodo():
    # Lógica para consultar notas por período
    pass


def consulta_por_folio():
    # Lógica para consultar notas por folio
    pass

# Menú Clientes
def menuClientes():
    print("*" * 30)
    print("\tMenu Clientes\n")
    while True:
        print("1. Agregar un cliente")
        print("2. Consultas y reportes")
        print("3. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_cliente()
            break
        elif opcion == "2":
            menuConsultasyReportesCLIENTES()
            break
        elif opcion == "3":
            menu_principal()
            break
def agregar_cliente():
    print("*" * 30)
    print("\tAgregar cliente\n")
    while True:
        patronNombre = r'[A-Za-z ]{3,}'
        C_nombreCliente = input("Ingrese su nombre completo\n>>")
        if not bool(re.match(patronNombre, C_nombreCliente.lower())) or len(C_nombreCliente.split()) == 0:
            print("!" * 30)
            print("No debe ser vacio, numerico, ni debe tener solo espacios en blanco.")
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
    print("Registro agregado correctamente.")
    menuClientes()
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
    try:
        while True:
            print("Ingresa la clave del cliente a buscar")
            try:
                claveBuscar = int(input(">>"))
            except:
                print("Regresando...")
                menuConsultasyReportesCLIENTES()
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM CLIENTES WHERE clave={claveBuscar}")
            resultado = cursor.fetchall()
            if resultado is None or len(resultado)==0:
                print("No hay datos de la clave ingresada, intenta con una existente")
                continue

            print("*"*30)
            print(f"Clave: {resultado[0][0]}")
            print(f"Nombre: {resultado[0][1]}")
            print(f"RFC: {resultado[0][2]}")
            print(f"Correo: {resultado[0][3]}")
            print("*" * 30)

            conn.commit()
            conn.close()
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

            # Consulta SQL para filtrar por nombre
            consulta = "SELECT * FROM clientes WHERE nombre LIKE ?"
            # Ejecutar la consulta con el parámetro del nombre buscado
            cursor.execute(consulta, ('%' + nombre + '%',))
            resultado = cursor.fetchall()
            if resultado[0] is None:
                print("No hay datos del nombre ingresado, intenta con uno existente")
                continue
            print("*" * 30)
            for i in resultado:
                print(f"Clave: {i[0]}\t| Nombre: {i[1]}\t| RFC: {i[2]}\t| Correo: {i[3]}")
            print("*" * 30)
            conn.commit()
            conn.close()
    except Exception as e:
        print("!" * 30)
        print("No se encontró el nombre.", e)
    pass
def listado_clientes_registrados():
    # Lógica para mostrar el listado de clientes
    print("*" * 30)
    datos_excel = [('Clave', 'Nombre', 'RFC', 'CORREO')]
    print("Selecciona.")
    try:
        op = int(input("1. Ordenado por clave\n"
                       "2. Ordenados por nombre\n"
                       "3. Volver al menú anterior\n>>"))
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
            elif op == 1:
                fechaActual1 = datetime.today()
                fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
                with open(f'ReporteClientesActivosPorClave_{fechahoy}.csv', 'w', newline='',
                          encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerows(datos_excel)
                    print("Exportado correctamente.")
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
# Menú Servicios
def mostrarServicios():
    while True:
        print("*" * 30)
        print("\tBusqueda por clave")
        conn = sqlite3.connect("TALLER_MECANICO.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SERVICIOS ORDER BY clave")
        resultado = cursor.fetchall()
        print("*" * 30, "\nListado:")
        for clave, nombreServicio, costo in resultado:
            print(f"Clave: {clave}\t{nombreServicio}")
        print("*" * 30)
        conn.commit()
        conn.close()
        break
def agregar_servicio():
    # Lógica para agregar un nuevo servicio
    while True:
        validar = r'\d'
        print("*"*30)
        print("\tAgregar Servicio")
        S_nombre = input("Ingrese nombre del servicio: ")
        if len(S_nombre.split())==0:
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
            if len(str(costo).split())==0 or costo+costo == 0.0:
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
        if not len(resultado)==0:
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

            # Consulta SQL para filtrar por nombre
            consulta = "SELECT * FROM SERVICIOS WHERE nombreServicio LIKE ?"
            # Ejecutar la consulta con el parámetro del nombre buscado
            cursor.execute(consulta, ('%' + nombre + '%',))
            resultado = cursor.fetchall()
            if len(resultado)<1:
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
    # Lógica para mostrar el listado de clientes
    print("*" * 30)
    datos_excel = [('Clave', 'Servicio', 'Costo')]
    print("Selecciona.")
    try:
        op = int(input("1. Ordenado por clave\n"
                       "2. Ordenados por nombre de servicio\n"
                       "3. Volver al menú anterior\n>>"))
        if op == 1:
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM SERVICIOS ORDER BY clave")
            resultado = cursor.fetchall()
            print("*" * 30)
            for clave, nombreServicio, costo,  in resultado:
                print(f"Clave: {clave}\t|\t{nombreServicio}\t|\t${costo}")
                datos_excel.append((clave, nombreServicio, costo ))
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
            for clave, nombreServicio, costo,  in resultado:
                print(f"Clave: {clave}\t|\t{nombreServicio}\t|\t${costo} ")
                datos_excel.append((clave, nombreServicio, costo ))
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
        print("2. Consultas y reportes")
        print("3. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_servicio()
            break
        elif opcion == "2":
            menuConsultasyReportesSERVICIOS()
            break
        elif opcion == "3":
            menu_principal()
            break
# Menú principal
def menu_principal():
    while True:
        print("*" * 30)
        print("Menú Principal")
        print("1. Menú Notas")
        print("2. Menú Clientes")
        print("3. Menú Servicios")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menuNotas()
            break
        elif opcion == "2":
            menuClientes()
            break
        elif opcion == "3":
            # Lógica del menú de servicios
            menuServicios()
            break
        elif opcion == "4":
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
# Ejecución del programa
menu_principal()
