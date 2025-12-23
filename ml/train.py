#!/usr/bin/env python3
"""
Script d'entraînement du modèle de détection de fake news
Utilise les datasets True.csv et Fake.csv pour entraîner un classifieur
"""

import pandas as pd
import numpy as np
import re
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import warnings

warnings.filterwarnings("ignore")

# Configuration
DATASETS_DIR = "data"
MODELS_DIR = "models"
TRUE_FILE = os.path.join(DATASETS_DIR, "True.csv")
FAKE_FILE = os.path.join(DATASETS_DIR, "Fake.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "fake_news_model.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")


# Téléchargement des ressources NLTK
def download_nltk_resources():
    """Télécharge les ressources NLTK nécessaires"""
    try:
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download("omw-1.4", quiet=True)
        print("Ressources NLTK telechargees")
    except Exception as e:
        print(f"Attention: Erreur lors du telechargement NLTK : {e}")


def load_data():
    """Charge et combine les datasets"""
    print("Chargement des donnees...")

    try:
        # Charger les données vraies
        df_true = pd.read_csv(TRUE_FILE)
        df_true["label"] = 0  # 0 = Real news
        print(f"Dataset True.csv charge : {len(df_true)} articles")

        # Charger les données fake
        df_fake = pd.read_csv(FAKE_FILE)
        df_fake["label"] = 1  # 1 = Fake news
        print(f"Dataset Fake.csv charge : {len(df_fake)} articles")

        # Combiner les datasets
        df_combined = pd.concat([df_true, df_fake], ignore_index=True)
        print(f"Datasets combinas : {len(df_combined)} articles totaux")

        return df_combined

    except Exception as e:
        print(f"Erreur lors du chargement des donnees : {e}")
        return None


def preprocess_text(text, lemmatizer, stop_words):
    """Prétraite le texte (identique à app.py)"""
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


def prepare_features(df):
    """Prépare les features pour l'entraînement"""
    print("🔧 Préparation des features...")

    # Initialisation NLTK
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    # Combiner title + text
    print("Combinaison titre + texte...")
    df["combined_text"] = df["title"] + " " + df["text"]

    # Prétraitement
    print("Nettoyage Prétraitement du texte...")
    df["processed_text"] = df["combined_text"].apply(
        lambda x: preprocess_text(x, lemmatizer, stop_words)
    )

    print("OK Prétraitement terminé")
    return df


def train_model(X_train, X_test, y_train, y_test):
    """Entraîne le modèle"""
    print("IA Entraînement du modèle...")

    # Vectorisation TF-IDF
    print("Analyse Création du vectorizer TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=5000,  # Limiter à 5000 features pour performance
        ngram_range=(1, 2),  # Unigrams et bigrams
        min_df=5,  # Mot présent dans au moins 5 documents
        max_df=0.7,  # Mot présent dans max 70% des documents
    )

    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    print(f"Resultats Features créées : {X_train_vectorized.shape[1]}")

    # Entraînement du modèle
    print("Entrainement Entraînement du classifieur LogisticRegression...")
    model = LogisticRegression(random_state=42, max_iter=1000, C=1.0)

    model.fit(X_train_vectorized, y_train)
    print("OK Modèle entraîné")

    # Évaluation
    print("Analyse Évaluation du modèle...")
    y_pred = model.predict(X_test_vectorized)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precision Accuracy: {accuracy:.3f}")
    # Rapport détaillé
    print("\nRapport Rapport de classification :")
    print(classification_report(y_test, y_pred, target_names=["Real", "Fake"]))

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    print("Stats Matrice de confusion :")
    print(f"Real prédits Real: {cm[0][0]}")
    print(f"Real prédits Fake: {cm[0][1]}")
    print(f"Fake prédits Real: {cm[1][0]}")
    print(f"Fake prédits Fake: {cm[1][1]}")

    return model, vectorizer, accuracy


def save_models(model, vectorizer):
    """Sauvegarde les modèles"""
    print("Sauvegarde Sauvegarde des modèles...")

    # Créer le dossier models s'il n'existe pas
    os.makedirs(MODELS_DIR, exist_ok=True)

    # Sauvegarder le modèle
    joblib.dump(model, MODEL_PATH)
    print(f"OK Modèle sauvegardé : {MODEL_PATH}")

    # Sauvegarder le vectorizer
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"OK Vectorizer sauvegardé : {VECTORIZER_PATH}")


def main():
    """Fonction principale"""
    print("News Fake News Detector - Entraînement du modèle")
    print("=" * 50)

    # Téléchargement NLTK
    download_nltk_resources()

    # Chargement des données
    df = load_data()
    if df is None:
        return

    # Préparation des features
    df = prepare_features(df)

    # Séparation train/test
    print("Separation  Séparation train/test...")
    X = df["processed_text"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Analyse Train set: {len(X_train)} échantillons")
    print(f"Analyse Test set: {len(X_test)} échantillons")

    # Entraînement
    model, vectorizer, accuracy = train_model(X_train, X_test, y_train, y_test)

    # Sauvegarde
    save_models(model, vectorizer)

    print("\nSucces Entraînement terminé avec succès !")
    print(f"Precision Accuracy finale: {accuracy:.3f}")
    print("\nInfo Pour utiliser le modèle :")
    print("   1. Les fichiers sont sauvegardés dans le dossier 'models/'")
    print("   2. Lancez l'application : python app.py")
    print("   3. Testez avec des articles sur http://127.0.0.1:8080/")


if __name__ == "__main__":
    main()
