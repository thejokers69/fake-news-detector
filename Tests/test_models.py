#!/usr/bin/env python3
"""
Test rapide des modèles chargés
"""

import sys

sys.path.append(".")
from app import load_model, predict_fake_news

print("TEST Test du chargement et de la prédiction...")

# Test du chargement
load_model()

# Test avec des exemples du dataset d'entraînement
test_real = "WASHINGTON (Reuters) - The head of a conservative Republican faction in the U.S. Congress, who voted this month for a huge expansion of the national debt to pay for tax cuts, called himself a fiscal conservative on Sunday and urged budget restraint in 2018."

test_fake = "Donald Trump just couldn t wish all Americans a Happy New Year and leave it at that. Instead, he had to give a shout out to his enemies, haters and the very dishonest fake news media."

result_real = predict_fake_news(test_real)
result_fake = predict_fake_news(test_fake)

print(
    f'Article réel: {result_real["label"]} (probabilité: {result_real["probability"]:.3f})'
)
print(
    f'Article fake: {result_fake["label"]} (probabilité: {result_fake["probability"]:.3f})'
)
print("OK Tests terminés!")
