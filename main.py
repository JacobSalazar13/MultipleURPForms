from flask import Flask, request, jsonify, render_template, make_response
import requests 
import functools
import google.cloud.logging
import logging

app = Flask(__name__)

def log(message, client):
    logging.warning(message)
    print(message)

def nocache(view):
    @functools.wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return no_cache

@app.route('/', methods = ['GET', 'POST'])
@nocache
def form():
    if request.method == 'GET':
        return render_template('Form.html')
    else:
        client = google.cloud.logging.Client()
        client.setup_logging()
        form_data = request.form.to_dict()
        subjects = ['calc_ab', 'calc_bc', 'chemistry', 'english_lang', 'environmental_science', 'euro_history', 'human_geo',
            'macro', 'micro', 'physics1', 'pysch', 'stats', 'usgov', 'ushistory', 'world', 'worksheets']
        try:
            for index, subject in enumerate(subjects):
                form_data['quote_' + subject] = int(form_data['li{}'.format(index + 2)]) * 15
                form_data['{}'.format(subject)] = subject
                log("added quote_{}".format(subject), client)
        except Exception as e:
            print(e)
            log(str(e),client)
            log(str(form_data), client)
        response = requests.post("https://hooks.zapier.com/hooks/catch/6860943/3tpp32p/", json = form_data)
        return render_template("success.html")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
