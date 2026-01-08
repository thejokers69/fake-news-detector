# 📰 Fake News Detector

A Django-based web application that uses machine learning to detect fake news articles. The system analyzes text content and provides authenticity predictions with confidence scores.

## ✨ Features

- 🧠 **Machine Learning**: Calibrated LinearSVC (SVM) model trained on 44,898 articles
- 🎯 **High Accuracy**: 98.9% precision on real vs fake news detection
- 🌐 **Web Interface**: Clean, responsive Django web application
- 📊 **Real-time Analysis**: Instant predictions with probability scores
- 🐳 **Docker Ready**: Easy deployment with Docker & Docker Compose
- ☁️ **Heroku Compatible**: Ready for cloud deployment

## 🌐 Live Demo

🚀 **Try it now:** [https://my-fake-news-detector-b2ecef362ddb.herokuapp.com/](https://my-fake-news-detector-b2ecef362ddb.herokuapp.com/)

Experience real-time fake news detection with our deployed application!

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip
- Git

### Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd fake-news-detector
```

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

1. **Run database migrations:**

```bash
python manage.py migrate
```

1. **Start the development server:**

```bash
python manage.py runserver
```

1. **Open your browser:**

Visit `http://127.0.0.1:8080/` to access the application.

## 📋 Usage

### Web Interface

1. **Access the application** at `http://127.0.0.1:8080/`

2. **Paste an article** into the text area

3. **Click "Analyze Article"** to get results

4. **View results** with:
   - Authenticity prediction (Real/Fake)
   - Confidence probability
   - Technical details

### API Usage

```bash
# Health check
curl http://127.0.0.1:8080/health/

# Analyze text (POST)
curl -X POST http://127.0.0.1:8080/analyze/ \
  -d "news_text=Your article text here"
```

### Using Examples

Test the detector with provided examples:

```bash
# Real news examples
cat examples/real_news.txt

# Fake news examples
cat examples/fake_news.txt
```

## 🧠 Model Training

To train your own model:

1. **Place your datasets** in `ml/data/`:
   - `True.csv` - Authentic articles
   - `Fake.csv` - Fake news articles

2. **Run training:**

```bash
cd ml
python train.py
```

1. **Models will be saved** to `ml/models/`

1. **Lancez l'application :**

```bash
python manage.py runserver
```

## 📁 Project Structure

```
fake-news-detector/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # Docker build instructions
├── Procfile                     # Heroku deployment config
├── runtime.txt                  # Python version for Heroku
│
├── fakenews_detector/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── detector/                    # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│
├── ml/                          # Machine Learning components
│   ├── __init__.py
│   ├── model.py                 # ML model loading & preprocessing
│   ├── train.py                 # Model training script
│   ├── models/                  # Trained models
│   │   ├── fake_news_model.pkl
│   │   └── tfidf_vectorizer.pkl
│   └── data/                    # Training datasets
│       ├── True.csv
│       └── Fake.csv
│
├── templates/                   # HTML templates
│   ├── base.html
│   └── detector/
│       ├── home.html
│       └── result.html
│
├── static/                      # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
│
├── examples/                    # Test examples
│   ├── real_news.txt
│   ├── fake_news.txt
│   └── README.md
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   └── test_views.py
│
└── docs/                        # Documentation
    ├── deployment.md
    ├── api.md
    └── quickstart.md
```

## ⚙️ Configuration

### Machine Learning Model

The model uses:

- **Vectorizer**: TF-IDF vectorizer with 5000 features
- **Algorithm**: Calibrated LinearSVC (LinearSVC + CalibratedClassifierCV) (SVM) (binary classification)
- **Preprocessing**: Text cleaning, stop word removal, lemmatization
- **Training Data**: 44,898 articles (21,417 real + 23,481 fake)
- **Accuracy**: 98.9% on test set

### Environment Variables

```bash
export DJANGO_SETTINGS_MODULE=fakenews_detector.settings
export DEBUG=True  # Set to False for production
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test tests.test_models
python manage.py test detector.tests
```

### Health Check

Check the API health endpoint:

```bash
curl http://127.0.0.1:8080/health/
```

Expected response:

```json
{
  "status": "OK",
  "model": "loaded",
  "vectorizer": "loaded"
}
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t fake-news-detector .
docker run -p 8080:8080 fake-news-detector
```

### Cloud Platforms

#### Heroku

```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
heroku open
```

#### Railway

```bash
# Connect GitHub repo to Railway
# Automatic deployment on push
```

#### Render

```bash
# Connect GitHub repo to Render
# Set build command: pip install -r requirements.txt
# Set start command: gunicorn fakenews_detector.wsgi:application
```

## 📊 Model Performance

The current model was trained on **44,898 articles** (21,417 real + 23,481 fake):

- **Accuracy**: 98.9%
- **Precision (Real)**: 99%
- **Precision (Fake)**: 99%
- **Recall (Real)**: 99%
- **Recall (Fake)**: 99%
- **F1-Score**: 99%

### Confusion Matrix (on 8,980 test articles)

- Real articles correctly classified: 4,245/4,284
- Fake articles correctly classified: 4,638/4,696
- Total errors: 97 articles (1.1%)

### Generate Clean Examples

To create clean example files from your datasets:

```bash
cd ml
python -c "
import pandas as pd
import os

# Load and sample data
true_df = pd.read_csv('data/True.csv')
fake_df = pd.read_csv('data/Fake.csv')

# Save examples
with open('../examples/real_news.txt', 'w') as f:
    for text in true_df['text'].head(10):
        f.write(text[:500] + '...\n\n')

with open('../examples/fake_news.txt', 'w') as f:
    for text in fake_df['text'].head(10):
        f.write(text[:500] + '...\n\n')
"
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset from [Kaggle Fake News Detection](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
- Built with Django, scikit-learn, and NLTK
- Icons from [Font Awesome](https://fontawesome.com/)

## 🤝 Collaborateurs

Merci aux contributeurs de ce projet :

- **Mohamed Lakssir** — [thejokers69](https://github.com/thejokers69) — Propriétaire du dépôt
- **Houssam Aoun** — [AuroreTBF](https://github.com/AuroreTBF)
- **Ahchouche Firdawsse** — [Firdaws73](https://github.com/Firdaws73)
- **Feth‑Eddine Zineb** — [zinebfthdn](https://github.com/zinebfthdn)

Consultez `CONTRIBUTORS.md` pour plus de détails.

## ⚠️ Avertissement

Ce detector est un outil d'aide à la décision et ne remplace pas l'analyse critique humaine. Les résultats peuvent contenir des erreurs.
