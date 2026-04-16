from datetime import datetime
import json

inventario=[] 
registro=[] 
bodegas={
    1: "norte",
    2: "centro",
    3: "Oriente"
}
def json_registro():
    datos_completos={
        "registro_productos": registro
    }
    with open("datos_registro.json", "w") as archivo:
        json.dump(datos_completos, archivo)
        print(" DATOS GUARDADOS EN JSON ")

def json_inventario(inventario):
    datos_completos={
        "registro_productos": inventario
    }
    with open("datos_inventario.json", "w") as archivo:
        json.dump(datos_completos, archivo)
        print(" DATOS GUARDADOS EN JSON ")

def json_historial(historial):
    datos_completos={
        "historial_productos": historial
    }
    with open("datos_historial.json", "w") as archivo:
        json.dump(datos_completos,archivo)
        print(" DATOS GUARDADOS EN JSON ")
####
def cargar_datos_registro():
    try:
        with open("datos_registro.json", "r") as archivo:
            return json.load(archivo)
    except:
        return[]
def cargar_datos_inventario():
    try:
        with open("datos_inventario.json", "r") as archivo:
            return json.load(archivo)
    except:
        return[]
def cargar_datos_historial():
    try:
        with open("datos_historial.json","r" ) as archivo:
            datos=json.load(archivo)
            return datos["historial_productos"]
    except:
        return[]
historial=cargar_datos_historial()
#
def registros():
    print(" SISTEMA REGISTRO DE PRODUCTO  ")
    producto=input("Ingrese nombre su producto: ")
    codigo=int(input("Ingrese codigo del producto: "))
    proveedor=input("Ingrese proveedor del producto: ")
    datos={
        "codigo": codigo,
        "producto":producto,
        "proveedor": proveedor
    }
    registro.append(datos)
    print(" PRODUCTO REGISTRADO ")
    json_registro()
#
def ingresar_inventario():
    datos=cargar_datos_registro()
    registro=datos["registro_productos"]
    print("   SISTEMA INGRESO PRODUCTOS AL INVENTARIO  ")
    codigo=int(input("Ingrese el codigo del producto: "))
    print(registro) 
    codigo_encontrado=None
    for item in registro:
        if item["codigo"]==codigo:
            codigo_encontrado=item
            break 
    if codigo_encontrado:
            print(" CODIGO VALIDO ")
            print("1.norte\n2.centro\n3.oriente")
            bodega_opcion=int(input("Ingrese bodega: "))
            if bodega_opcion in bodegas:
             bodegas_guardar=bodegas[bodega_opcion] 
             stock=int(input("Ingrese stock del producto: "))
             descripcion=input("Ingrese descripcion del producto: ")
             datos_bodega={
                 "codigo": codigo,
                 "descripcion": descripcion,
                 "bodega": bodega_opcion,
                 "stock": stock
             }
             inventario.append(datos_bodega)
            else:
                print("NO HAY MAS BODEGAS")
                return
            ahora=datetime.now().strftime("%m-%d-%H-%M")
            print(f"codigo: {codigo}, esta en la bodega: {bodegas_guardar}, su stock es: {stock}")
            print(f"fecha y hora actual: {ahora}")
            print(" PRODUCTO INGRESADO ")
            json_inventario(inventario)

            movimiento_ingreso={
                "codigo": codigo,
                "producto": codigo_encontrado["producto"],
                "bodega": bodegas_guardar,
                "stock": stock,
                "tipo": "entrada",
                "descripcion": descripcion,
                "fecha": ahora
            }
            historial.append(movimiento_ingreso)
            json_historial(historial)
    else:
        print("CODIGO NO EXISTE, NO SE PUEDE EJECUTAR")
##
def sacar_del_inventario():
    datos=cargar_datos_inventario()
    inventario=datos["registro_productos"]
    print("  SISTEMA RETIRO DE PRODUCTOS " )
    codigo=int(input("Ingrese el codigo del producto: "))
    print(inventario)
    codigo_encontrado=None
    for item in inventario:
        if item["codigo"]==codigo:
            codigo_encontrado=item
            break 
    if codigo_encontrado:
                print("1.norte\n2.centro\n3.oriente")
                bodega_op=int(input("De que bodega desea retirar el producto: "))
                if codigo_encontrado["bodega"]!=bodega_op:
                    print(" PRODUCTO NO ESTA EN BODEGA ")
                    return
                cantidades=int(input("Ingrese cantidad a retirar: "))
                stock=codigo_encontrado["stock"]
                if cantidades<=stock:
                    stock-=cantidades
                    codigo_encontrado["stock"]=stock
                    print(" RETIRO VALIDO ")
                    json_inventario(inventario)
                    datos_registro= cargar_datos_registro()["registro_productos"]
                    nombre_producto=""
                    movimientos_retiro = {}
                    for item in datos_registro:
                        if item["codigo"]==codigo:
                            nombre_producto=item["producto"]
                            break
                    ahora=datetime.now().strftime("%m-%d-%H-%M")
                    print(f"fecha y hora actual: {ahora}")
                
                    movimientos_retiro={
                        "codigo": codigo,
                        "producto": nombre_producto,
                        "bodega": bodegas[bodega_op],
                        "tipo":"salida",
                        "stock": stock,
                        "descripcion": codigo_encontrado["descripcion"],
                        "fecha": ahora
                    }
                    historial.append(movimientos_retiro)
                    json_historial(historial)
                else:
                    print(" RETIRO NO VALIDO ")
                    return
    else:
        print("CODIGO NO EXISTE, NO SE PUEDE EJECUTAR")
#
def buscar_producto():
    datos1=cargar_datos_registro()
    datos2=cargar_datos_inventario()
    registro=datos1["registro_productos"]
    inventario=datos2["registro_productos"]
    print("  SISTEMA DE BUSQUEDA PRODUCTOS " )
    codigo=int(input("Ingrese el codigo del producto: "))

    codigo_encontrado=None
    for item in inventario:
        if item["codigo"]==codigo:
            codigo_encontrado=item
            break 
    if codigo_encontrado:
           cantidad=codigo_encontrado["cantidad"]
           print(inventario)
           print(registro)
           print(f"Cantidades del producto: ", cantidad)
#

def visualizar_historial():
    print("  SISTEMA DE HISTORIAL DE PRODUCTOS " )
    codigo=int(input("Ingrese el codigo del producto: "))
    datos_historial= cargar_datos_historial()
    codigos_existente=[item["codigo"] for item in datos_historial]
    if codigo not in codigos_existente:
        print("CODIGO NO EXISTE, NO SE PUEDE EJECUTAR")
        return

    print("1.norte\n2.centro\n3.oriente")
    bodega_opcion=int(input("Ingrese bodega: "))
    if bodega_opcion not in bodegas:
        print(" NO EXISTE BODEGA ")
        return 
    bodegas_guardar=bodegas[bodega_opcion] 

    encontrar=[]
    for item in datos_historial:
        if item["codigo"] == codigo and item["bodega"]== bodegas_guardar:
            encontrar.append(item)
    if not encontrar: 
        print(" NO SE ENCONTRO NADA ")
        return
    
    print(f"\n HISTORIAL DE MOVIMIENTOS \n CODIGO {codigo} DE LA BODEGA, {bodegas_guardar}")
    for item in encontrar:
        print("Tipo:", item["tipo"])
        print("Descripcion:", item["descripcion"])
        print("fecha", item["fecha"])
#
def reporte_productos():
    datos_registro=cargar_datos_registro()
    datos_inventario=cargar_datos_inventario()

    if not datos_registro or not datos_inventario:
        print("NO HAY DATOS DISPONIBLES")
        return

    registro = datos_registro["registro_productos"]
    inventario = datos_inventario["registro_productos"]

    if not registro or not inventario:
        print("NO HAY PRODUCTOS REGISTRADOS EN EL INVENTARIO")
        return

    print(" SISTEMA DE REPORTE DE PRODUCTOS ")
    reporte_productos = {}

    for item in inventario:
        codigo = item["codigo"]
        bodega_num = item["bodega"]
        stock = item["stock"]

        nombre_producto = "desconocido"
        for items in registro:
            if items["codigo"] == codigo: 
                nombre_producto = items["producto"]
                break

        if codigo not in reporte_productos:
            reporte_productos[codigo] = {
                "producto": nombre_producto,
                "total_stock": 0,
                "bodegas": {},
                }
        reporte_productos[codigo]["total_stock"] += stock
        reporte_productos[codigo]["bodegas"][bodegas[bodega_num]] = {
            "stock": stock
        }
    archivo_txt = []
    archivo_txt.append(" REPORTE GENERAL DE INVENTARIO ")
    for codigo, info in reporte_productos.items():
        archivo_txt.append(f"Codigo: {codigo} | Producto: {info['producto']}")
        archivo_txt.append(f" Total stock: {info['total_stock']}")
        for nombre_bodega, datos_bodega in info["bodegas"].items():
            archivo_txt.append(f" -{nombre_bodega}: stock={datos_bodega['stock']}")

    for linea in archivo_txt:
        print(linea)

    guardar = input("Desea guardar el reporte en un archivo? (s/n): ").strip().lower()
    if guardar == "s":
        nom_archivo = f"reporte.txt"
        with open(nom_archivo, "w") as archivo:
            for linea in archivo_txt:
                archivo.write(linea + "\n")
        print(f" REPORTE GUARDADO COMO: {nom_archivo} ")
    else:
        print(" REPORTE NO GUARDADO ")

def transferir_producto():
   datos = cargar_datos_inventario()
   inventario = datos["registro_productos"]
   codigo = int(input("Ingrese el codigo del producto: "))
   bodega_origen = int(input("Ingrese bodega de origen: "))
   for item in inventario:
    if item["bodega"] != bodega_origen:
        print(" PRODUCTO NO ESTA EN BODEGA ")
        return
   bodega_destino = int(input("Ingrese bodega de destino: "))
   cantidad = int(input("Ingrese la cantidad a transferir: "))
   for item in inventario:
        if item["codigo"] == codigo and item["bodega"] == bodega_origen:
            if item["stock"] < cantidad:
                print(" NO HAY SUFICIENTE STOCK ")
                return
            
            item["stock"] -= cantidad
            destino_encontrado = None
            for i in inventario:
                if i["codigo"] == codigo and i["bodega"] == bodega_destino:
                    destino_encontrado = i
                    break
                
            if destino_encontrado:
                destino_encontrado["stock"] += cantidad
            else:
                inventario.append({
                    "codigo": codigo,
                    "bodega": bodega_destino,
                    "stock": cantidad,
                    "descripcion": item["descripcion"],
                })

                Movimiento_transferencia=({
                    "codigo": codigo,
                    "tipo": "TRANSFERENCIA",
                    "bodega": bodega_destino,
                    "stock": cantidad,
                    "descripcion": item["descripcion"]

                })
            
            historial.append(Movimiento_transferencia)
            json_inventario(inventario)
            json_historial(historial)
            print("TRANSFERENCIA REALIZADA")
            return
    
        print("PRODUCTO NO ENCONTRADO")

while True: 
    print("   GESTOR INVENTARIO ACME   ")
    print("------MENU PRINCIPAL-----")
    print("1. PRODUTOS\n2. REPORTE E HISTORIAL")
    opcion=int(input("Que opciones deseas: "))
    if opcion == 1:
            print("- 1.Registrar productos,\n- 2.Ingresar productos al inventario\n- 3.Retirar productos del inventario\n- 4.Buscar productos\n- 5.Transferir entre bodegas\n- 6. SALIR -")
            opcion=int(input("Que opcion deseas: "))
            match opcion:
                case 1:
                    print("Deseas ingresar a Registrar producto: ")
                    decision=int(input("1. SI - 2. NO: "))
                    if decision == 1:
                        registros()
                    else:
                        print("SALISTE DE REGISTRAR PRODUCTOS")
                    
                case 2: 
                    print("Deseas ingresar productos al inventario: ")
                    decision=int(input("1. SI - 2. NO"))
                    if decision == 1:
                        ingresar_inventario()
                    else:
                        print("SALISTE DE INGRESAR PRODUCTOS")
                        
                case 3:
                    print("Deseas Retirar productos del inventario: ")
                    decision=int(input("1. SI - 2. NO: "))
                    if decision == 1:
                        sacar_del_inventario()
                    else:
                        print("SALISTE DE RETIRAR PRODUCTOS")
                        
                case 4:
                    print("Deseas Buscar productos: ")
                    decision=int(input("1. SI - 2. NO"))
                    if decision == 1:
                        buscar_producto()
                    else:
                        print("SALISTE DE BUSCAR PRODUCTOS")
                        
                case 5:
                    print("Deseas Transferir entre bodegas: ")
                    decision=int(input("1. SI - 2. NO"))
                    if decision == 1:
                        transferir_producto()
                    else:
                        print("SALISTE DE TRANSFERENCIA ENTRE BODEGAS")
                case 6:
                    print("-- SALIENDO DEL PROGRAMA --")
                    break 
                
    elif opcion == 2:
            print("- 1. historial de productos\n- 2. reporte de productos\n3.SALIR")
            opcion=int(input("Que opcion deseas: "))
            match opcion:
                case 1:
                    print("Deseas ver el Historial de productos: ")
                    decision=int(input("1. SI - 2. NO: "))
                    if decision == 1:
                        visualizar_historial()
                    else:
                         print("SALISTE DE HISTORIAL PRODUCTOS")
                         
                case 2:
                    print("Deseas ver reporte de los productos: ")
                    decision=int(input("1. SI - 2. NO"))
                    if decision == 1:
                        reporte_productos()
                    else:
                        print("SALISTE DE INGRESAR PRODUCTOS")
                        
                case 3:
                    print("-- SALIENDO DEL PROGRAMA --")
                    break 
    else: 
        print(" NO HICISTE NADA ")
                
        