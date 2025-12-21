# 📰 Fake News Detector

Un détecteur de fake news utilisant le machine learning avec une interface web Flask.

## 🚀 Démarrage rapide

### Prérequis

- Python 3.8+
- pip

### Installation

1. **Cloner le projet et installer les dépendances :**

```bash
pip install -r requirements.txt
```

2. **Placer les fichiers du modèle ML :**
   - Placez votre modèle entraîné dans `models/fake_news_model.pkl`
   - Placez votre vectorizer TF-IDF dans `models/tfidf_vectorizer.pkl`

3. **Lancer l'application :**

```bash
python app.py
```

4. **Accéder à l'application :**
   - Ouvrez votre navigateur à l'adresse `http://127.0.0.1:8080/`

## 📋 Utilisation

### Avec les modèles pré-entraînés

Si vous utilisez les modèles déjà entraînés (recommandé) :

1. **Démarrez l'application :**

```bash
python start.py
# ou directement : python app.py
```

2. **Accédez à l'application :**
   - Ouvrez `http://127.0.0.1:8080/` dans votre navigateur

3. **Utilisez le détecteur :**
   - **Option 1 : Utilisez les exemples nettoyés**
     - Ouvrez `Exemples/examples_true_clean.txt` ou `Exemples/examples_fake_clean.txt`
     - Copiez le texte d'un exemple (sans les guillemets)
   - **Option 2 : Copiez depuis des articles externes**
     - Collez le texte directement depuis des sites web ou articles
   - Cliquez sur le bouton "Analyser"
   - Le résultat s'affiche avec la probabilité

### ⚠️ Problèmes de copier-coller

Si vous rencontrez des problèmes lors du copier-coller :

- **Évitez de copier directement depuis les fichiers CSV** (`DATASETS/True.csv`, `DATASETS/Fake.csv`)
- **Utilisez plutôt les fichiers nettoyés** : `Exemples/examples_true_clean.txt` et `Exemples/examples_fake_clean.txt`
- **Vérifiez le texte** dans la zone de texte avant de cliquer sur "Analyser"
- **Nettoyez le texte** si nécessaire (supprimez les guillemets, caractères spéciaux)

### Entraîner votre propre modèle

Si vous voulez entraîner le modèle avec vos propres données :

1. **Placez vos datasets dans le dossier `DATASETS/` :**
   - `True.csv` : articles authentiques
   - `Fake.csv` : articles fake news

2. **Entraînez le modèle :**

```bash
python train_model.py
```

3. **Lancez l'application :**

```bash
python app.py
```

## 🏗️ Architecture

```tree
fake-news-detector/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── start.py               # Script de démarrage avec vérifications
├── train_model.py        # Script d'entraînement du modèle
├── clean_text.py         # Nettoyage des textes d'exemple
├── README.md             # Documentation
├── .gitignore            # Fichiers à ignorer
├── DATASETS/             # Données d'entraînement
│   ├── True.csv
│   └── Fake.csv
├── models/               # Modèles entraînés
│   ├── fake_news_model.pkl
│   └── tfidf_vectorizer.pkl
├── templates/            # Templates HTML
│   └── index.html
├── static/               # CSS, images (optionnel)
├── Exemples/             # 📚 Exemples de textes
│   ├── README.md
│   ├── examples.txt
│   ├── examples_true_clean.txt
│   └── examples_fake_clean.txt
└── Tests/                # 🧪 Scripts de test
    ├── README.md
    ├── test_models.py
    ├── test_app.py
    └── test_full_app.py
```

## 🔧 Configuration

### Fichiers du modèle ML

Le modèle doit être entraîné avec :

- **Vectorizer** : TF-IDF vectorizer de scikit-learn
- **Modèle** : Classifieur binaire (0 = Real, 1 = Fake)
- **Prétraitement** : Nettoyage du texte, suppression des stop words, lemmatization

### Variables d'environnement (optionnel)

```bash
export FLASK_ENV=development  # Mode debug
export FLASK_APP=app.py
```

## 🧪 Tests

### Tests locaux

1. Lancez l'application avec `python app.py`
2. Testez avec différents types de texte
3. Vérifiez les résultats dans la console

### Endpoint de santé

Accédez à `http://127.0.0.1:8080/health` pour vérifier l'état du modèle.

## 🚢 Déploiement

### Options recommandées

- **Render** : PaaS simple pour Flask
- **Railway** : Déploiement automatisé
- **Heroku** : Plateforme cloud populaire

### Avec Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "app.py"]
```

## 📊 Métriques du modèle actuel

Le modèle fourni a été entraîné sur **44,898 articles** (21,417 vrais + 23,481 fake) :

- **Accuracy** : 98.9%
- **Precision (Real)** : 99%
- **Precision (Fake)** : 99%
- **Recall (Real)** : 99%
- **Recall (Fake)** : 99%
- **F1-Score** : 99%

### Matrice de confusion (sur 8,980 articles de test)

- Articles réels correctement classés : 4,245/4,284
- Articles fake correctement classés : 4,638/4,696
- Erreurs totales : 97 articles (1.1%)

### Nettoyer les textes d'exemple

Pour créer des fichiers d'exemples propres à partir de vos datasets :

```bash
python clean_text.py
```

Cela génère dans le dossier `Exemples/` :

- `examples_true_clean.txt` : articles authentiques nettoyés
- `examples_fake_clean.txt` : articles fake news nettoyés

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT.

## ⚠️ Avertissement

Ce détecteur est un outil d'aide à la décision et ne remplace pas l'analyse critique humaine. Les résultats peuvent contenir des erreurs.
