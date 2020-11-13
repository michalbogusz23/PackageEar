from flask import Flask, render_template, request, make_response
app = Flask(__name__)
app.debug = False

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sender/register', methods=['GET'])
def register_form():
    return render_template("register_form.html")

@app.route('/sender/register', methods=['POST'])
def register():
    return response

@app.route('/sender/login', methods=['GET'])
def login_form():
    return render_template("login_form.html")

@app.route('/sender/login', methods=['POST'])
def login():
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)