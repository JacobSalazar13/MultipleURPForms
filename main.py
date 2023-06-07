from flask import Flask, request, jsonify, render_template, make_response
import requests 
import functools

app = Flask(__name__)

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
        form_data = request.form.to_dict()
        subjects = ['calc_ab', 'calc_bc', 'chemistry', 'english_lang', 'environmental_science', 'euro_history', 'human_geo',
            'macro', 'micro', 'physics1', 'pysch', 'stats', 'usgov', 'ushistory', 'world', 'worksheets']
        for index, subject in enumerate(subjects):
            try:
                form_data['quote_' + subject] = form_data['li{}'.format(index + 1)] * 15
            except:
                pass
        response = requests.post("https://hooks.zapier.com/hooks/catch/6860943/3tpp32p/", json = form_data)
        return render_template("success.html")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
