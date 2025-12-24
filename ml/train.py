#!/usr/bin/env python3
"""
Train an SVM-based classifier for fake-news detection and save artifacts
in `ml/models` using filenames expected by the application loader.
"""

from pathlib import Path
import os
import re
import joblib
import pandas as pd
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, classification_report

# Ensure NLTK resources are present
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

TRUE_FILE = DATASETS_DIR / "True.csv"
FAKE_FILE = DATASETS_DIR / "Fake.csv"

MODEL_PATH = MODELS_DIR / "fake_news_model.pkl"  # matches ml/model.py
VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.pkl"

# Preprocessing
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """Clean HTML/URLs, keep letters, normalize whitespace, lowercase, remove stopwords and lemmatize."""
    if not isinstance(text, str):
        return ""

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Keep letters and whitespace only
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Lowercase
    text = text.lower()

    # Tokenize, remove stop words, lemmatize
    words = [w for w in text.split() if w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]

    return " ".join(words)


def main(sample: int | None = None):
    # Load CSVs
    df_true = pd.read_csv(TRUE_FILE)
    df_fake = pd.read_csv(FAKE_FILE)

    # Labels: 0 = Real, 1 = Fake (same as ml.model.py expects)
    df_true["label"] = 0
    df_fake["label"] = 1

    # Combine text
    df_true["content"] = df_true["title"].fillna("") + " " + df_true["text"].fillna("")
    df_fake["content"] = df_fake["title"].fillna("") + " " + df_fake["text"].fillna("")

    df = pd.concat([df_true, df_fake], ignore_index=True)

    # Optional sampling for quick local tests
    if sample is not None:
        df = df.sample(n=sample, random_state=42).reset_index(drop=True)

    df = df[["content", "label"]].sample(frac=1, random_state=42).reset_index(drop=True)

    # Preprocess
    df["content"] = df["content"].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["content"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        min_df=5,
        max_df=0.6,
        sublinear_tf=True,
        max_features=5000,
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    svm = LinearSVC(random_state=42, max_iter=10000)
    model = CalibratedClassifierCV(svm, method="sigmoid", cv=5)

    print("Training SVM (this may take a few minutes)...")
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy:", round(accuracy, 4))
    print(classification_report(y_test, y_pred))

    # Persist artifacts in ml/models with the expected filenames
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"Saved model -> {MODEL_PATH}")
    print(f"Saved vectorizer -> {VECTORIZER_PATH}")


if __name__ == "__main__":
    main()
