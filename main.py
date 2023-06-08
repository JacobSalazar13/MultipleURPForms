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

        # dictionary mapping for the services and product_ids
        service_id_mapping = {
            "calc_ab": {"Service": "AP Calculus AB Ultimate Review Packet", "ID": 36},
            "calc_bc": {"Service": "AP Calculus BC Ultimate Review Packet", "ID": 29},
            "chemistry": {"Service": "AP Chemistry Ultimate Review Packet", "ID": 24},
            "english_lang": {"Service": "AP English Language Ultimate Review Packet", "ID": 32},
            "environmental_science": {"Service": "AP Environmental Science Ultimate Review Packet", "ID": 25},
            "euro_history": {"Service": "AP European History Ultimate Review Packet", "ID": 26},
            "human_geo": {"Service": "AP Human Geography Ultimate Review Packet", "ID": 33},
            "macro": {"Service": "AP Macroeconomics Ultimate Review Packet", "ID": 27},
            "micro": {"Service": "AP Microeconomics Ultimate Review Packet", "ID": 28},
            "physics1": {"Service": "AP Physics 1 Ultimate Review Packet", "ID": 38},
            "pysch": {"Service": "AP Psychology Ultimate Review Packet", "ID": 31},
            "stats": {"Service": "AP Statistics Ultimate Review Packet", "ID": 39},
            "usgov": {"Service": "AP U.S. Government and Politics Ultimate Review Packet", "ID": 40},
            "ushistory": {"Service": "AP U.S. History Ultimate Review Packet", "ID": 34},
            "world": {"Service": "AP World History Ultimate Review Packet", "ID": 42}
        }

        services = []
        product_ids = []

        try:
            for index, subject in enumerate(subjects):
                quantity = 'li{}'.format(index + 2)
                if quantity in form_data and int(form_data[quantity]) > 0:
                    services.append(service_id_mapping[subject]["Service"])
                    product_ids.append(service_id_mapping[subject]["ID"])
                    form_data['quantity_{}'.format(subject)] = int(form_data.pop(quantity)) # renaming the key

                form_data['quote_' + subject] = form_data['quantity_{}'.format(subject)] * 15
                form_data[subject] = subject
                log("added quote_{}".format(subject), client)

            # add services and product_ids to form_data
            form_data["services"] = ','.join(services)
            form_data["product_ids"] = ','.join(map(str, product_ids))
            form_data['services_list'] = services
            form_data['product_ids_list'] = product_ids

        except Exception as e:
            print(e)
            log(str(e),client)
            log(str(form_data), client)

        response = requests.post("https://hooks.zapier.com/hooks/catch/6860943/3tpp32p/", json = form_data)

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
