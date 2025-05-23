from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
import json
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
CORS(app)

NOMBRE_ARCHIVO = "json/calificaciones.json"

if not os.path.exists(NOMBRE_ARCHIVO):
    with open(NOMBRE_ARCHIVO, "w") as txt:
        json.dump([], txt, indent=4)

def leer_datos():
    with open(NOMBRE_ARCHIVO, "r") as txt:
        return json.load(txt)

def guardar_datos(calificacion):
    with open(NOMBRE_ARCHIVO, "w") as txt:
        json.dump(calificacion, txt, indent=4)

@app.route('/insertar', methods=["POST"])
def insertar():
    datos = request.json
    print(datos)
    calificaciones = leer_datos()
    calificaciones.append(datos)
    guardar_datos(calificaciones)
    return {"mensaje": "OK"}

@app.route('/consultar', methods=["GET"])
def consultar_calificaciones():
    calificaciones = leer_datos()
    return jsonify(calificaciones)

@app.route("/grafica")
def grafica_ciudad():
    calificaciones = leer_datos()  # Aquí debes usar leer_datos()

    conteo = {}
    for i in calificaciones:
        ciudad = i.get("ciudadFavorita")
        if ciudad:
            if ciudad in conteo:
                conteo[ciudad] += 1
            else:
                conteo[ciudad] = 1

    ciudades = list(conteo.keys())
    cantidades = list(conteo.values())

    plt.figure(figsize=(10, 6))
    plt.bar(ciudades, cantidades, color="orange", edgecolor="green")
    plt.title("Ciudad Favorita")
    plt.xlabel("Ciudad")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=90)  # Gira las etiquetas del eje X para que no se encimen
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)
    return Response(img.getvalue(), mimetype="image/png")

@app.route("/grafica_tipo_viaje")
def grafica_tipo_viaje():
    calificaciones = leer_datos()
    
    conteo = {}
    for i in calificaciones:
        tipos = i.get("tipo_viaje")
        if tipos:
            if tipos in conteo:
                conteo[tipos] += 1
            else:
                conteo[tipos] = 1

    tipos = list(conteo.keys())
    cantidades = list(conteo.values())

    plt.figure(figsize=(8, 6))
    plt.bar(tipos, cantidades, color="lightgreen", edgecolor="black")
    plt.title("Motivo de Viaje")
    plt.xlabel("Tipo de viaje")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)
    return Response(img.getvalue(), mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, port=5000)



