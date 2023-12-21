import base64
import io

from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image

from compare_img_v2 import process_dni_images
from db_connection import collection

app = Flask(__name__)
CORS(app, resources={r"/process-dni": {"origins": "http://localhost:3000"}})


@app.route("/process-dni", methods=["POST"])
def process_dni():
    # try:
    data = request.get_json()

    dni_image_data = base64.b64decode(data["dni_image"].split(",")[1])
    user_image_data = base64.b64decode(data["user_image"].split(",")[1])
    dni_image = Image.open(io.BytesIO(dni_image_data))
    user_image = Image.open(io.BytesIO(user_image_data))

    results = process_dni_images(dni_image, user_image)
    if not results["¿Son la misma persona?"]:
        return (
            jsonify(
                {
                    "message": "Imágenes No son iguales",
                    "results": results,
                }
            ),
            200,
        )

    # Insertar los resultados en MongoDB y obtener el ID insertado
    insert_result = collection.insert_one(results)
    results["_id"] = str(insert_result.inserted_id)
    # Preparar la respuesta, incluyendo el ID del documento como una cadena
    response = {
        "message": "Imágenes procesadas con éxito",
        "results": results,
    }
    return jsonify(response)


# except Exception as e:
#     return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
