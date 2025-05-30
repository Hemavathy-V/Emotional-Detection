import pytest
from unittest.mock import patch
from main_prgm import detect_emotion

# Test that detect_emotion returns correct mocked label
def test_detect_emotion_returns_joy(mock_pipeline):
    mock_pipeline.return_value = [{"label": "joy", "score": 0.99}]
    result = detect_emotion("I'm so happy today!")
    assert result == "joy"

def test_detect_emotion_returns_anger(mock_pipeline):
    mock_pipeline.return_value = [{"label": "anger", "score": 0.92}]
    result = detect_emotion("I'm furious about what happened!")
    assert result == "anger"

def test_detect_emotion_returns_sadness(mock_pipeline):
    mock_pipeline.return_value = [{"label": "sadness", "score": 0.87}]
    result = detect_emotion("I feel very down today.")
    assert result == "sadness"

# test behavior when model returns empty (edge case)
def test_detect_emotion_empty_response(mock_pipeline):
    mock_pipeline.return_value = []
    with pytest.raises(IndexError):
        detect_emotion("This might break the model.")
