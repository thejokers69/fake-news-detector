# Copilot Instructions for fake-news-detector

- Purpose: Django UI + Calibrated LinearSVC (SVM) TF‑IDF classifier for fake/real news; entrypoints live in Django views (`detector.views`) and templates under [templates/](templates/).
- Runtime: server binds 0.0.0.0:8080 when running via `python manage.py runserver`; prefer `python manage.py runserver` for local testing and `python train.py` for retraining.
- Endpoints: `/` renders form, `/analyze` (POST) consumes `news_text`, `/health` returns JSON status; logic lives in `detector/views.py`.
- Prediction contract: `predict_fake_news(text)` returns dict with `label` ('Fake'|'Real'|'Erreur'), `probability`, optional `processed_text`/`error`; templates expect that shape.
- Model IO: globals `model` and `vectorizer` loaded from `ml/models/fake_news_model.pkl` and `ml/models/tfidf_vectorizer.pkl` via `load_models()` in `ml/model.py`; keep filenames stable or update constants.
- Text preprocessing (must stay aligned with training): lowercasing, strip non-letters, split, drop English stop words, WordNet lemmatization in `ml/model.py` and mirrored in `ml/train.py`.
- Training pipeline in [train.py](ml/train.py): loads DATASETS/True.csv and Fake.csv, combines title + text to `content`, preprocesses, TF‑IDF (max_features=5000, ngram_range=(1,3), min_df=5, max_df=0.6, sublinear_tf=True), LinearSVC trained and wrapped with `CalibratedClassifierCV` for probability outputs; saves artifacts to `ml/models/`.
- NLTK resources: downloads stopwords/wordnet/omw-1.4 at runtime; `nltk_data` path appended to `./nltk_data` in `ml/model.py`; ensure offline environments include these assets.
- Frontend expectations: Bootstrap 5 CDN; template shows progress bar and labels based on `prediction.label` and `prediction.probability` in [templates/index.html](templates/index.html); keep keys stable if changing backend.
- Demo script [demo.py](demo.py) boots server, posts examples from Exemples files, and tears down the process group; avoid port conflicts before running.
- Example generation: [clean_text.py](clean_text.py) pulls first rows from DATASETS/True.csv and Fake.csv, cleans basic whitespace/quotes, writes examples_true_clean.txt and examples_fake_clean.txt in repo root (moved to Exemples/ by organize script).
- Project scaffolding helper [organize_project.py](organize_project.py) creates folders and moves example/test files; mind side effects if rerun after edits.
- Emoji scrubber [clean_emojis.py](clean_emojis.py) replaces emojis across .py files; rarely needed but will overwrite files in place.
- Tests: fast model smoke in [Tests/test_models.py](Tests/test_models.py) imports `ml.model`, calls `load_models()` + `predict_fake_news`; endpoint checks in [Tests/test_app.py](Tests/test_app.py) expect server already running on 8080; end-to-end in [Tests/test_full_app.py](Tests/test_full_app.py) starts its own server and stops it.
- Typical commands: `pip install -r requirements.txt`; `python manage.py runserver` (serve); `python ml/train.py` (retrain + write models/); `python Tests/test_app.py` (needs running server) or `python Tests/test_full_app.py` (self-starts server).
- Data assumptions: CSVs in DATASETS/ with columns title/text/subject; labels encoded 0=Real, 1=Fake; training stratifies 80/20 split; keep schema when swapping datasets.
- Error handling: if model/vectorizer missing, `/health` reports "non chargé" and predictions return label "Erreur" with probability 0.0; templates render error messages when provided.
- Style/conventions: outputs and logs are French; keep user-facing text consistent; avoid introducing new framework conventions (stick to Django, joblib, scikit-learn, NLTK already in use).
- Deployment: README documents Docker snippet and PaaS options; port 8080 is assumed in docs and tests—update docs/tests together if changing.
- When extending features, preserve preprocessing parity between app and training, keep probability as float in [0,1], and ensure new routes/templates maintain Bootstrap form submit to `/predict`.
- If modifying health/predict responses, update tests and template conditions accordingly to prevent regressions.

Feedback welcome: note any gaps or unclear behaviors, especially around model files, dataset schema, or test expectations, so we can refine this guide.
