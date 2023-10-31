# BASE DE DATOS
import sys, sqlite3, re, os, pandas as pd, csv
from sqlite3 import Error
from datetime import datetime

base_datos = 'TALLER_MECANICO.db'
if not os.path.isfile(base_datos):
    try:
        with sqlite3.connect("TALLER_MECANICO.db") as conn:
            # CONEXION  conn = sqlite3.connect("TALLER_MECANICO")
            mi_cursor = conn.cursor()
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS CLIENTES \
            (clave INTEGER PRIMARY KEY, nombre TEXT NOT NULL, rfc TEXT NOT NULL, correo TEXT NOT NULL);")
            if mi_cursor:
                print("Tabla creada exitosamente")
    except Error as e:
        print (e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")




# Menú Notas
def registrar_nota():
    # Lógica para registrar una nueva nota
    pass

def cancelar_nota():
    # Lógica para cancelar una nota
    pass

def recuperar_nota():
    # Lógica para recuperar una nota cancelada
    pass

def consulta_por_periodo():
    # Lógica para consultar notas por período
    pass

def consulta_por_folio():
    # Lógica para consultar notas por folio
    pass

###################### Menú Clientes
'''Variables CLIENTES'''
clientes = []
C_nombreCliente = ""
C_RFC = ""
C_correo = ""

def menuClientes():
    print("*"*30)
    while True:
        print("1. Agregar un cliente")
        print("2. Consultas y reportes de clientes")
        print("3. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        print("*" * 30)
        if opcion == "1":
            agregar_cliente()
            pass
        elif opcion == "2":
            menuConsultasyReportes()
            pass
        elif opcion == "3":
            menu_principal()
            pass

def agregar_cliente():
    print("*" * 30)
    while True:
        patronNombre = r'[A-Za-z ]{3,}'
        C_nombreCliente = input("Ingrese su nombre completo\n>>")
        if not bool(re.match(patronNombre, C_nombreCliente.lower())) or len(C_nombreCliente.split()) == 0:
            print("!" * 30)
            print("No debe ser vacio, numerico, ni debe tener solo espacios en blanco.")
            continue
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
        claveMax=0
    else:
        claveMax = resultado[0] + 1
    cursor.execute(f"INSERT INTO CLIENTES VALUES({claveMax},'{C_nombreCliente}','{C_RFC}','{C_correo}')")
    conn.commit()
    conn.close()

def menuConsultasyReportes():
    print("*" * 30)
    while True:
        print("1. Listado de clientes registrados")
        print("2. Busqueda por clave")
        print("3. Busqueda por nombre")
        print("4. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            listado_clientes_registrados()
            pass
        elif opcion == "2":
            busquedaPorClave()
            pass
        elif opcion == "3":
            busquedaPorNombre()
            pass
        elif opcion == "4":
            menuClientes()
            pass

def busquedaPorClave():
    print("*" * 30)
    try:
        while True:
            print("Ingresa la clave del cliente a buscar")
            claveBuscar = int(input(">>"))
            if len(claveBuscar.split())==0:
                menu_principal()
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM CLIENTES WHERE clave={claveBuscar}")
            resultado = cursor.fetchall()
            if resultado[0] is None:
                print("No hay datos de la clave ingresada, intenta con una existente")
                continue
            for i in resultado:
                print(f"Clave: {i[0]}")
                print(f"Nombre: {i[1]}")
                print(f"RFC: {i[2]}")
                print(f"Correo: {i[3]}")
            conn.commit()
            conn.close()
    except Exception as e:
        print("!" * 30)
        print("Debe ser un valor numerico, y no debe estar vacio.", e)


def busquedaPorNombre():
    print("*" * 30)
    try:
        while True:
            print("Ingresa el nombre del cliente a buscar")
            nombre = input(">>")
            if nombre.split()=="":
                menu_principal()
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
    datos_excel =[('Clave','Nombre','RFC','CORREO')]
    print("Selecciona.")
    try:
        op = int(input("1. Ordenado por clave\n"
                       "2. Ordenados por nombre\n"
                       "3. Volver al menú anterior\n>>"))
        if op==1:
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CLIENTES ORDER BY clave")
            resultado = cursor.fetchall()
            print("*" * 30)
            for clave,nombre,rfc,correo in resultado:
                print(f"Clave: {clave}\t{nombre}\t{rfc}\t{correo}")
                datos_excel.append((clave,nombre,rfc,correo))
            print("*" * 30)
            conn.commit()
            conn.close()
        elif op==2:
            conn = sqlite3.connect("TALLER_MECANICO.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CLIENTES ORDER BY nombre")
            resultado = cursor.fetchall()
            print("*" * 30)
            for clave,nombre,rfc,correo in resultado:
                print(f"Clave: {clave}\t{nombre}\t{rfc}\t{correo}")
                datos_excel.append((clave, nombre, rfc, correo))
            print("*" * 30)
            conn.commit()
            conn.close()
        elif op == 3:
            menuConsultasyReportes()

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
        elif op == 1:
            fechaActual1 = datetime.today()
            fechahoy = datetime.strftime(fechaActual1, '%m-%d-%Y')
            with open(f'ReporteClientesActivosPorClave_{fechahoy}.csv', 'w', newline='', encoding='utf-8') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerows(datos_excel)
        listado_clientes_registrados()
    except Exception as e:
        print("!" * 30)
        print("Error en la entrada de datos. Vuelva a intentarlo con los numeros 1, 2 o 3.")
        print(e)
    pass

# Menú Servicios
def agregar_servicio():
    # Lógica para agregar un nuevo servicio
    pass

def busqueda_por_clave_servicio():
    # Lógica para buscar un servicio por clave
    pass

def busqueda_por_nombre_servicio():
    # Lógica para buscar un servicio por nombre
    pass

def listado_servicios():
    # Lógica para mostrar el listado de servicios
    pass

# Menú principal
def menu_principal():
    while True:
        print("Menú Principal")
        print("1. Menú Notas")
        print("2. Menú Clientes")
        print("3. Menú Servicios")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":

            pass
        elif opcion == "2":
            menuClientes()

            pass
        elif opcion == "3":
            # Lógica del menú de servicios
            pass
        elif opcion == "4":
            confirmacion = int(input("¿Está seguro que desea salir? (1. Sí/2. No): "))
            if confirmacion==1:
                print("Saliendo del programa...")
                break
            elif confirmacion==2:
                continue
            else:
                print("Opción no válida. Regresando al menú principal.")
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecución del programa
menu_principal()
