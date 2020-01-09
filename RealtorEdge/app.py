from flask import Flask
app = Flask(__name__)

@app.route('/')
def My_Home_Page():
    return 'My Home Page'
    
@app.route('/about')
def about_me():
    return 'This page is About Me'
