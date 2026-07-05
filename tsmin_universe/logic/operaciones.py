from data.datos import SERVICIOS, CARTELERA, EVENTOS


def obtener_servicios():
    return SERVICIOS


def buscar_servicio(servicio_id):
    for servicio in SERVICIOS:
        if servicio["id"] == servicio_id:
            return servicio

    return None


def obtener_cartelera():
    return CARTELERA


def buscar_pelicula(pelicula_id):
    for pelicula in CARTELERA:
        if pelicula["id"] == pelicula_id:
            return pelicula

    return None


def calcular_total_carrito(carrito):
    total = 0

    for item in carrito:
        total += item["precio"] * item["cantidad"]

    return round(total, 2)


def calcular_total_reservas(reservas):
    total = 0

    for reserva in reservas:
        total += reserva.get("total", 0)

    return round(total, 2)


def contar_productos():
    total = 0

    for servicio in SERVICIOS:
        total += len(servicio["productos"])

    return total


def calcular_inventario_total():
    total_stock = 0

    for servicio in SERVICIOS:
        for producto in servicio["productos"]:
            total_stock += producto["stock"]

    return total_stock


def obtener_todos_los_productos():
    productos = []

    for servicio in SERVICIOS:
        for producto in servicio["productos"]:
            productos.append({
                "servicio_id": servicio["id"],
                "servicio": servicio["nombre"],
                "marca": servicio["marca"],
                "nombre": producto["nombre"],
                "tipo": producto["tipo"],
                "precio": producto["precio"],
                "stock": producto["stock"]
            })

    return productos


def ordenar_productos(productos, ordenar):
    productos_ordenados = list(productos)

    if ordenar == "precio_asc":
        productos_ordenados.sort(key=lambda producto: producto["precio"])

    elif ordenar == "precio_desc":
        productos_ordenados.sort(key=lambda producto: producto["precio"], reverse=True)

    elif ordenar == "stock_desc":
        productos_ordenados.sort(key=lambda producto: producto["stock"], reverse=True)

    elif ordenar == "nombre_asc":
        productos_ordenados.sort(key=lambda producto: producto["nombre"].lower())

    return productos_ordenados


def obtener_categorias_servicio(servicio_id):
    servicio = buscar_servicio(servicio_id)

    if servicio is None:
        return []

    categorias = []

    for producto in servicio["productos"]:
        if producto["tipo"] not in categorias:
            categorias.append(producto["tipo"])

    categorias.sort()

    return categorias


def filtrar_productos_servicio(servicio_id, categoria="todos", ordenar=""):
    servicio = buscar_servicio(servicio_id)

    if servicio is None:
        return []

    productos = list(servicio["productos"])

    if categoria and categoria != "todos":
        productos = [
            producto for producto in productos
            if producto["tipo"].lower() == categoria.lower()
        ]

    productos = ordenar_productos(productos, ordenar)

    return productos


def buscar_productos_global(consulta, ordenar=""):
    if not consulta:
        return []

    consulta = consulta.lower()
    productos = obtener_todos_los_productos()
    resultados = []

    for producto in productos:
        texto_busqueda = (
            producto["nombre"] + " " +
            producto["tipo"] + " " +
            producto["servicio"] + " " +
            producto["marca"]
        ).lower()

        if consulta in texto_busqueda:
            resultados.append(producto)

    resultados = ordenar_productos(resultados, ordenar)

    return resultados


def obtener_producto_mayor_precio():
    productos = obtener_todos_los_productos()

    if not productos:
        return None

    producto_mayor = productos[0]

    for producto in productos:
        if producto["precio"] > producto_mayor["precio"]:
            producto_mayor = producto

    return producto_mayor


def obtener_producto_menor_precio():
    productos = obtener_todos_los_productos()

    if not productos:
        return None

    producto_menor = productos[0]

    for producto in productos:
        if producto["precio"] < producto_menor["precio"]:
            producto_menor = producto

    return producto_menor


def calcular_precio_promedio_productos():
    productos = obtener_todos_los_productos()

    if not productos:
        return 0

    suma = 0

    for producto in productos:
        suma += producto["precio"]

    promedio = suma / len(productos)

    return round(promedio, 2)


def crear_matriz_asientos(pelicula_id, asientos_reservados=None):
    if asientos_reservados is None:
        asientos_reservados = []

    filas = ["A", "B", "C", "D", "E", "F"]
    columnas = range(1, 9)

    matriz = []

    for fila in filas:
        fila_asientos = []

        for columna in columnas:
            codigo = f"{fila}{columna}"
            clave = f"{pelicula_id}:{codigo}"

            if clave in asientos_reservados:
                estado = "ocupado"
            else:
                estado = "libre"

            fila_asientos.append({
                "codigo": codigo,
                "estado": estado
            })

        matriz.append(fila_asientos)

    return matriz


def generar_resumen_servicios():
    resumen = []

    for servicio in SERVICIOS:
        total_productos = len(servicio["productos"])
        stock_total = sum(producto["stock"] for producto in servicio["productos"])

        resumen.append({
            "nombre": servicio["nombre"],
            "marca": servicio["marca"],
            "productos": total_productos,
            "stock": stock_total
        })

    return resumen


def generar_reporte(carrito, reservas, asientos_reservados):
    producto_mayor = obtener_producto_mayor_precio()
    producto_menor = obtener_producto_menor_precio()

    total_asientos_por_pelicula = 6 * 8
    total_asientos_sistema = len(CARTELERA) * total_asientos_por_pelicula
    asientos_ocupados = len(asientos_reservados)
    asientos_libres = total_asientos_sistema - asientos_ocupados

    return {
        "total_servicios": len(SERVICIOS),
        "total_productos": contar_productos(),
        "inventario_total": calcular_inventario_total(),
        "total_peliculas": len(CARTELERA),
        "total_eventos": len(EVENTOS),
        "total_carrito": calcular_total_carrito(carrito),
        "total_reservas_dinero": calcular_total_reservas(reservas),
        "items_carrito": len(carrito),
        "total_reservas": len(reservas),
        "asientos_reservados": asientos_ocupados,
        "asientos_libres": asientos_libres,
        "total_asientos_sistema": total_asientos_sistema,
        "precio_promedio": calcular_precio_promedio_productos(),
        "producto_mayor": producto_mayor,
        "producto_menor": producto_menor,
        "resumen_servicios": generar_resumen_servicios(),
        "eventos": EVENTOS
    }


def obtener_estructuras_aplicadas():
    return [
        {
            "estructura": "Lista de servicios",
            "uso": "Almacena las zonas principales de Ts’Min Universe.",
            "ejemplo": "Cafetería, Game Over, Heart, Cine y Plaza Central."
        },
        {
            "estructura": "Lista de diccionarios",
            "uso": "Organiza productos con nombre, tipo, precio y stock.",
            "ejemplo": "Cada producto contiene datos estructurados para ser procesados."
        },
        {
            "estructura": "Matriz de asientos",
            "uso": "Representa la disponibilidad del cine mediante filas y columnas.",
            "ejemplo": "Filas A-F y columnas 1-8."
        },
        {
            "estructura": "Diccionarios",
            "uso": "Permiten guardar información detallada de servicios, películas y reservas.",
            "ejemplo": "Cada película tiene título, género, sala, hora y precio."
        },
        {
            "estructura": "Sesiones",
            "uso": "Guardan temporalmente carrito, reservas y asientos ocupados.",
            "ejemplo": "El usuario puede agregar productos y reservar asientos."
        }
    ]


def obtener_procesos_algoritmicos():
    return [
        {
            "proceso": "Búsqueda de productos",
            "algoritmo": "Recorrido secuencial",
            "descripcion": "Se recorren todos los productos y se comparan con la palabra ingresada por el usuario."
        },
        {
            "proceso": "Filtrado por categoría",
            "algoritmo": "Condicional aplicado a listas",
            "descripcion": "Se seleccionan únicamente los productos que coinciden con el tipo elegido."
        },
        {
            "proceso": "Ordenamiento",
            "algoritmo": "Ordenamiento por clave",
            "descripcion": "Los productos se organizan por precio, stock o nombre."
        },
        {
            "proceso": "Cálculo de totales",
            "algoritmo": "Acumulador",
            "descripcion": "Se suman precios, cantidades, stock y valores de reservas."
        },
        {
            "proceso": "Reserva de asientos",
            "algoritmo": "Validación en matriz",
            "descripcion": "Cada asiento se identifica por una posición y se valida si está libre u ocupado."
        },
        {
            "proceso": "Reporte general",
            "algoritmo": "Procesamiento de datos",
            "descripcion": "El sistema resume servicios, productos, inventario, reservas y disponibilidad."
        }
    ]