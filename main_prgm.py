from langchain.chains.base import Chain
from transformers import pipeline
from typing import ClassVar, List, Dict
import streamlit as st

# Load the emotion detection pipeline from Hugging Face
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Define a function that uses the Hugging Face model for emotion detection
def detect_emotion(text: str) -> str:
    result = emotion_pipeline(text)
    return result[0]['label']  

# Define a custom chain that uses the Hugging Face emotion detection model
class EmotionDetectionChain(Chain):
    input_keys: ClassVar[List[str]] = ["text"]  
    output_keys: ClassVar[List[str]] = ["emotion"]  

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        text = inputs.get("text", "")
        if text:
            emotion = detect_emotion(text)
            return {"emotion": emotion}
        return {"emotion": "No emotion detected."}

# Create an instance of the custom chain
emotion_chain = EmotionDetectionChain()

st.title("Share and Test Your Emotional Level Here...")
st.write("Enter a sentence to detect the emotion.")
user_input = st.text_input("Enter emotional sentence here:")
if st.button("Submit"):
    output = emotion_chain.invoke({"text": user_input})
    st.write(f"Detected Emotion: {output['emotion']}")