import json
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=["POST"])
def index():
    try:
        data = json.loads(request.data.decode('utf-8'))
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'message': 'エラーが発生しました'}), 400


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
