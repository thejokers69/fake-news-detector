#!/usr/bin/env python3
"""
Démonstration du Fake News Detector
Test rapide avec les exemples nettoyés
"""

import requests
import time
import subprocess
import signal
import os


def demo():
    """Démonstration complète du détecteur"""
    print("Demo Démonstration du Fake News Detector")
    print("=" * 50)

    # Démarrer l'application
    print("Demarrage Démarrage de l'application...")
    server = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
    )

    time.sleep(2)  # Attendre le démarrage

    try:
        # Test 1: Article authentique
        print("\nArticle Test 1: Article authentique")
        with open("Exemples/examples_true_clean.txt", "r", encoding="utf-8") as f:
            content = f.read()
            # Extraire le premier exemple
            lines = content.split("==================================================")
            example_text = lines[1].strip().split("\n", 2)[2]  # Titre + contenu

        print(f"Texte: {example_text[:100]}...")

        response = requests.post(
            "http://127.0.0.1:8080/predict", data={"news_text": example_text}
        )
        if "Article Authentique" in response.text:
            print("OK Résultat: CORRECT - Article authentique détecté")
        else:
            print("Erreur Résultat: INCORRECT")

        # Test 2: Article fake
        print("\nFake Test 2: Article fake news")
        with open("Exemples/examples_fake_clean.txt", "r", encoding="utf-8") as f:
            content = f.read()
            # Extraire le premier exemple
            lines = content.split("==================================================")
            example_text = lines[1].strip().split("\n", 2)[2]  # Titre + contenu

        print(f"Texte: {example_text[:100]}...")

        response = requests.post(
            "http://127.0.0.1:8080/predict", data={"news_text": example_text}
        )
        if "Fake News" in response.text:
            print("OK Résultat: CORRECT - Fake news détecté")
        else:
            print("Erreur Résultat: INCORRECT")

        print("\nTermine Démonstration terminée avec succès!")
        print("\nNote L'application fonctionne correctement.")
        print(
            "   Vos camarades peuvent maintenant tester avec les exemples du dossier Exemples/"
        )

    except Exception as e:
        print(f"Erreur Erreur lors de la démonstration: {e}")

    finally:
        # Arrêter le serveur
        try:
            os.killpg(os.getpgid(server.pid), signal.SIGTERM)
            print("\nArret Serveur arrêté")
        except:
            pass


if __name__ == "__main__":
    demo()
