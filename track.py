import requests
import json
import os
import sys
from datetime import datetime

try:
    from fake_useragent import UserAgent
    ua = UserAgent()
    USER_AGENT = ua.chrome
except:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

# === Константы ===
URL = 'https://www.laposte.fr/ssu/sun/back/suivi-unifie/86503506522946O'
PARAMS = {'lang': 'fr'}
HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8',
    'Referer': 'https://www.laposte.fr/outils/suivre-vos-envois?code=86503506522946O'
}
FILE_NAME = 'data.json'

# === Получение данных ===
def fetch_tracking_data():
    try:
        print("[*] Запрос к серверу...")
        response = requests.get(URL, headers=HEADERS, params=PARAMS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[Ошибка запроса] {e}")
        return None

# === Сохранение JSON ===
def save_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[✓] Данные сохранены в файл: {file_path}")
    except Exception as e:
        print(f"[Ошибка сохранения] {e}")

# === Загрузка JSON ===
def load_json(file_path):
    if not os.path.exists(file_path):
        print("[!] Файл не найден.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Ошибка чтения файла] {e}")
        return None

# === Вывод событий ===
def print_events(data):
    try:
        # Если data — список, берем первый элемент
        if isinstance(data, list):
            data = data[0]

        events = data.get('shipment', {}).get('event', [])
        if not events:
            print("[!] События не найдены.")
            return

        print(f"\n[События] Всего: {len(events)}\n")
        for e in sorted(events, key=lambda x: x.get("order", 0), reverse=True):
            print(f"🕒 {e.get('date')} — {e.get('label')}")
    except Exception as e:
        print(f"[Ошибка обработки событий] {e}")



# === Главная логика ===
def main():
    update = '--update' in sys.argv or '-u' in sys.argv

    if update:
        print("[*] Принудительное обновление данных с сервера.")
        data = fetch_tracking_data()
        if data:
            save_json(data, FILE_NAME)
    else:
        print("[i] Используем локальный файл:", FILE_NAME)

    data = load_json(FILE_NAME)
    if data:
        print_events(data)

if __name__ == "__main__":
    main()
