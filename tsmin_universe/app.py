from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from logic.operaciones import (
    obtener_servicios,
    buscar_servicio,
    obtener_cartelera,
    buscar_pelicula,
    calcular_total_carrito,
    crear_matriz_asientos,
    generar_reporte,
    obtener_categorias_servicio,
    filtrar_productos_servicio,
    buscar_productos_global,
    obtener_estructuras_aplicadas,
    obtener_procesos_algoritmicos,
    obtener_producto_mayor_precio,
    obtener_producto_menor_precio
)

app = Flask(__name__)
app.secret_key = "tsmin_universe_secret_key"


@app.before_request
def iniciar_sesion():
    if "carrito" not in session:
        session["carrito"] = []

    if "reservas" not in session:
        session["reservas"] = []

    if "asientos_reservados" not in session:
        session["asientos_reservados"] = []


@app.context_processor
def variables_globales():
    carrito = session.get("carrito", [])

    return {
        "cantidad_carrito": len(carrito)
    }


@app.route("/")
def index():
    servicios = obtener_servicios()
    cartelera = obtener_cartelera()[:3]

    return render_template(
        "index.html",
        servicios=servicios,
        cartelera=cartelera
    )


@app.route("/servicio/<servicio_id>")
def servicio(servicio_id):
    servicio_actual = buscar_servicio(servicio_id)

    if servicio_actual is None:
        flash("El servicio solicitado no existe.", "error")
        return redirect(url_for("index"))

    categoria = request.args.get("categoria", "todos")
    ordenar = request.args.get("ordenar", "")

    productos_filtrados = filtrar_productos_servicio(
        servicio_id=servicio_id,
        categoria=categoria,
        ordenar=ordenar
    )

    categorias = obtener_categorias_servicio(servicio_id)

    return render_template(
        "servicio.html",
        servicio=servicio_actual,
        productos=productos_filtrados,
        categorias=categorias,
        categoria_actual=categoria,
        ordenar_actual=ordenar
    )


@app.route("/buscar")
def buscar():
    consulta = request.args.get("q", "").strip()
    ordenar = request.args.get("ordenar", "")

    resultados = buscar_productos_global(
        consulta=consulta,
        ordenar=ordenar
    )

    return render_template(
        "busqueda.html",
        consulta=consulta,
        resultados=resultados,
        ordenar_actual=ordenar
    )


@app.route("/agregar-carrito", methods=["POST"])
def agregar_carrito():
    servicio_id = request.form.get("servicio_id")
    nombre = request.form.get("nombre")
    tipo = request.form.get("tipo")
    precio = float(request.form.get("precio", 0))
    cantidad = int(request.form.get("cantidad", 1))

    servicio_actual = buscar_servicio(servicio_id)

    if servicio_actual is None:
        flash("No se pudo agregar el producto.", "error")
        return redirect(url_for("index"))

    if cantidad <= 0:
        flash("La cantidad debe ser mayor a cero.", "error")
        return redirect(url_for("servicio", servicio_id=servicio_id))

    carrito = session.get("carrito", [])

    carrito.append({
        "servicio_id": servicio_id,
        "servicio": servicio_actual["nombre"],
        "nombre": nombre,
        "tipo": tipo,
        "precio": precio,
        "cantidad": cantidad
    })

    session["carrito"] = carrito

    flash(f"{nombre} fue agregado al carrito.", "success")
    return redirect(url_for("servicio", servicio_id=servicio_id))


@app.route("/carrito")
def carrito():
    carrito_actual = session.get("carrito", [])
    total = calcular_total_carrito(carrito_actual)

    return render_template(
        "carrito.html",
        carrito=carrito_actual,
        total=total
    )


@app.route("/vaciar-carrito", methods=["POST"])
def vaciar_carrito():
    session["carrito"] = []
    flash("El carrito fue vaciado correctamente.", "success")
    return redirect(url_for("carrito"))


@app.route("/cine")
def cine():
    cartelera = obtener_cartelera()

    return render_template(
        "cine.html",
        cartelera=cartelera
    )


@app.route("/reserva/<int:pelicula_id>", methods=["GET", "POST"])
def reserva(pelicula_id):
    pelicula = buscar_pelicula(pelicula_id)

    if pelicula is None:
        flash("La película solicitada no existe.", "error")
        return redirect(url_for("cine"))

    asientos_reservados = session.get("asientos_reservados", [])

    if request.method == "POST":
        asientos_seleccionados = request.form.getlist("asientos")

        if not asientos_seleccionados:
            flash("Selecciona al menos un asiento.", "error")
            return redirect(url_for("reserva", pelicula_id=pelicula_id))

        nuevos_asientos = []

        for asiento in asientos_seleccionados:
            clave = f"{pelicula_id}:{asiento}"

            if clave not in asientos_reservados:
                asientos_reservados.append(clave)
                nuevos_asientos.append(asiento)

        if not nuevos_asientos:
            flash("Los asientos seleccionados ya fueron reservados.", "error")
            return redirect(url_for("reserva", pelicula_id=pelicula_id))

        reservas = session.get("reservas", [])

        reservas.append({
            "pelicula": pelicula["titulo"],
            "sala": pelicula["sala"],
            "hora": pelicula["hora"],
            "asientos": nuevos_asientos,
            "cantidad": len(nuevos_asientos),
            "total": round(len(nuevos_asientos) * pelicula["precio"], 2)
        })

        session["asientos_reservados"] = asientos_reservados
        session["reservas"] = reservas

        flash("Reserva realizada correctamente.", "success")
        return redirect(url_for("reportes"))

    matriz_asientos = crear_matriz_asientos(pelicula_id, asientos_reservados)

    return render_template(
        "reserva.html",
        pelicula=pelicula,
        matriz_asientos=matriz_asientos
    )


@app.route("/reportes")
def reportes():
    carrito_actual = session.get("carrito", [])
    reservas = session.get("reservas", [])
    asientos_reservados = session.get("asientos_reservados", [])

    reporte = generar_reporte(
        carrito=carrito_actual,
        reservas=reservas,
        asientos_reservados=asientos_reservados
    )

    return render_template(
        "reportes.html",
        reporte=reporte,
        reservas=reservas
    )


@app.route("/algoritmos")
def algoritmos():
    estructuras = obtener_estructuras_aplicadas()
    procesos = obtener_procesos_algoritmicos()
    producto_mayor = obtener_producto_mayor_precio()
    producto_menor = obtener_producto_menor_precio()

    return render_template(
        "algoritmos.html",
        estructuras=estructuras,
        procesos=procesos,
        producto_mayor=producto_mayor,
        producto_menor=producto_menor
    )


@app.route("/api/servicios")
def api_servicios():
    return jsonify(obtener_servicios())


if __name__ == "__main__":
    app.run(debug=True)