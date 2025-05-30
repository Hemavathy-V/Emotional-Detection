import unittest
from main_ttd import detect_emotion  # Import the function from refactor_code.py

class TestEmotionDetection(unittest.TestCase):

    def test_detect_happy_emotion(self):
        text = "I am feeling great today! Everything is awesome."
        expected_emotion = "happy"
        self.assertEqual(detect_emotion(text), expected_emotion)

    def test_detect_sad_emotion(self):
        text = "I am so down and disappointed."
        expected_emotion = "sad"
        self.assertEqual(detect_emotion(text), expected_emotion)

    def test_detect_angry_emotion(self):
        text = "This is so frustrating and annoying!"
        expected_emotion = "angry"
        self.assertEqual(detect_emotion(text), expected_emotion)

    def test_detect_neutral_emotion(self):
        text = "It is an ordinary day with nothing special happening."
        expected_emotion = "neutral"
        self.assertEqual(detect_emotion(text), expected_emotion)

    def test_detect_unknown_emotion(self):
        text = ""
        expected_emotion = "unknown"
        self.assertEqual(detect_emotion(text), expected_emotion)

if __name__ == "__main__":
    unittest.main()