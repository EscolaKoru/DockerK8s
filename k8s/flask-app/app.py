from flask import Flask, jsonify, request, render_template
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import start_http_server, Summary, Counter, Gauge, generate_latest

app = Flask(__name__, template_folder="templates")
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.0')

# Create metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Number of requests processed', ['endpoint'])
IN_PROGRESS = Gauge('inprogress_requests', 'Number of requests in progress', ['endpoint'])

# Exemplo de dados simulados em um banco de dados
db = [
    {"id": 1, "nome": "Chaves", "idade": 40},
    {"id": 2, "nome": "Seu Madruga", "idade": 50},
    {"id": 3, "nome": "Chiquinha", "idade": 30},
    {"id": 4, "nome": "Quico", "idade": 10},
    {"id": 5, "nome": "Dona Florinda", "idade": 45},
    {"id": 6, "nome": "Professor Girafales", "idade": 35},
    {"id": 7, "nome": "Seu Barriga", "idade": 60},
    {"id": 8, "nome": "Don Ramón", "idade": 40}
]

@app.route('/')
@REQUEST_TIME.time()
def home():
    endpoint = '/'
    IN_PROGRESS.labels(endpoint=endpoint).inc()
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    IN_PROGRESS.labels(endpoint=endpoint).dec()
    return render_template('index.html')

# Endpoint para retornar todos os registros
@app.route('/api/data', methods=['GET'])
@REQUEST_TIME.time()
def get_all_data():
    endpoint = '/api/data'
    IN_PROGRESS.labels(endpoint=endpoint).inc()
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    IN_PROGRESS.labels(endpoint=endpoint).dec()
    return jsonify(db)

# Endpoint para retornar um registro específico
@app.route('/api/data/<int:data_id>', methods=['GET'])
@REQUEST_TIME.time()
def get_data(data_id):
    endpoint = f'/api/data/{data_id}'
    IN_PROGRESS.labels(endpoint=endpoint).inc()
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    IN_PROGRESS.labels(endpoint=endpoint).dec()
    data = next((item for item in db if item["id"] == data_id), None)
    if data:
        return jsonify(data)
    else:
        return jsonify({"message": "Data not found"}), 404

# Endpoint para adicionar um novo registro
@app.route('/api/data', methods=['POST'])
@REQUEST_TIME.time()
def add_data():
    endpoint = '/api/data'
    IN_PROGRESS.labels(endpoint=endpoint).inc()
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    IN_PROGRESS.labels(endpoint=endpoint).dec()
    new_data = request.json
    if "id" in new_data and "nome" in new_data and "idade" in new_data:
        db.append(new_data)
        return jsonify({"message": "Data added successfully"}), 201
    else:
        return jsonify({"message": "Incomplete data"}), 400

# Endpoint para atualizar um registro existente
@app.route('/api/data/<int:data_id>', methods=['PUT'])
@REQUEST_TIME.time()
def update_data(data_id):
    endpoint = f'/api/data/{data_id}'
    IN_PROGRESS.labels(endpoint=endpoint).inc()
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    IN_PROGRESS.labels(endpoint=endpoint).dec()
    data = next((item for item in db if item["id"] == data_id), None)
    if data:
        data.update(request.json)
        return jsonify({"message": "Data updated successfully"})
    else:
        return jsonify({"message": "Data not found"}), 404

# Endpoint para deletar um registro
@app.route('/api/data/<int:data_id>', methods=['DELETE'])
@REQUEST_TIME.time()
def delete_data(data_id):
    endpoint = f'/api/data/{data_id}'
    IN_PROGRESS.labels(endpoint=endpoint).inc()
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    IN_PROGRESS.labels(endpoint=endpoint).dec()
    global db
    db = [item for item in db if item["id"] != data_id]
    return jsonify({"message": "Data deleted successfully"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5000)
