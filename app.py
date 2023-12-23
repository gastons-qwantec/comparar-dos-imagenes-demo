import base64
import io

from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
from pymongo.errors import PyMongoError

from compare_img import process_dni_images
from config.db.noSQL_connection import collection

app = Flask(__name__)
CORS(app, resources={r"/process-dni": {"origins": "http://localhost:3000"}})


@app.route("/process-dni", methods=["POST"])
def process_dni():
    try:
        data = request.get_json()

        # Validaciones de datos recibidos
        if "dni_image" not in data or "user_image" not in data:
            return jsonify({"message": "Datos incompletos"}), 400

        dni_image_data = base64.b64decode(data["dni_image"].split(",")[1])
        user_image_data = base64.b64decode(data["user_image"].split(",")[1])
        dni_image = Image.open(io.BytesIO(dni_image_data))
        user_image = Image.open(io.BytesIO(user_image_data))

        results = process_dni_images(dni_image, user_image)

        if not results["misma_persona"]:
            return (
                jsonify({"message": "Imágenes No son iguales", "results": results}),
                200,
            )

        rut = results.get("RUN")
        if rut and collection.find_one({"RUN": rut}):
            app.logger.info(f"RUT {rut} ya existe en la base de datos")
            return jsonify({"message": f"RUT {rut} ya existe en la base de datos"}), 201

        insert_result = collection.insert_one(results)
        results["_id"] = str(insert_result.inserted_id)

        return (
            jsonify({"message": "Imágenes procesadas con éxito", "results": results}),
            200,
        )

    except PyMongoError as e:
        app.logger.error(f"Error de base de datos: {e}")
        return jsonify({"error": "Error al interactuar con la base de datos"}), 500
    except Exception as e:
        app.logger.error(f"Error del servidor: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == "__main__":
    app.run(debug=True)
