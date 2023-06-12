from flask import Flask, request, jsonify, render_template, make_response, redirect
import requests
import functools
import google.cloud.logging
import logging
import time
from servicemapping import service_id_mapping
from werkzeug.utils import secure_filename
from storage import upload_blob, generate_session_id
from google.cloud import firestore

app = Flask(__name__)


def log(message, client):
    try:
        logging.warning(message)
        print(message)
    except:
        pass


def nocache(view):
    @functools.wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return no_cache


@app.route("/", methods=["GET", "POST"])
@nocache
def form():
    if request.method == "GET":
        return render_template("Form.html")
    else:
        db = firestore.Client()
        selectedValue = request.form.get("bulk")
        if (
            selectedValue
            == "I am a teacher or school employee and I want to request a free teacher trial"
        ):
            # Redirect to the Google Form
            return redirect("https://forms.gle/vDuq13XEnBLhkf7i6")
        elif selectedValue == "I am a student or parent":
            # Redirect to ultimatereviewpackets.com
            return redirect("https://www.ultimatereviewpacket.com/")
        try:
            client = google.cloud.logging.Client()
            client.setup_logging()
        except:
            pass
        form_data = request.form.to_dict()

        subjects = [
            "calc_ab",
            "calc_bc",
            "chemistry",
            "english_lang",
            "environmental_science",
            "euro_history",
            "human_geo",
            "macro",
            "micro",
            "physics1",
            "pysch",
            "stats",
            "usgov",
            "ushistory",
            "world",
            "worksheets",
        ]

        # dictionary mapping for the services and product_ids

        services = []
        product_ids = []
        amounts = []
        quantities = []
        list_of_subjects = []
        sampleCodes = []
        thinkificCodes = []
        worksheetCodes = []

        for index, subject in enumerate(subjects):
            quantity = "li{}".format(index + 2)
            try:
                adding = {}
                form_data["quantity_{}".format(subject)] = int(
                    form_data.get(f"{quantity}")
                )  # renaming the key
                form_data["quote_" + subject] = (
                    form_data["quantity_{}".format(subject)] * 15
                )
                form_data[subject] = subject

                try:
                    log("added quote_{}".format(subject), client)
                except:
                    pass
                service = service_id_mapping.get("{}".format(subject)).get("Service")
                services.append(service)
                try:
                    log("added {}".format(service), client)
                except:
                    pass
                try:
                    fullname = form_data["full_name{}".format(index + 2)]
                    email = form_data["email{}".format(index + 2)]
                    adding["{}".format(service)] = {
                        "quantity": quantity,
                        "email": email,
                        "fullname": fullname,
                    }
                    list_of_subjects.append(adding)
                except Exception as e:
                    print(e)
                product = service_id_mapping.get("{}".format(subject)).get("ID")
                product_ids.append(product)
                thinkificCode = service_id_mapping.get("{}".format(subject)).get(
                    "ThinkificCode"
                )
                thinkificCodes.append(thinkificCode)
                worksheetCode = service_id_mapping.get("{}".format(subject)).get(
                    "WorksheetCodes"
                )
                worksheetCodes.append(worksheetCode)
                sampleCode = service_id_mapping.get("{}".format(subject)).get(
                    "SampleCodes"
                )
                sampleCodes.append(sampleCode)
                quantity = form_data["quantity_{}".format(subject)]
                quantities.append(quantity)
                amount = form_data["quote_" + subject]
                amounts.append(amount)
                try:
                    log("added {}".format(product), client)
                except:
                    pass
            except Exception as e:
                try:
                    log("couldnt get {} - {}".format(subject, str(e)), client)
                except:
                    pass
        # add services and product_ids to form_data
        form_data["services"] = ",".join(services)
        form_data["product_ids"] = ",".join(map(str, product_ids))
        form_data["services_list"] = services
        form_data["product_ids_list"] = product_ids
        form_data["quantities"] = ",".join(map(str, quantities))
        form_data["quantities_list"] = quantities
        form_data["amounts"] = ",".join(map(str, amounts))
        form_data["amounts_list"] = amounts
        form_data["subject_data_list"] = list_of_subjects
        form_data["sampleCodes"] = sampleCodes
        form_data["thinkificCodes"] = thinkificCodes
        form_data["worksheetCode"] = worksheetCodes
        session_id = generate_session_id(7)
        form_data['ID'] = session_id
        try:
            log(str(form_data), client)
        except:
            pass
        try:
            form_data["timestamp"] = time.time()
            log("got timestamp", client)
            try:
                file = request.files['purchaseOrderFile']
                log("got {}".format(str(file.filename)), client)
            except Exception as e:
                log(f"{e}", client)
            if file.filename == '':
                log('No selected file', client)
                pass
            else:
          #      filename = secure_filename(file.filename)
                log(f"{file.filename}", client)
                file_url = upload_blob(
                    session_id, file.filename, file
                    )
                log(f"{file_url}", client)
                form_data['purchaseOrderURL'] = file_url
                log(str(form_data), client)
        except Exception as e: 
            print("No file")
            log("no file logged", client)
            log("{}".format(e), client)
        
        response = requests.post(
            "https://hooks.zapier.com/hooks/catch/6860943/3tpp32p/", json=form_data
        )
       # time.sleep(20)
        doc_ref = db.collection(u'Sessions').document(session_id)
        doc_ref.set(form_data)
        print(form_data)
        return redirect(url_for("route_success", order_id=session_id))

@app.route("/success/<order_id>")
def route_success(order_id):
    return render_template("success.html", order_id=order_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
