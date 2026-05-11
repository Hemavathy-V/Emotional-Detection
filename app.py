from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline

app = Flask(__name__)

print("⚡ Loading AI model...")
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)
print("✅ Model ready!")


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    body = request.get_json(silent=True) or {}
    text = body.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided."}), 400

    raw = emotion_pipeline(text)
    items = raw[0] if isinstance(raw[0], list) else raw
    scores = {r["label"].lower(): round(r["score"] * 100, 1) for r in items}
    top = max(scores, key=scores.get)

    return jsonify({"emotion": top, "confidence": scores[top], "scores": scores})


if __name__ == "__main__":
    app.run(port=5000, debug=False)
