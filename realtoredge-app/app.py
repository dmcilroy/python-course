from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
from realtordata import get_realtor_data

app = Flask(__name__)

Bootstrap(app)

@app.route("/")
def hello():
    return render_template("index-simple.html")

@app.route("/about") 
def about():
    return render_template('about.html')

@app.route("/data")
def data():
    my_data = get_realtor_data()
    return jsonify(my_data)

if __name__ == '__main__':
     app.run(debug=True)