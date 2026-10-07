import io
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        quality = int(request.form.get("quality", 50))

        if not file or file.filename == "":
            return "No file selected", 400

        # Read image safely
        img = Image.open(file)

        # Convert to RGB if PNG/RGBA
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="image/jpeg",
            as_attachment=True,
            download_name=f"compressed_{file.filename}.jpg",
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)