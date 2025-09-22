from flask import Flask, request, send_file
import subprocess, os, tempfile

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]
    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, file.filename)
    file.save(input_path)

    output_path = os.path.join(temp_dir, os.path.splitext(file.filename)[0] + ".pdf")

    try:
        subprocess.run([
            "libreoffice", "--headless",
            "--convert-to", "pdf",
            "--outdir", temp_dir,
            input_path
        ], check=True)
    except Exception as e:
        return f"Conversion failed: {e}", 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
