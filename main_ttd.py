def detect_emotion(text):
    """
    Refactored function to detect emotion from text by checking for keywords.
    Supports easy extension for additional emotions.
    """
    keywords_to_emotions = {
        "happy": ["great", "awesome", "good", "joy", "fantastic"],
        "sad": ["down", "disappointed", "unhappy", "sad"],
        "angry": ["frustrating", "annoying", "angry", "mad"],
        "neutral": ["ordinary", "nothing special", "fine", "okay"],
    }
    lower_text = text.lower()
    for emotion, keywords in keywords_to_emotions.items():
        for keyword in keywords:
            if keyword in lower_text:
                return emotion
    return "unknown"

if __name__ == "__main__":
    # Example usage
    samples = [
        "I am feeling great today! Everything is awesome.",
        "I am so down and disappointed.",
        "This is so frustrating and annoying!",
        "It is an ordinary day with nothing special happening.",
        "",
    ]
    for sample in samples:
        print(f"Text: '{sample}' -> Detected Emotion: {detect_emotion(sample)}")