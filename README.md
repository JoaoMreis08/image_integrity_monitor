# Image Integrity Monitor

A simple web application that monitors the integrity of images using cryptographic hashing (SHA-256).

This project was developed as a cybersecurity-oriented tool to detect unauthorized changes to product images, such as those used in e-commerce platforms.

## Features

- Upload images through a web interface
- Generate SHA-256 hash for each image
- Detect image modifications
- Store hashes locally (no database required)
- Modern, responsive interface with preview cards

## Technologies Used

- Python
- Flask
- HTML & CSS
- SHA-256 Cryptographic Hashing

## Project Structure

- `app.py` Flask application
- `templates/index.html` Main page
- `static/style.css` Styling
- `images/` Uploaded images
- `hashes.json` Local hash registry

## Run

1. Install dependencies
   - `pip install -r requirements.txt`
1. Start the app
   - `python app.py`
1. Open `http://127.0.0.1:5000/`
