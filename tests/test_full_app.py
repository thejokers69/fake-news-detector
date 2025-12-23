#!/usr/bin/env python3
"""
End-to-end test for the Fake News Detector application.
Tests that the Django server can start up and respond to basic requests.
"""

import os
import sys
import time
import requests
import subprocess
import signal
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakenews_detector.settings')

import django
django.setup()

from django.test import TestCase
from django.test.utils import get_runner


class TestFullApp(TestCase):
    """End-to-end tests for the complete application"""

    def setUp(self):
        """Set up test fixtures"""
        self.server_process = None
        self.server_url = "http://127.0.0.1:8080"

    def tearDown(self):
        """Clean up after tests"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()

    def test_server_startup_and_health(self):
        """Test that the server starts and health endpoint works"""
        # Start the Django development server
        self.server_process = subprocess.Popen(
            [sys.executable, 'manage.py', 'runserver', '8080', '--noreload'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(__file__).parent.parent
        )

        # Wait for server to start
        time.sleep(3)

        # Test health endpoint
        try:
            response = requests.get(f"{self.server_url}/health/", timeout=10)
            self.assertEqual(response.status_code, 200)

            data = response.json()
            self.assertEqual(data['status'], 'OK')
            self.assertIn('model', data)
            self.assertIn('vectorizer', data)

        except requests.exceptions.RequestException as e:
            self.fail(f"Health endpoint request failed: {e}")

    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        # Start the Django development server
        self.server_process = subprocess.Popen(
            [sys.executable, 'manage.py', 'runserver', '8080', '--noreload'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(__file__).parent.parent
        )

        # Wait for server to start
        time.sleep(3)

        # Test home page
        try:
            response = requests.get(self.server_url, timeout=10)
            self.assertEqual(response.status_code, 200)
            self.assertIn('fake news detector', response.text.lower())

        except requests.exceptions.RequestException as e:
            self.fail(f"Home page request failed: {e}")

    def test_home_page_form_functionality(self):
        """Test that the home page form loads and is functional"""
        # Start the Django development server
        self.server_process = subprocess.Popen(
            [sys.executable, 'manage.py', 'runserver', '8080', '--noreload'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(__file__).parent.parent
        )

        # Wait for server to start
        time.sleep(3)

        # Test home page loads with form
        try:
            response = requests.get(self.server_url, timeout=10)
            self.assertEqual(response.status_code, 200)
            # Check that the form elements are present
            self.assertIn('analyze an article', response.text.lower())
            self.assertIn('textarea', response.text.lower())
            self.assertIn('news_text', response.text)
            self.assertIn('submit', response.text.lower())

        except requests.exceptions.RequestException as e:
            self.fail(f"Home page form test failed: {e}")


if __name__ == '__main__':
    # Run as standalone script for CI/CD
    import unittest

    # Start Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakenews_detector.settings')
    django.setup()

    # Run the tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFullApp)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
