#!/usr/bin/env python3
"""
Script pour nettoyer automatiquement les émojis des fichiers Python
Utile si vous voulez éviter que ça montre l'utilisation d'IA
"""

import os
import re

def clean_file_emojis(filepath):
    """Nettoie les émojis d'un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remplacements des émojis courants
        replacements = {
            '🎯': 'Precision',
            '📰': 'News',
            '🤖': 'IA',
            '📊': 'Analyse',
            '🏃': 'Entrainement',
            '✅': 'OK',
            '❌': 'ERREUR',
            '📈': 'Resultats',
            '📋': 'Rapport',
            '🔢': 'Stats',
            '💾': 'Sauvegarde',
            '🎉': 'Succes',
            '💡': 'Info',
            '📂': 'Dossier',
            '📝': 'Creation',
            '🧹': 'Nettoyage',
            '✂️': 'Separation',
            '📚': 'Exemples',
            '🧪': 'Test',
            '🚀': 'Demarrage',
            '📖': 'Article',
            '🔬': 'Science',
            '⚠️': 'Attention',
            '📱': 'App',
            '🛑': 'Arret'
        }

        original_content = content
        for emoji, replacement in replacements.items():
            content = content.replace(emoji, replacement)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Nettoye: {filepath}")
            return True

    except Exception as e:
        print(f"Erreur avec {filepath}: {e}")

    return False

def clean_project_emojis():
    """Nettoie tous les émojis du projet"""
    print("Nettoyage automatique des emojis...")

    # Fichiers à nettoyer
    files_to_clean = [
        'app.py',
        'start.py',
        'train_model.py',
        'demo.py',
        'clean_text.py',
        'organize_project.py'
    ]

    # Ajouter les fichiers des dossiers
    for root, dirs, files in os.walk('.'):
        if root.startswith('./') and not root.startswith('./.'):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    files_to_clean.append(filepath)

    cleaned_count = 0
    for filepath in files_to_clean:
        if os.path.exists(filepath):
            if clean_file_emojis(filepath):
                cleaned_count += 1

    print(f"Fait ! {cleaned_count} fichiers nettoyes.")

if __name__ == "__main__":
    clean_project_emojis()
