import unittest

class TestEmotionDetection(unittest.TestCase):

    def test_detect_happy_emotion(self):
        text = "I am feeling great today! Everything is awesome."
        expected_emotion = "happy"
        self.assertEqual(detect_emotion(text), expected_emotion)

if __name__ == "__main__":
    # Running this will raise NameError: name 'detect_emotion' is not defined
    unittest.main()
