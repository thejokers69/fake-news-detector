#!/usr/bin/env python3
"""
Test complet de l'application web
"""

import requests
import time
import subprocess
import signal
import os

def test_application():
    # Démarrer le serveur en arrière-plan
    print('Demarrage du serveur Flask...')
    server = subprocess.Popen(['python', 'app.py'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             preexec_fn=os.setsid)

    # Attendre que le serveur démarre
    time.sleep(3)

    try:
        # Test de l'endpoint health
        response = requests.get('http://127.0.0.1:8080/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print('OK Serveur démarré avec succès')
            print(f'   Modèle: {data["model"]}')
            print(f'   Vectorizer: {data["vectorizer"]}')

            # Test de la page principale
            response = requests.get('http://127.0.0.1:8080/', timeout=5)
            if 'Fake News Detector' in response.text:
                print('OK Page d\'accueil accessible')

                # Test de prédiction
                test_data = {'news_text': 'This is a test news article about technology.'}
                response = requests.post('http://127.0.0.1:8080/predict', data=test_data, timeout=10)
                if response.status_code == 200 and 'Fake News Detector' in response.text:
                    print('OK Prédiction fonctionnelle')
                    print('SUCCES Application complètement opérationnelle !')
                    return True
                else:
                    print('ERREUR Erreur lors de la prédiction')
                    return False
            else:
                print('ERREUR Page d\'accueil non accessible')
                return False
        else:
            print(f'ERREUR Serveur non accessible (code: {response.status_code})')
            return False

    except Exception as e:
        print(f'ERREUR Erreur: {e}')
        return False

    finally:
        # Arrêter le serveur
        try:
            os.killpg(os.getpgid(server.pid), signal.SIGTERM)
            print('🛑 Serveur arrêté')
        except:
            pass

if __name__ == "__main__":
    success = test_application()
    exit(0 if success else 1)
