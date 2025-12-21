# 🧪 Dossier Tests

Ce dossier contient tous les scripts de test pour valider le fonctionnement du détecteur de fake news.

## 📄 Fichiers de test :

### `test_models.py`
- **Test rapide** des modèles chargés
- Vérifie que les prédictions fonctionnent correctement
- Test avec quelques exemples simples

### `test_app.py`
- **Test des endpoints** de l'API Flask
- Vérifie la disponibilité des routes `/`, `/health`, `/predict`
- Test automatisé de l'application

### `test_full_app.py`
- **Test complet** de l'application
- Démarre automatiquement le serveur et teste toutes les fonctionnalités
- Test end-to-end complet

## 🚀 Comment exécuter les tests :

### Test rapide des modèles :
```bash
python test_models.py
```

### Test des endpoints API :
```bash
python test_app.py
```

### Test complet de l'application :
```bash
python test_full_app.py
```

## 📊 Résultats attendus :

- ✅ Modèles chargés correctement
- ✅ Prédictions fonctionnelles avec accuracy ~99%
- ✅ Application web accessible
- ✅ API répondant correctement

## 🔧 Scripts disponibles dans la racine :

- `train_model.py` : Entraînement du modèle
- `clean_text.py` : Nettoyage des textes d'exemple
- `start.py` : Démarrage facilité de l'application
