from flask import Flask, request, render_template
import joblib
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

# Configuration de NLTK
nltk.data.path.append("./nltk_data")
try:
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)
except:
    pass

app = Flask(__name__)

# Configuration
MODEL_PATH = "models/fake_news_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

# Variables globales pour le modèle
model = None
vectorizer = None
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def load_model():
    """Charge le modèle ML et le vectorizer"""
    global model, vectorizer

    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print("Modele charge avec succes")
        else:
            print(
                "Attention: Modele non trouve. Placez fake_news_model.pkl dans le dossier models/"
            )

        if os.path.exists(VECTORIZER_PATH):
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("Vectorizer charge avec succes")
        else:
            print(
                "Attention: Vectorizer non trouve. Placez tfidf_vectorizer.pkl dans le dossier models/"
            )

    except Exception as e:
        print(f"Erreur lors du chargement du modele : {e}")


def preprocess_text(text):
    """Prétraite le texte de la même manière que pendant l'entraînement"""
    if not text:
        return ""

    # Conversion en minuscules
    text = text.lower()

    # Suppression des caractères spéciaux et chiffres
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Tokenization
    words = text.split()

    # Suppression des stop words et lemmatization
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

    # Rejoindre les mots
    return " ".join(words)


def predict_fake_news(text):
    """Prédit si le texte est une fake news"""
    if model is None or vectorizer is None:
        return {
            "label": "Erreur",
            "probability": 0.0,
            "error": "Modèle ou vectorizer non chargé",
        }

    try:
        # Prétraitement du texte
        processed_text = preprocess_text(text)

        # Vectorisation
        text_vectorized = vectorizer.transform([processed_text])

        # Prédiction
        prediction = model.predict(text_vectorized)[0]
        probabilities = model.predict_proba(text_vectorized)[0]

        # Probabilité de la classe prédite
        probability = probabilities[prediction]

        # Conversion en label
        label = "Fake" if prediction == 1 else "Real"

        return {
            "label": label,
            "probability": float(probability),
            "processed_text": processed_text,
        }

    except Exception as e:
        return {"label": "Erreur", "probability": 0.0, "error": str(e)}


@app.route("/", methods=["GET"])
def home():
    """Page d'accueil avec le formulaire"""
    return render_template("index.html", submitted_text="")


@app.route("/predict", methods=["POST"])
def predict():
    """Route pour faire la prédiction"""
    try:
        # Récupération du texte du formulaire
        news_text = request.form.get("news_text", "").strip()

        if not news_text:
            prediction = {
                "label": "Erreur",
                "probability": 0.0,
                "error": "Veuillez entrer du texte à analyser",
            }
        else:
            # Prédiction
            prediction = predict_fake_news(news_text)

            # Ajouter un aperçu pour l'affichage
            prediction["input_preview"] = news_text[:240]
            prediction["input_length"] = len(news_text)

        return render_template(
            "index.html", prediction=prediction, submitted_text=news_text
        )

    except Exception as e:
        prediction = {"label": "Erreur", "probability": 0.0, "error": str(e)}
        return render_template(
            "index.html", prediction=prediction, submitted_text=news_text
        )


@app.route("/health")
def health():
    """Endpoint de santé pour vérifier que l'app fonctionne"""
    model_status = "chargé" if model is not None else "non chargé"
    vectorizer_status = "chargé" if vectorizer is not None else "non chargé"

    return {"status": "OK", "model": model_status, "vectorizer": vectorizer_status}


if __name__ == "__main__":
    # Chargement du modèle au démarrage
    load_model()

    # Démarrage du serveur
    print("Demarrage du Fake News Detector...")
    print("Accedez a http://127.0.0.1:8080/")
    app.run(debug=True, host="0.0.0.0", port=8080)
