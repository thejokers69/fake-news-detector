import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class TestViews(TestCase):
    """Test cases for Django views"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_home_view(self):
        """Test home page view"""
        response = self.client.get(reverse('detector:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detector/home.html')

    def test_about_view(self):
        """Test about page view"""
        response = self.client.get(reverse('detector:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detector/about.html')

    def test_home_view_direct_url(self):
        """Test home page view with direct URL"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detector/home.html')

    @patch('detector.views.predict_fake_news')
    def test_analyze_view_post_valid(self, mock_predict):
        """Test analyze view with valid POST data"""
        # Mock the prediction result
        mock_predict.return_value = {
            "label": "Real",
            "probability": 0.95,
            "processed_text": "processed text"
        }

        test_text = "This is a test news article about technology."
        response = self.client.post(reverse('detector:analyze'), {'news_text': test_text})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detector/result.html')

        # Check that context contains prediction data
        self.assertIn('prediction', response.context)
        self.assertIn('submitted_text', response.context)
        self.assertEqual(response.context['submitted_text'], test_text)

        # Verify prediction was called
        mock_predict.assert_called_once_with(test_text)

    def test_analyze_view_post_empty(self):
        """Test analyze view with empty POST data"""
        response = self.client.post(reverse('detector:analyze'), {'news_text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detector/result.html')

        # Check that error prediction is returned
        prediction = response.context['prediction']
        self.assertEqual(prediction['label'], 'Erreur')
        self.assertEqual(prediction['probability'], 0.0)
        self.assertIn('error', prediction)

    def test_analyze_view_get(self):
        """Test analyze view with GET request redirects to home"""
        response = self.client.get(reverse('detector:analyze'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detector/home.html')

    def test_health_view(self):
        """Test health endpoint"""
        response = self.client.get(reverse('detector:health'))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['status'], 'OK')
        self.assertIn('model', data)
        self.assertIn('vectorizer', data)

        # Model and vectorizer status should be either "loaded" or "not loaded"
        self.assertIn(data['model'], ['loaded', 'not loaded'])
        self.assertIn(data['vectorizer'], ['loaded', 'not loaded'])

    def test_health_view_direct_url(self):
        """Test health endpoint with direct URL"""
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['status'], 'OK')


if __name__ == "__main__":
    import unittest
    unittest.main()
