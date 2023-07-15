from flask import Flask, request, redirect
from engine import Engine

app = Flask(__name__)
search_input = ""
search_result = []
engine = Engine()


@app.route("/")
def home():
    return {"": "Welcome to backend"}


@app.route("/search", methods=['GET', 'POST'])
def search():
    global search_input, search_result
    if request.method == 'POST':
        request_data = request.get_json()
        search_input = request_data['search']
        search_result = engine.search(search_input)
    return {"search_input": search_input}


@app.route("/result")
def result():
    return {"result": search_result}


if __name__ == "__main__":
    app.run(debug=True)
