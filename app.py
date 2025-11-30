# app.py
# Импортируем необходимые библиотеки
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import folium
import json
from geopy.distance import geodesic
import threading
import time
import random

# Создаём Flask-приложение и SocketIO для реального времени
app = Flask(__name__, static_folder='static')
socketio = SocketIO(app)

# Инициализация базы данных
def init_db():
    # Подключаемся к SQLite (база создаётся автоматически, если её нет)
    conn = sqlite3.connect('utm.db')
    c = conn.cursor()
    # Создаём таблицы для дронов, пилотов и заявок
    c.execute('''CREATE TABLE IF NOT EXISTS drones 
                 (id INTEGER PRIMARY KEY, brand TEXT, model TEXT, serial TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pilots 
                 (id INTEGER PRIMARY KEY, name TEXT, contact TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS flight_requests 
                 (id INTEGER PRIMARY KEY, drone_id INTEGER, pilot_id INTEGER, 
                  route TEXT, altitude INTEGER, time TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# Вызываем инициализацию базы данных
init_db()

# Определяем запретные зоны (пример: круг вокруг аэропорта Астаны)
FORBIDDEN_ZONES = [
    {"center": (51.1801, 71.4451), "radius_km": 10}  # Аэропорт Астаны
]

# Проверка, пересекает ли точка запретную зону
def check_forbidden_zone(point):
    # point - кортеж (широта, долгота)
    for zone in FORBIDDEN_ZONES:
        # Вычисляем расстояние от точки до центра зоны
        distance = geodesic(point, zone["center"]).km
        if distance <= zone["radius_km"]:
            return False  # Точка в запретной зоне
    return True  # Точка безопасна

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Регистрация дрона
@app.route('/register_drone', methods=['POST'])
def register_drone():
    # Получаем данные из формы
    brand = request.form['brand']
    model = request.form['model']
    serial = request.form['serial']
    
    # Сохраняем в базу данных
    conn = sqlite3.connect('utm.db')
    c = conn.cursor()
    c.execute("INSERT INTO drones (brand, model, serial) VALUES (?, ?, ?)",
              (brand, model, serial))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Дрон зарегистрирован"})

# Регистрация пилота
@app.route('/register_pilot', methods=['POST'])
def register_pilot():
    name = request.form['name']
    contact = request.form['contact']
    
    conn = sqlite3.connect('utm.db')
    c = conn.cursor()
    c.execute("INSERT INTO pilots (name, contact) VALUES (?, ?)",
              (name, contact))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Пилот зарегистрирован"})

# Подача заявки на полёт
@app.route('/submit_flight_request', methods=['POST'])
def submit_flight_request():
    drone_id = request.form['drone_id']
    pilot_id = request.form['pilot_id']
    route = request.form['route']  # JSON-строка с точками маршрута
    altitude = request.form['altitude']
    time = request.form['time']
    
    # Проверяем маршрут на запретные зоны
    try:
        route_points = json.loads(route)  # Парсим JSON в список точек
        for point in route_points:
            if not check_forbidden_zone((point['lat'], point['lng'])):
                return jsonify({"status": "rejected", "message": "Маршрут пересекает запретную зону"})
    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Неверный формат маршрута"})
    
    # Сохраняем заявку в базу
    conn = sqlite3.connect('utm.db')
    c = conn.cursor()
    c.execute("INSERT INTO flight_requests (drone_id, pilot_id, route, altitude, time, status) VALUES (?, ?, ?, ?, ?, ?)",
              (drone_id, pilot_id, route, altitude, time, "approved"))
    conn.commit()
    conn.close()
    return jsonify({"status": "approved", "message": "Заявка одобрена"})

# Страница с картой мониторинга
@app.route('/monitor')
def monitor():
    # Создаём карту с центром в Астане
    m = folium.Map(location=[51.1801, 71.4451], zoom_start=10)
    # Добавляем запретные зоны на карту
    for zone in FORBIDDEN_ZONES:
        folium.Circle(
            radius=zone["radius_km"] * 1000,  # в метрах
            location=zone["center"],
            color="red",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)
    # Сохраняем карту в HTML
    m.save('templates/map.html')
    return render_template('map.html')

# Эмуляция телеметрии дрона
def simulate_drone():
    while True:
        # Эмулируем движение дрона (случайные координаты около Астаны)
        lat = 51.1801 + random.uniform(-0.1, 0.1)
        lng = 71.4451 + random.uniform(-0.1, 0.1)
        # Проверяем, не в запретной ли зоне дрон
        if not check_forbidden_zone((lat, lng)):
            socketio.emit('alert', {'message': 'Дрон в запретной зоне!'})
        # Отправляем координаты через WebSocket
        socketio.emit('drone_position', {'lat': lat, 'lng': lng})
        time.sleep(2)  # Обновление каждые 2 секунды

# Запускаем эмуляцию в отдельном потоке
threading.Thread(target=simulate_drone, daemon=True).start()

# WebSocket: получение позиции дрона
@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected to WebSocket'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)