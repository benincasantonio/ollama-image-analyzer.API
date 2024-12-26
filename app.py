from flask import Flask, request, Response, stream_with_context, jsonify
from ollama import chat, generate
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})



@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/describe-image", methods=["POST"])
def describeImage():
    if "image" not in request.files:
        return jsonify({"error": "File not found"}), 400

    if "content" not in request.form:
        return jsonify({"error": "Content not found"}), 400

    image = request.files["image"]

    base64_image = image.read()

    def generate():
        response = chat(
            model="llama3.2-vision",
            messages=[
                {"role": "user", "content": request.form["content"], "images": [base64_image]},
            ],            
            stream=True,

        )
        for response in response:
            yield response.message.content

    return Response(stream_with_context(generate()), content_type="plain/text")
