from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess, os, tempfile

app = Flask(__name__)
CORS(app)

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, file.filename)
    file.save(input_path)

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", temp_dir,
        input_path
    ], check=True)

    pdf_path = os.path.join(temp_dir, file.filename.rsplit('.', 1)[0] + ".pdf")
    if not os.path.exists(pdf_path):
        return "Conversion failed", 500

    return send_file(pdf_path, as_attachment=True)
