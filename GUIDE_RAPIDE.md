# 🚀 Guide Rapide - Fake News Detector

## 🎯 Objectif
Ce projet détecte automatiquement si un article de presse est une **fake news** ou un **article authentique** avec une précision de **99%**.

## 📁 Structure du projet (3 dossiers principaux)

### 1. 📚 `Exemples/` - Textes de test
- **Articles vrais** : `examples_true_clean.txt`
- **Articles fake** : `examples_fake_clean.txt`
- **Comment utiliser** : Copiez-collez le texte dans l'application

### 2. 🧪 `Tests/` - Validation
- **Test des modèles** : `test_models.py`
- **Test de l'application** : `test_app.py`
- **Test complet** : `test_full_app.py`

### 3. 🏗️ Racine - Code principal
- **Application web** : `app.py`
- **Entraînement** : `train_model.py`
- **Démarrage** : `start.py`

## 🖥️ Comment lancer l'application

### Étape 1 : Démarrer l'application
```bash
python start.py
```

### Étape 2 : Ouvrir dans le navigateur
- Allez à : `http://127.0.0.1:8080/`
- L'application se charge automatiquement avec les modèles ML

### Étape 3 : Tester avec un exemple
1. Ouvrez `Exemples/examples_true_clean.txt`
2. Copiez le texte du premier exemple
3. Collez-le dans la zone "Texte de l'article"
4. Cliquez sur "🔍 Analyser"
5. **Résultat attendu** : "✅ Résultat : Article Authentique" avec ~99% de confiance

## 🔬 Fonctionnement technique

### Le modèle ML :
- **Algorithme** : Régression Logistique
- **Vectorisation** : TF-IDF (5,000 mots-clés)
- **Prétraitement** : Nettoyage, stop words, lemmatization
- **Accuracy** : 98.9% sur 44,898 articles

### L'application web :
- **Framework** : Flask (Python)
- **Interface** : Bootstrap (responsive)
- **API** : Routes GET/POST pour l'analyse

## 🧪 Tests automatisés

### Vérifier que tout fonctionne :
```bash
# Test rapide des modèles
python Tests/test_models.py

# Test de l'application
python Tests/test_app.py

# Test complet
python Tests/test_full_app.py
```

## 📊 Résultats d'exemple

| Texte testé | Résultat | Confiance |
|-------------|----------|-----------|
| Article Reuters | ✅ Authentique | 99.6% |
| Article fake news | ❌ Fake News | 93.2% |
| Texte neutre | ❌ Fake News | 57.7% |

## ⚠️ Points importants

1. **Utilisez les fichiers nettoyés** dans `Exemples/` plutôt que les CSV
2. **Copiez seulement le texte** (pas les guillemets ou en-têtes)
3. **Vérifiez que le texte apparaît** dans la zone avant de cliquer
4. **L'application doit tourner** sur le port 8080

## 🎓 Pour les camarades de classe

- **Comprendre le ML** : Le modèle apprend à distinguer les patterns des vrais/fake articles
- **Interface simple** : Copier-coller → Analyser → Résultat instantané
- **Précision élevée** : 99% d'accuracy sur des milliers d'articles
- **Application réelle** : Détecte la désinformation automatiquement

## 🔧 Support

Si ça ne fonctionne pas :
1. Vérifiez que l'application tourne (`python start.py`)
2. Utilisez les exemples du dossier `Exemples/`
3. Copiez seulement le texte principal (sans guillemets)
4. Rafraîchissez la page si nécessaire

---
**Projet créé par [Votre nom] - Détection automatique de fake news avec IA**
