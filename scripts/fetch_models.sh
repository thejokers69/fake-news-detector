#!/usr/bin/env bash
set -euo pipefail

mkdir -p models

if [ -f models/fake_news_model.pkl ] && [ -f models/tfidf_vectorizer.pkl ]; then
  echo "Models already present; skipping download."
  exit 0
fi

: "${MODEL_URL:?Set MODEL_URL to the fake_news_model.pkl download URL}"
: "${VECTORIZER_URL:?Set VECTORIZER_URL to the tfidf_vectorizer.pkl download URL}"

echo "Downloading model artifacts..."
curl -fL "$MODEL_URL" -o models/fake_news_model.pkl
curl -fL "$VECTORIZER_URL" -o models/tfidf_vectorizer.pkl

echo "Model files fetched:"
ls -lh models
