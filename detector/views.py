from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ml.model import predict_fake_news


def home(request):
    """Page d'accueil avec le formulaire"""
    return render(request, "detector/home.html")


@csrf_exempt
def analyze(request):
    """Vue pour analyser le texte soumis"""
    if request.method == "POST":
        # Récupérer le texte du formulaire
        news_text = request.POST.get("news_text", "").strip()

        if not news_text:
            prediction = {
                "label": "Erreur",
                "probability": 0.0,
                "error": "Veuillez entrer du texte à analyser",
            }
        else:
            # Effectuer la prédiction
            prediction = predict_fake_news(news_text)

        # Ajouter des informations supplémentaires pour l'affichage
        prediction["input_preview"] = news_text[:240]
        prediction["input_length"] = len(news_text)
        prediction["confidence_percent"] = round(prediction["probability"] * 100, 1)

        return render(
            request,
            "detector/result.html",
            {"prediction": prediction, "submitted_text": news_text},
        )

    # Si ce n'est pas une requête POST, rediriger vers la page d'accueil
    return render(request, "detector/home.html")


def about(request):
    """About page with project information"""
    return render(request, "detector/about.html")


def health(request):
    """Health endpoint to check models status"""
    from ml.model import model, vectorizer

    model_status = "loaded" if model is not None else "not loaded"
    vectorizer_status = "loaded" if vectorizer is not None else "not loaded"

    return JsonResponse(
        {"status": "OK", "model": model_status, "vectorizer": vectorizer_status}
    )
