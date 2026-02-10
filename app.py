from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

app = Flask(__name__)

IMAGES_DIR = Path("images")
HASH_FILE = Path("hashes.json")
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}

# 10 MB upload limit to keep the app responsive
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

IMAGES_DIR.mkdir(exist_ok=True)


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def save_and_hash(file_storage, dest_path: Path):
    sha256 = hashlib.sha256()
    size = 0
    with dest_path.open("wb") as f:
        for block in iter(lambda: file_storage.stream.read(8192), b""):
            size += len(block)
            sha256.update(block)
            f.write(block)
    return sha256.hexdigest(), size


def load_hashes():
    if HASH_FILE.exists():
        with HASH_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Migrate legacy format: {"filename": "hash"}
        for name, value in list(data.items()):
            if isinstance(value, str):
                data[name] = {
                    "hash": value,
                    "size": None,
                    "updated_at": None,
                }
        return data
    return {}


def save_hashes(data):
    tmp_path = HASH_FILE.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=True)
    tmp_path.replace(HASH_FILE)


@app.route("/images/<path:filename>")
def uploaded_image(filename):
    return send_from_directory(IMAGES_DIR, filename, max_age=3600)


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    hashes = load_hashes()

    if request.method == "POST":
        file = request.files.get("image")
        if not file or not file.filename:
            message = "Nenhum ficheiro selecionado."
        else:
            safe_name = secure_filename(file.filename)
            if not safe_name or not allowed_file(safe_name):
                message = "Formato de ficheiro nao suportado."
            else:
                path = IMAGES_DIR / safe_name
                new_hash, size = save_and_hash(file, path)

                if safe_name in hashes:
                    if hashes[safe_name]["hash"] == new_hash:
                        message = f"{safe_name} - OK (sem alteracoes)"
                    else:
                        message = f"{safe_name} - ALTERADA!"
                else:
                    message = f"{safe_name} - nova imagem registada"

                hashes[safe_name] = {
                    "hash": new_hash,
                    "size": size,
                    "updated_at": utc_now_iso(),
                }
                save_hashes(hashes)

    # Sort by most recent first, keep stable order for None timestamps
    sorted_items = sorted(
        hashes.items(),
        key=lambda item: item[1].get("updated_at") or "",
        reverse=True,
    )

    return render_template("index.html", message=message, hashes=sorted_items)


if __name__ == "__main__":
    app.run(debug=True)
