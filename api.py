from flask import Flask, jsonify

app = Flask(__name__)

# Define API endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    # Dummy data for demonstration
    data = {'message': 'Hello from Python server!'}
    return jsonify(data)
def index():
    return '<h1>Hello!</h1>'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the server on port 5000
