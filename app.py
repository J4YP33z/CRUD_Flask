from flask import Flask

app = Flask(__name__)  # references this file


@app.route("/")
def index():
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)