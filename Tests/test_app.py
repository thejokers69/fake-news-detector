#!/usr/bin/env python3
"""
Tests simples pour vérifier le fonctionnement de l'application
"""

import requests
import time
import subprocess
import signal
import os
import sys

def test_health_endpoint(base_url="http://127.0.0.1:8080"):
    """Test l'endpoint de santé"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("OK Endpoint /health fonctionne")
            print(f"   Status: {data.get('status')}")
            print(f"   Modèle: {data.get('model')}")
            print(f"   Vectorizer: {data.get('vectorizer')}")
            return True
        else:
            print(f"ERREUR Endpoint /health retourne le code {response.status_code}")
            return False
    except Exception as e:
        print(f"ERREUR Erreur lors du test de /health : {e}")
        return False

def test_homepage(base_url="http://127.0.0.1:8080"):
    """Test la page d'accueil"""
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200 and "Fake News Detector" in response.text:
            print("OK Page d'accueil accessible")
            return True
        else:
            print(f"ERREUR Page d'accueil retourne le code {response.status_code}")
            return False
    except Exception as e:
        print(f"ERREUR Erreur lors du test de la page d'accueil : {e}")
        return False

def test_prediction_endpoint(base_url="http://127.0.0.1:8080"):
    """Test l'endpoint de prédiction"""
    test_text = "This is a test news article about technology and innovation."

    try:
        response = requests.post(
            f"{base_url}/predict",
            data={'news_text': test_text},
            timeout=10
        )

        if response.status_code == 200:
            print("OK Endpoint /predict accessible")

            # Vérifie que la réponse contient les éléments attendus
            if "Fake News Detector" in response.text:
                print("OK Formulaire affiché correctement")
                return True
            else:
                print("ATTENTION  Réponse reçue mais contenu inattendu")
                return False
        else:
            print(f"ERREUR Endpoint /predict retourne le code {response.status_code}")
            return False
    except Exception as e:
        print(f"ERREUR Erreur lors du test de /predict : {e}")
        return False

def run_tests():
    """Exécute tous les tests"""
    print("TEST Tests de l'application Fake News Detector")
    print("=" * 50)

    # Vérifier si l'application tourne
    try:
        response = requests.get("http://127.0.0.1:8080", timeout=2)
    except:
        print("ERREUR L'application ne semble pas tourner sur le port 8080")
        print("Démarrez l'application avec : python app.py")
        print("Ou utilisez le script : python start.py")
        return False

    tests = [
        ("Endpoint de santé", test_health_endpoint),
        ("Page d'accueil", test_homepage),
        ("Endpoint de prédiction", test_prediction_endpoint)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Test : {test_name}")
        if test_func():
            passed += 1

    print(f"\nRESULTATS Résultats : {passed}/{total} tests réussis")

    if passed == total:
        print("SUCCES Tous les tests sont passés !")
        return True
    else:
        print("ATTENTION  Certains tests ont échoué")
        return False

def main():
    """Fonction principale"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python test_app.py")
        print("Teste le fonctionnement de l'application Fake News Detector")
        print("Assurez-vous que l'application tourne sur http://127.0.0.1:8080")
        return

    success = run_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
