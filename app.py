# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# PENTING: Untuk produksi, ganti "*" dengan domain GitHub Pages Anda
# Contoh: CORS(app, resources={r"/*": {"origins": "https://mithanada8.github.io"}})
CORS(app)

# --- PENTING: KUNCI API ANDA DI SINI ---
# Sangat disarankan untuk menggunakan environment variables untuk keamanan.
# Contoh:
# API_KEY_GEMINI = os.environ.get("GEMINI_API_KEY")
# API_KEY_IMAGEN = os.environ.get("IMAGEN_API_KEY")

# Untuk pengujian cepat, Anda bisa menempatkan kunci API langsung di sini,
# TETAPI JANGAN LAKUKAN INI UNTUK PRODUKSI PUBLIK.
API_KEY_GEMINI = "AIzaSyActb6sYI7wr_esoDPkK_vfBaKBVhsDeEk" # Kunci API yang Anda berikan
API_KEY_IMAGEN = "AIzaSyActb6sYI7wr_esoDPkK_vfBaKBVhsDeEk" # Biasanya sama

@app.route('/proxy/gemini-flash', methods=['POST'])
def proxy_gemini_flash():
    """
    Proxy untuk API Gemini 2.0 Flash (untuk terjemahan prompt).
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={AIzaSyActb6sYI7wr_esoDPkK_vfBaKBVhsDeEk}"

        headers = {'Content-Type': 'application/json'}
        response = requests.post(gemini_api_url, json=data, headers=headers)
        response.raise_for_status()

        return jsonify(response.json()), response.status_code

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error from Gemini API: {e.response.status_code} - {e.response.text}")
        return jsonify({"error": "Gemini API call failed", "details": e.response.text}), e.response.status_code
    except Exception as e:
        print(f"An unexpected error occurred in Gemini proxy: {e}")
        return jsonify({"error": "Internal server error in Gemini proxy", "details": str(e)}), 500

@app.route('/proxy/imagen-predict', methods=['POST'])
def proxy_imagen_predict():
    """
    Proxy untuk API Imagen 3.0 (untuk pembuatan gambar).
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        imagen_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={AIzaSyActb6sYI7wr_esoDPkK_vfBaKBVhsDeEk}"

        headers = {'Content-Type': 'application/json'}
        response = requests.post(imagen_api_url, json=data, headers=headers)
        response.raise_for_status()

        return jsonify(response.json()), response.status_code

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error from Imagen API: {e.response.status_code} - {e.response.text}")
        return jsonify({"error": "Imagen API call failed", "details": e.response.text}), e.response.status_code
    except Exception as e:
        print(f"An unexpected error occurred in Imagen proxy: {e}")
        return jsonify({"error": "Internal server error in Imagen proxy", "details": str(e)}), 500

if __name__ == '__main__':
    # Jalankan aplikasi Flask
    # Untuk produksi, Anda akan menggunakan Gunicorn atau server WSGI lainnya
    # Ganti port jika diperlukan, misalnya untuk deployment lokal
    app.run(debug=True, port=5000) # debug=True hanya untuk pengembangan

