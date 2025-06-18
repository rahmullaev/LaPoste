from flask import Flask, render_template, request
import requests
import json
import os
from fake_useragent import UserAgent

app = Flask(__name__)
ua = UserAgent()

# === Флаг переключения источника данных ===
USE_LOCAL_DATA = False  # True = читать из data.json, False = с сайта La Poste

DATA_FILE = 'data.json'

def fetch_tracking_data(track_code):
    url = f'https://www.laposte.fr/ssu/sun/back/suivi-unifie/{track_code}'
    params = {'lang': 'fr'}
    try:
        HEADERS = {
            'User-Agent': ua.chrome,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8',
            'Referer': f'https://www.laposte.fr/outils/suivre-vos-envois?code={track_code}'
        }

        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            data = data[0]
        return data
    except Exception as e:
        print(f"[Ошибка запроса] {e}")
        return None

def load_local_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    data = data[0]
                return data
            except Exception as e:
                print(f"[Ошибка чтения файла] {e}")
    return None



@app.route("/", methods=["GET", "POST"])
def index():
    events = []
    track_code = ""
    if request.method == "POST":
        track_code = request.form.get("track_number", "").strip()
        if track_code or USE_LOCAL_DATA:
            data = load_local_data() if USE_LOCAL_DATA else fetch_tracking_data(track_code)
            if data:
                events = data.get("shipment", {}).get("event", [])
                #events = sorted(events, key=lambda x: x.get("date", ""))
    return render_template("index.html", events=events, track_code=track_code)

if __name__ == "__main__":
    app.run(debug=True)
