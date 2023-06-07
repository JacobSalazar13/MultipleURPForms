from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('Form.html')
    else:
        form_data = request.form.to_dict()
        return jsonify(form_data), 200