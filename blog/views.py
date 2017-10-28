from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def index():
    message = "This is a GET request"

    if request.method == "POST":
        message = "This is a POST request."
    return render_template("index.html", message= message)

@app.route('/about/<something>')
def about(something):
    return 'This is about {0}'.format(something)
