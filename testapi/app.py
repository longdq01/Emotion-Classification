from flask import Flask, jsonify, request
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)


@app.route('/')
def hello():
    return 'hello'


@app.route('/post', methods=["POST"])
def post():
    if request.method == 'POST':
        try:
            data = request.get_json()
            id = data['id']
            name = data['name']
            print(id, name)
            return jsonify({'id': id, 'name': name})
        except Exception as e:
            print(e)
            return jsonify({'Status': 'Failed', 'msg': str(e)})


if __name__ == '__main__':
    app.run()
