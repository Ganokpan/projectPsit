from flask import Flask , render_template

app = Flask('Test')


@app.route('/')
def home():
    return render_template('index.html')

app.run()
