#!/usr/bin/env python3
"""
Script d'organisation automatique du projet Fake News Detector
Crée la structure de dossiers et organise les fichiers
"""

import os
import shutil

def create_folders():
    """Créer la structure de dossiers"""
    folders = ['Exemples', 'Tests', 'DATASETS', 'models', 'templates', 'static']

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"OK Dossier créé: {folder}/")

def organize_files():
    """Organiser les fichiers dans les bons dossiers"""
    # Fichiers d'exemples
    example_files = ['examples.txt', 'examples_true_clean.txt', 'examples_fake_clean.txt']
    for file in example_files:
        if os.path.exists(file):
            shutil.move(file, f'Exemples/{file}')
            print(f"Exemples Déplacé: {file} → Exemples/")

    # Fichiers de test
    test_files = ['test_app.py', 'test_full_app.py', 'test_models.py']
    for file in test_files:
        if os.path.exists(file):
            shutil.move(file, f'Tests/{file}')
            print(f"Tests Déplacé: {file} → Tests/")

def create_readmes():
    """Créer les fichiers README dans chaque dossier"""
    # README pour Exemples
    exemples_readme = """# Exemples Dossier Exemples

Ce dossier contient des exemples de textes pour tester le détecteur de fake news.

## 📄 Fichiers disponibles :

### `examples.txt`
- Exemples originaux du projet

### `examples_true_clean.txt`
- **Articles authentiques** nettoyés et prêts à être copiés
- 3 exemples d'articles de presse véridiques

### `examples_fake_clean.txt`
- **Articles fake news** nettoyés et prêts à être copiés
- 3 exemples d'articles de désinformation

## Comment Comment utiliser :

1. Ouvrez le fichier souhaité
2. Copiez le texte d'un exemple (sans les guillemets)
3. Collez dans l'application web
4. Cliquez sur "Analyser"
"""

    with open('Exemples/README.md', 'w', encoding='utf-8') as f:
        f.write(exemples_readme)
    print("Creation README créé: Exemples/README.md")

    # README pour Tests
    tests_readme = """# Tests Dossier Tests

Scripts de test pour valider le fonctionnement du détecteur.

## 📄 Fichiers de test :

### `test_models.py`
- Test rapide des modèles chargés

### `test_app.py`
- Test des endpoints de l'API Flask

### `test_full_app.py`
- Test complet de l'application

## Execution Exécution :
```bash
python test_models.py    # Test rapide
python test_app.py      # Test API
python test_full_app.py # Test complet
```
"""

    with open('Tests/README.md', 'w', encoding='utf-8') as f:
        f.write(tests_readme)
    print("Creation README créé: Tests/README.md")

def main():
    """Fonction principale"""
    print("Organisation Organisation automatique du projet Fake News Detector")
    print("=" * 60)

    create_folders()
    print()
    organize_files()
    print()
    create_readmes()

    print("\nOK Organisation terminée!")
    print("\nDossiers Structure finale:")
    print("├── Exemples/     # Exemples Textes d'exemple")
    print("├── Tests/        # Tests Scripts de test")
    print("├── DATASETS/     # Donnees Données d'entraînement")
    print("├── models/       # Modeles Modèles ML")
    print("├── templates/    # 🎨 Interface web")
    print("└── [fichiers principaux]")
    print("\nObjectif Vos camarades peuvent maintenant facilement comprendre la structure!")

if __name__ == "__main__":
    main()
