from flask import Flask, request, jsonify, render_template
import requests 
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('Form.html')
    else:
        form_data = request.form.to_dict()
        response = requests.post("https://hooks.zapier.com/hooks/catch/6860943/3tpp32p/", json = form_data)
        return jsonify(form_data), 200