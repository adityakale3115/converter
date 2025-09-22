from flask import Flask, request, send_file
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400

    uploaded_file = request.files['file']
    with tempfile.TemporaryDirectory() as tmpdir:
        doc_path = os.path.join(tmpdir, uploaded_file.filename)
        uploaded_file.save(doc_path)
        pdf_path = os.path.join(tmpdir, "output.pdf")

        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            tmpdir,
            doc_path
        ], check=True)

        return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
