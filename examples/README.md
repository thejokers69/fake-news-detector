# 📚 Dossier Exemples

Ce dossier contient des exemples de textes pour tester le détecteur de fake news.

## 📄 Fichiers disponibles :

### `examples.txt`
- Exemples originaux du projet
- Textes d'exemple pour comprendre le fonctionnement

### `examples_true_clean.txt`
- **Articles authentiques** nettoyés et prêts à être copiés
- Extraits des données d'entraînement `DATASETS/True.csv`
- 3 exemples d'articles de presse véridiques

### `examples_fake_clean.txt`
- **Articles fake news** nettoyés et prêts à être copiés
- Extraits des données d'entraînement `DATASETS/Fake.csv`
- 3 exemples d'articles de désinformation

## 💡 Comment utiliser :

1. **Ouvrez le fichier** souhaité (`examples_true_clean.txt` ou `examples_fake_clean.txt`)
2. **Copiez le texte** d'un exemple (sans les guillemets)
3. **Collez dans l'application** web à l'adresse `http://127.0.0.1:8080/`
4. **Cliquez sur "Analyser"** pour voir le résultat

## ⚠️ Important :

- Utilisez ces fichiers plutôt que les CSV directement
- Copiez seulement le texte principal (pas les en-têtes)
- Les textes sont déjà nettoyés pour éviter les problèmes de caractères spéciaux
