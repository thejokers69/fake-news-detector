#!/usr/bin/env python3
"""
Script de démarrage pour le Fake News Detector
"""

import os
import sys
import subprocess

def check_requirements():
    """Vérifie si les dépendances sont installées"""
    try:
        import flask
        import sklearn
        import nltk
        print("Dependances verifiees")
        return True
    except ImportError as e:
        print(f"Dependance manquante : {e}")
        print("Installez les dépendances avec : pip install -r requirements.txt")
        return False

def check_models():
    """Vérifie si les fichiers du modèle existent"""
    model_exists = os.path.exists('models/fake_news_model.pkl')
    vectorizer_exists = os.path.exists('models/tfidf_vectorizer.pkl')

    if model_exists and vectorizer_exists:
        print("Modeles ML trouves")
        return True
    else:
        print("Attention: Modeles ML manquants :")
        if not model_exists:
            print("   - models/fake_news_model.pkl")
        if not vectorizer_exists:
            print("   - models/tfidf_vectorizer.pkl")
        print("Placez vos fichiers de modèle dans le dossier models/")
        return False

def main():
    """Fonction principale"""
    print("Fake News Detector - Verification du systeme")
    print("=" * 50)

    # Vérifications
    deps_ok = check_requirements()
    models_ok = check_models()

    if not deps_ok:
        sys.exit(1)

    if not models_ok:
        print("\nVous pouvez quand même démarrer l'application,")
        print("mais la fonctionnalité de prédiction ne sera pas disponible.")

    print("\nDemarrage de l'application...")
    print("Appuyez sur Ctrl+C pour arrêter")

    try:
        # Démarrage de Flask
        os.system("python app.py")
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée")
    except Exception as e:
        print(f"\nErreur lors du demarrage : {e}")

if __name__ == "__main__":
    main()
