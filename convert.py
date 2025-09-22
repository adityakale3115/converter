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

    # Save to temporary directory
    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, file.filename)
    file.save(input_path)

    # Convert DOC/DOCX -> PDF using LibreOffice
    try:
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", temp_dir,
            input_path
        ], check=True)
    except subprocess.CalledProcessError:
        return "Conversion failed", 500

    # Return PDF
    pdf_filename = file.filename.rsplit(".", 1)[0] + ".pdf"
    pdf_path = os.path.join(temp_dir, pdf_filename)
    if not os.path.exists(pdf_path):
        return "PDF not generated", 500

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
