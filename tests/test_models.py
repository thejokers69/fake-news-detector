import unittest
from ml.model import load_models, predict_fake_news, preprocess_text
from pathlib import Path


class TestMLModel(unittest.TestCase):
    """Test cases for the machine learning model functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests"""
        # Load models for testing
        cls.models_loaded = load_models()

    def test_models_loaded(self):
        """Test that models are loaded successfully"""
        self.assertTrue(self.models_loaded, "Models should be loaded successfully")

    def test_preprocess_text(self):
        """Test text preprocessing function"""
        # Test normal text
        text = "This is a TEST with numbers 123 and symbols @#$!"
        processed = preprocess_text(text)
        self.assertIsInstance(processed, str)
        self.assertNotIn("123", processed)
        self.assertNotIn("@#$!", processed)

        # Test empty text
        empty_processed = preprocess_text("")
        self.assertEqual(empty_processed, "")

        # Test None input
        none_processed = preprocess_text(None)
        self.assertEqual(none_processed, "")

    def test_predict_fake_news_real(self):
        """Test prediction on real news text"""
        real_news = """
        WASHINGTON (Reuters) - The United States Senate on Tuesday approved a $1.3 trillion
        spending bill to fund government operations through September, avoiding a government shutdown.
        The bill, which funds nine of the 12 government agencies, now goes to President Donald Trump
        for his signature. The Senate voted 83-16 to approve the measure.
        """

        result = predict_fake_news(real_news)

        # Check result structure
        self.assertIn("label", result)
        self.assertIn("probability", result)
        self.assertIsInstance(result["probability"], float)
        self.assertGreaterEqual(result["probability"], 0.0)
        self.assertLessEqual(result["probability"], 1.0)

    def test_predict_fake_news_fake(self):
        """Test prediction on fake news text"""
        fake_news = """
        BREAKING: Scientists have discovered that eating chocolate cures all diseases!
        A new study from Harvard University shows that consuming just one chocolate bar per day
        eliminates cancer, heart disease, and even aging. The FDA has approved emergency distribution
        of chocolate to all citizens immediately. Stock up now before it's too late!
        """

        result = predict_fake_news(fake_news)

        # Check result structure
        self.assertIn("label", result)
        self.assertIn("probability", result)
        self.assertIsInstance(result["probability"], float)
        self.assertGreaterEqual(result["probability"], 0.0)
        self.assertLessEqual(result["probability"], 1.0)

    def test_predict_fake_news_empty(self):
        """Test prediction on empty text"""
        result = predict_fake_news("")

        # Empty text gets processed and classified (may be classified as Fake or Real)
        self.assertIn("label", result)
        self.assertIn("probability", result)
        self.assertIsInstance(result["probability"], float)
        self.assertIn(result["label"], ["Real", "Fake", "Erreur"])
        self.assertGreaterEqual(result["probability"], 0.0)
        self.assertLessEqual(result["probability"], 1.0)

    def test_model_files_exist(self):
        """Test that model files exist"""
        base_dir = Path(__file__).resolve().parent.parent
        model_path = base_dir / "ml" / "models" / "fake_news_model.pkl"
        vectorizer_path = base_dir / "ml" / "models" / "tfidf_vectorizer.pkl"

        self.assertTrue(model_path.exists(), f"Model file should exist at {model_path}")
        self.assertTrue(vectorizer_path.exists(), f"Vectorizer file should exist at {vectorizer_path}")


if __name__ == "__main__":
    unittest.main()
