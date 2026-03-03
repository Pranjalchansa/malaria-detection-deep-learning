from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from werkzeug.utils import secure_filename
import os
import uuid
import json

app = Flask(__name__)

# =============================
# Load Trained Model
# =============================
model = tf.keras.models.load_model("malaria_model.keras")

# =============================
# Load Class Indices
# =============================
with open("class_indices.json", "r") as f:
    class_indices = json.load(f)

# Reverse mapping (index → class name)
index_to_class = {v: k for k, v in class_indices.items()}

print("Class Indices:", class_indices)

# =============================
# Upload Folder Setup
# =============================
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =============================
# Routes
# =============================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return render_template("index.html", error="No file uploaded")

    file = request.files["file"]

    if file.filename == "":
        return render_template("index.html", error="No file selected")

    if not allowed_file(file.filename):
        return render_template("index.html", error="Invalid file type (Only PNG/JPG allowed)")

    # =============================
    # Save File
    # =============================
    filename = secure_filename(file.filename)
    unique_name = str(uuid.uuid4()) + "_" + filename
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file.save(filepath)

    try:
        # =============================
        # Image Preprocessing
        # =============================
        img = image.load_img(filepath, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        # MobileNetV2 preprocessing
        img_array = preprocess_input(img_array)

        # =============================
        # Prediction
        # =============================
        prediction = model.predict(img_array)[0][0]

        print("Raw Prediction:", prediction)

        # Binary classification logic
        if prediction < 0.5:
            predicted_index = 0
            confidence = (1 - prediction) * 100
            result = "Malaria Detected"
            recommendation = "Malaria detected. Please consult a doctor immediately."
            status_color = "red"
        else:
            predicted_index = 1
            confidence = prediction * 100
            result = "Malaria Not Detected"
            recommendation = "No malaria detected. Maintain hygiene and regular health checkups."
            status_color = "green"

        detected_class = index_to_class[predicted_index]

        return render_template(
            "index.html",
            result=result,
            detected_class=detected_class,
            confidence=f"{confidence:.2f}",
            recommendation=recommendation,
            image_path=filepath,
            status_color=status_color
        )

    except Exception as e:
        print("Error:", e)
        return render_template(
            "index.html",
            error="Something went wrong during prediction."
        )


# =============================
# Run App
# =============================
if __name__ == "__main__":
    app.run(debug=True)