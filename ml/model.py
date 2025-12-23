import os
import joblib
import re
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Configuration des chemins
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "models" / "fake_news_model.pkl"
VECTORIZER_PATH = BASE_DIR / "ml" / "models" / "tfidf_vectorizer.pkl"

# Variables globales pour les modèles
model = None
vectorizer = None
lemmatizer = None
stop_words = None


def initialize_nltk():
    """Initialize NLTK and download necessary resources"""
    try:
        nltk.data.path.append(str(BASE_DIR / "nltk_data"))
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download("omw-1.4", quiet=True)
    except Exception as e:
        print(f"Warning: Could not download NLTK resources: {e}")


def load_models():
    """Load ML models and vectorizer"""
    global model, vectorizer, lemmatizer, stop_words

    try:
        # Initialiser NLTK
        initialize_nltk()

        # Initialiser le lemmatizer et les stop words
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))

        # Charger le modèle
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            print("✓ Model loaded successfully")
        else:
            print(f"✗ Modèle non trouvé: {MODEL_PATH}")
            return False

        # Charger le vectorizer
        if VECTORIZER_PATH.exists():
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("✓ Vectorizer loaded successfully")
        else:
            print(f"✗ Vectorizer non trouvé: {VECTORIZER_PATH}")
            return False

        return True

    except Exception as e:
        print(f"✗ Erreur lors du chargement des modèles: {e}")
        return False


def preprocess_text(text):
    """Preprocess text the same way as during training"""
    if not isinstance(text, str) or not text.strip():
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
    """Predict if the text is fake news"""
    if model is None or vectorizer is None:
        return {
            "label": "Erreur",
            "probability": 0.0,
            "error": "Model or vectorizer not loaded",
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


# Charger les modèles au démarrage du module
if not load_models():
    print(
        "⚠️  Warning: Models could not be loaded. The application may not work correctly."
    )
