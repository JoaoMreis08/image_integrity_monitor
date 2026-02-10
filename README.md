# 🔐 Image Integrity Monitor

A simple web application that monitors the integrity of images using cryptographic hashing (SHA-256).

This project was developed as a cybersecurity-oriented tool to detect unauthorized changes to product images, such as those used in e-commerce platforms.

---

## 🚀 Features

- Upload images through a web interface
- Generate SHA-256 hash for each image
- Detect image modifications
- Store hashes locally (no database required)
- Simple and clean web interface

---

## 🛠️ Technologies Used

- Python
- Flask
- HTML & CSS
- SHA-256 Cryptographic Hashing

---

## 📂 Project Structure

image_integrity_monitor/
├── app.py
├── requirements.txt
├── templates/
│ └── index.html
├── static/
│ └── style.css
├── images/ # ignored (local only)
├── hashes.json # ignored (local only)


---

## ▶️ How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
