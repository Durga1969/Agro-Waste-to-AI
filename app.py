from flask import Flask, render_template, request
import os
import numpy as np
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
from tensorflow.keras.preprocessing import image
from gtts import gTTS

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
VOICE_FOLDER = "static/voice"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VOICE_FOLDER, exist_ok=True)

model = MobileNet(weights="imagenet")

# Waste + Recycling + Industry info
DATA = {
    "coconut_husk": {
        "label": "Coconut Husk",
        "recycle_en": "Used for coir products, cocopeat, ropes, and compost.",
        "recycle_te": "కొయిర్ ఉత్పత్తులు, కోకోపీట్ మరియు కంపోస్టింగ్ కోసం ఉపయోగిస్తారు",
        "co2": "1.0 kg",
        "industries": [
            "Coir Board India",
            "Kerala Coir Products Ltd",
            "EcoGreen Cocopeat Pvt Ltd"
        ]
    },
    "sugarcane_bagasse": {
        "label": "Sugarcane Bagasse",
        "recycle_en": "Used for paper manufacturing, biofuel, and electricity generation.",
        "recycle_te": "కాగితం తయారీ మరియు బయో ఇంధనానికి ఉపయోగిస్తారు",
        "co2": "1.5 kg",
        "industries": [
            "Triveni Engineering Ltd",
            "JK Paper Mills",
            "Bajaj Hindustan Sugar Ltd"
        ]
    },
    "banana_peel": {
        "label": "Banana Peel",
        "recycle_en": "Used for composting ,bioplastics and bio-enzyme production.",
        "recycle_te": "కంపోస్టింగ్ మరియు బయో ఎంజైమ్ తయారీకి ఉపయోగిస్తారు",
        "co2": "0.8 kg",
        "industries": [
            "UrbanMali Compost Solutions",
            "GreenGrow Organics"
        ]
    },
    "rice_husk": {
        "label": "Rice Husk",
        "recycle_en": "Used in power plants and silica extraction.",
        "recycle_te": "విద్యుత్ ఉత్పత్తి మరియు సిలికా తయారీకి ఉపయోగిస్తారు",
        "co2": "1.2 kg",
        "industries": [
            "Usher Agro Ltd",
            "KRBL Ltd",
            "Olam Agro India"
        ]
    }
}

# Demo prediction logic
def predict_waste(img_path):
    name = img_path.lower()
    if "coconut" in name:
        return "coconut_husk"
    elif "banana" in name:
        return "banana_peel"
    elif "rice" in name:
        return "rice_husk"
    else:
        return "sugarcane_bagasse"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["image"]
        location = request.form.get("location", "India")

        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        key = predict_waste(image_path)
        data = DATA[key]

        telugu_voice = f"""
గుర్తించిన వ్యర్థ పదార్థం {data['label']}.
రీసైక్లింగ్ సూచన: {data['recycle_te']}.
కార్బన్ తగ్గింపు: {data['co2']}.
సమీప పరిశ్రమలు అందుబాటులో ఉన్నాయి.
        """

        voice_path = os.path.join(VOICE_FOLDER, "output.mp3")
        gTTS(telugu_voice, lang="te").save(voice_path)

        result = {
            "label": data["label"],
            "recycle": data["recycle_en"],
            "co2": data["co2"],
            "industries": data["industries"],
            "location": location,
            "image": image_path,
            "voice": voice_path
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
