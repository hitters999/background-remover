import base64
import io
import os

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
from rembg import remove

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}
MAX_FILE_SIZE = 50 * 1024 * 1024
MAX_PIXELS = 40_000_000
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def remove_background_bytes(image_data: bytes) -> bytes:
    if not image_data:
        raise ValueError("The uploaded image is empty")
    try:
        with Image.open(io.BytesIO(image_data)) as image:
            if image.width * image.height > MAX_PIXELS:
                raise ValueError("Image dimensions are too large; please use an image under 40 megapixels")
            image.verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("The uploaded file is not a valid image") from exc

    # rembg returns a PNG with an alpha channel for the foreground.
    result = remove(image_data)
    with Image.open(io.BytesIO(result)) as output_image:
        output = io.BytesIO()
        output_image.convert("RGBA").save(output, format="PNG", optimize=True)
        return output.getvalue()


def json_image_response(png_bytes: bytes):
    encoded = base64.b64encode(png_bytes).decode("ascii")
    return jsonify({
        "success": True,
        "image": f"data:image/png;base64,{encoded}",
        "content_type": "image/png",
    })


@app.get("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Background Remover API is running",
        "endpoints": {"remove": "/api/remove", "remove_bg": "/api/remove-bg", "health": "/api/health"},
    })


@app.get("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "background-remover", "version": "1.1.0"})


@app.post("/api/remove")
def remove_background_multipart():
    uploaded = request.files.get("image")
    if uploaded is None or not uploaded.filename:
        return jsonify({"success": False, "error": "No image file provided"}), 400
    if not allowed_file(uploaded.filename):
        return jsonify({"success": False, "error": "Unsupported image type. Use PNG, JPG, JPEG, GIF, BMP, or WEBP"}), 400
    try:
        output = remove_background_bytes(uploaded.read())
        return send_file(io.BytesIO(output), mimetype="image/png", as_attachment=True, download_name="image-no-background.png")
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception("Background removal failed")
        return jsonify({"success": False, "error": "Background removal failed. Please try another image."}), 500


@app.post("/api/remove-bg")
def remove_background_json():
    payload = request.get_json(silent=True) or {}
    data_url = payload.get("image", "")
    if not isinstance(data_url, str) or not data_url.startswith("data:image/"):
        return jsonify({"success": False, "error": "Send an image data URL in the image field"}), 400
    try:
        encoded = data_url.split(",", 1)[1]
        image_data = base64.b64decode(encoded, validate=True)
        output = remove_background_bytes(image_data)
        return json_image_response(output)
    except (ValueError, base64.binascii.Error) as exc:
        return jsonify({"success": False, "error": str(exc) or "Invalid image data"}), 400
    except Exception:
        app.logger.exception("Background removal failed")
        return jsonify({"success": False, "error": "Background removal failed. Please try another image."}), 500


@app.get("/api/stats")
def stats():
    return jsonify({
        "service": "Background Remover",
        "ai_model": "rembg",
        "supported_formats": sorted(ALLOWED_EXTENSIONS),
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024),
        "processing": "AI-powered server-side rembg segmentation",
        "output_format": "PNG with transparency",
    })


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"success": False, "error": "Image is too large. Maximum size is 50 MB."}), 413


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
