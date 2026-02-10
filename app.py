from flask import Flask, render_template, request
import hashlib
import os
import json

app = Flask(__name__)

IMAGES_DIR = "images"
HASH_FILE = "hashes.json"

os.makedirs(IMAGES_DIR, exist_ok=True)

def calculate_hash(path):
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(data):
    with open(HASH_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    hashes = load_hashes()

    if request.method == "POST":
        file = request.files["image"]

        if file:
            path = os.path.join(IMAGES_DIR, file.filename)
            file.save(path)

            new_hash = calculate_hash(path)

            if file.filename in hashes:
                if hashes[file.filename] == new_hash:
                    message = f"{file.filename} — OK (sem alterações)"
                else:
                    message = f"{file.filename} — ALTERADA!"
                    hashes[file.filename] = new_hash
            else:
                hashes[file.filename] = new_hash
                message = f"{file.filename} — nova imagem registada"

            save_hashes(hashes)

    return render_template("index.html", message=message, hashes=hashes)

if __name__ == "__main__":
    app.run(debug=True)
