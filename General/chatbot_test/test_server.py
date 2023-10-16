from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/salvador")
def salvador():
    return "Hello, Salvador"

# To locally run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=3000)
