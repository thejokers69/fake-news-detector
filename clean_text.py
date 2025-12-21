#!/usr/bin/env python3
"""
Script pour nettoyer et préparer des textes d'exemple
pour le Fake News Detector
"""

import re
import pandas as pd

def clean_csv_text(text):
    """Nettoie le texte extrait des fichiers CSV"""
    if not isinstance(text, str):
        return ""

    # Supprimer les guillemets doubles au début et à la fin
    text = text.strip('"')

    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text)

    # Supprimer les caractères de contrôle invisibles
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)

    return text.strip()

def extract_examples_from_csv(csv_file, output_file, num_examples=5):
    """Extrait des exemples propres depuis un fichier CSV"""
    try:
        df = pd.read_csv(csv_file, nrows=num_examples)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Exemples nettoyés depuis {}\n\n".format(csv_file))

            for i, (_, row) in enumerate(df.iterrows(), 1):
                # Combiner titre et texte
                title = clean_csv_text(row['title'])
                text = clean_csv_text(row['text'])

                combined = f"{title}\n\n{text}"

                f.write(f"## Exemple {i} ({row['subject']})\n")
                f.write(combined)
                f.write("\n\n" + "="*50 + "\n\n")

        print(f"OK {num_examples} exemples extraits et nettoyés dans {output_file}")

    except Exception as e:
        print(f"Erreur lors de l'extraction : {e}")

def main():
    """Fonction principale"""
    print("Nettoyage Nettoyage des textes d'exemple...")

    # Extraire des exemples depuis True.csv
    extract_examples_from_csv(
        'DATASETS/True.csv',
        'examples_true_clean.txt',
        num_examples=3
    )

    # Extraire des exemples depuis Fake.csv
    extract_examples_from_csv(
        'DATASETS/Fake.csv',
        'examples_fake_clean.txt',
        num_examples=3
    )

    print("\nConseils pour eviter les problemes de copier-coller :")
    print("1. Utilisez les fichiers examples_true_clean.txt et examples_fake_clean.txt")
    print("2. Copiez seulement le texte principal (sans les guillemets)")
    print("3. Évitez de copier depuis le fichier CSV directement")
    print("4. Vérifiez que le texte apparaît bien dans la zone de texte avant de cliquer sur Analyser")

if __name__ == "__main__":
    main()
