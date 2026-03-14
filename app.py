from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
from model_loader import load_acne_model, load_pigmentation_model, load_melanoma_model

app = Flask(__name__)
app.secret_key = "dermacare_secret_key"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------- LOAD MODELS --------
acne_model = load_acne_model()
pigmentation_model = load_pigmentation_model()
melanoma_model = load_melanoma_model()


# -------- DATABASE --------
def db_connection():
    return sqlite3.connect("users.db")


conn = db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT UNIQUE,
password TEXT
)
""")
conn.close()


# -------- HELPER FUNCTIONS --------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def risk_explanation(category, level):

    explanations = {

        "acne": {
            "Low": "Your acne level is low. Maintain good hygiene and routine care.",
            "Moderate": "Moderate acne detected. Consider consulting a dermatologist.",
            "High": "High acne severity. Immediate dermatologist consultation recommended."
        },

        "pigmentation": {
            "Low": "Minimal pigmentation. Use sunscreen and moisturizers.",
            "Moderate": "Moderate pigmentation. Regular skincare recommended.",
            "High": "High pigmentation. Dermatologist consultation recommended."
        },

        "melanoma": {
            "Low Risk": "No major melanoma signs detected. Continue regular self-checks.",
            "High Risk": "Possible melanoma risk. Consult a dermatologist immediately."
        }

    }

    return explanations.get(category, {}).get(level, "No information available")


# -------- CHATBOT --------
def chatbot_response(text):

    text = text.lower()
    category = session.get("category")

    if "acne" in text:
        category = "acne"
        session["category"] = "acne"

    elif "pigmentation" in text:
        category = "pigmentation"
        session["category"] = "pigmentation"

    elif "melanoma" in text:
        category = "melanoma"
        session["category"] = "melanoma"

    if text in ["hi", "hello", "menu", "options"]:

        if category == "acne":
            return "👋 Acne Menu:\n1.What is acne?\n2.Causes\n3.Types\n4.Symptoms\n5.Treatment\n6.Home remedies\n7.Diet\n8.When to consult doctor"

        if category == "pigmentation":
            return "👋 Pigmentation Menu:\n1.What is pigmentation?\n2.Causes\n3.Types\n4.Symptoms\n5.Treatment\n6.Home remedies\n7.Diet\n8.When to consult doctor"

        if category == "melanoma":
            return "👋 Melanoma Menu:\n1.What is melanoma?\n2.Causes\n3.Warning signs\n4.Symptoms\n5.Prevention\n6.Medical advice"

        return "Please upload an image first."

    return "Type 'menu' to see options."


# -------- DOSHA DIET --------
def dosha_diet_details(dosha):

    diets = {

        "Vatham": {
            "recommended": ["Warm cooked foods","Milk and ghee","Sweet fruits","Root vegetables"],
            "avoid": ["Cold drinks","Dry foods","Raw vegetables"]
        },

        "Pitham": {
            "recommended": ["Cucumber","Watermelon","Leafy vegetables","Coconut water"],
            "avoid": ["Spicy foods","Fried foods","Excess oil"]
        },

        "Kabam": {
            "recommended": ["Light foods","Green vegetables","Ginger and turmeric"],
            "avoid": ["Dairy","Sugary foods","Heavy foods"]
        }

    }

    return diets.get(dosha, {})


# -------- LOGIN --------
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = email
            return redirect("/upload")

        return "Invalid email or password"

    return render_template("login.html")


# -------- REGISTER --------
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = db_connection()

        try:
            conn.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name,email,password)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            return "Email already registered"

        finally:
            conn.close()

        return redirect("/")

    return render_template("register.html")


# -------- IMAGE UPLOAD --------
@app.route("/upload", methods=["GET","POST"])
def upload():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        image_file = request.files["image"]
        category = request.form["category"]

        if image_file and allowed_file(image_file.filename):

            filename = secure_filename(image_file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            image_file.save(path)

            img = Image.open(path).convert("RGB").resize((224,224))
            img = np.array(img) / 255.0
            img = np.expand_dims(img,axis=0)

            session.pop("acne",None)
            session.pop("pigmentation",None)
            session.pop("melanoma",None)

            # -------- ACNE --------
            if category == "acne":

                probs = acne_model.predict(img)[0]

                if len(probs) == 3:
                    levels = ["Low","Moderate","High"]
                    acne_level = levels[np.argmax(probs)]

                else:
                    acne_level = "High" if probs[1] > 0.5 else "Low"

                session["category"] = "acne"
                session["acne"] = acne_level


            # -------- PIGMENTATION --------
            elif category == "pigmentation":

                probs = pigmentation_model.predict(img)[0]

                if len(probs) == 3:
                    levels = ["Low","Moderate","High"]
                    pigmentation_level = levels[np.argmax(probs)]

                else:
                    pigmentation_level = "High" if probs[1] > 0.5 else "Low"

                session["category"] = "pigmentation"
                session["pigmentation"] = pigmentation_level


            # -------- MELANOMA --------
            elif category == "melanoma":

                probs = melanoma_model.predict(img)[0]
                melanoma_level = "High Risk" if probs[1] > 0.5 else "Low Risk"

                session["category"] = "melanoma"
                session["melanoma"] = melanoma_level


            return redirect("/dosha")

        return "Invalid image file"

    return render_template("upload.html")


# -------- DOSHA --------
@app.route("/dosha", methods=["GET","POST"])
def dosha():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        answers = [request.form[f"q{i}"] for i in range(1,11)]

        scores = {"vatham":0,"pitham":0,"kabam":0}

        for ans in answers:
            scores[ans]+=1

        session["dosha"] = max(scores,key=scores.get).capitalize()

        return redirect("/result")

    return render_template("dosha_form.html")


# -------- RESULT --------
@app.route("/result")
def result():

    if "user" not in session:
        return redirect("/")

    category = session.get("category")
    dosha = session.get("dosha")

    return render_template(

        "result.html",

        category=category,
        acne=session.get("acne"),
        pigmentation=session.get("pigmentation"),
        melanoma=session.get("melanoma"),

        dosha=dosha,
        diet=dosha_diet_details(dosha),

        acne_explain=risk_explanation("acne",session.get("acne")),
        pigmentation_explain=risk_explanation("pigmentation",session.get("pigmentation")),
        melanoma_explain=risk_explanation("melanoma",session.get("melanoma"))

    )


# -------- CHAT --------
@app.route("/chat",methods=["POST"])
def chat():

    message = request.form.get("message")
    reply = chatbot_response(message)

    return jsonify({"reply":reply})


# -------- RUN --------
if __name__ == "__main__":

    os.makedirs(UPLOAD_FOLDER,exist_ok=True)

    app.run(debug=True)