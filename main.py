from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for
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

def extract_emails_and_names(data):
    emails = []
    names = []

    for course_data in data[0].values():
        if any(value != "" for value in course_data.values()):
            if course_data.get('email', '') != "":
                emails.append(course_data['email'])
            if course_data.get('name', '') != "":
                names.append(course_data['name'])

    return emails, names

def log(message, client):
    try:
        logging.warning(message)
        print(message)
    except:
        pass

def validate_data(data):
    if not data:
        return False
    else:
        for dictionary in data:
            for value in dictionary.values():
                # Turn the values of the inner dictionary into a list
                inner_values = list(value.values())
                # Check if all elements are empty or all elements are non-empty
                if not all(v == '' for v in inner_values) and not all(v != '' for v in inner_values):
                    return False
        return True


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
        try:
            db = firestore.Client()
        except:
            pass
        selectedValue = request.form.get("bulk")
        if (
            selectedValue
            == "I am a teacher or school employee and I want to request a free teacher trial"
        ):
            # Redirect to the Google Form
            return redirect("https://forms.gle/vDuq13XEnBLhkf7i6")
        elif selectedValue == "I am a student or parent":
            # Redirect to ultimatereviewpackets.com
            return render_template("student-parent.html")
        try:
            client = google.cloud.logging.Client()
            client.setup_logging()
        except:
            pass
        form_data = request.form.to_dict()
        session_id=generate_session_id(5)
        if 'payment' not in list(form_data.keys()):
            return render_template("Form.html", error = "Please choose a payment method!")
        print(form_data)
        print("got data")
        # process the raw_data to get the format you want
        processed_data = [
            {
                
                "AP Calculus AB": {
                    "quantity": form_data.get('APCalcAB1', None),
                    "name": form_data.get('APCalcAB2', None),
                    "email": form_data.get('APCalcAB3', None)
                },
                "AP Calculus BC": {
                    "quantity": form_data.get('APCalcBC1', None),
                    "name": form_data.get('APCalcBC2', None),
                    "email": form_data.get('APCalcBC3', None)
                },
                "AP Chemistry": {
                    "quantity": form_data.get('APChem1', None),
                    "name": form_data.get('APChem2', None),
                    "email": form_data.get('APChem3', None)
                },
                "AP English Language and Composition": {
                    "quantity": form_data.get('APLangComp1', None),
                    "name": form_data.get('APLangComp2', None),
                    "email": form_data.get('APLangComp3', None)
                },
                "AP Environmental Science": {
                    "quantity": form_data.get('APEnvSci1', None),
                    "name": form_data.get('APEnvSci2', None),
                    "email": form_data.get('APEnvSci3', None)
                },
                "AP European History": {
                    "quantity": form_data.get('APEuroHist1', None),
                    "name": form_data.get('APEuroHist2', None),
                    "email": form_data.get('APEuroHist3', None)
                },
                "AP Human Geography": {
                    "quantity": form_data.get('APHumGeo1', None),
                    "name": form_data.get('APHumGeo2', None),
                    "email": form_data.get('APHumGeo3', None)
                },
                "AP Macroeconomics": {
                    "quantity": form_data.get('APMacro1', None),
                    "name": form_data.get('APMacro2', None),
                    "email": form_data.get('APMacro3', None)
                },
                "AP Microeconomics": {
                    "quantity": form_data.get('APMicro1', None),
                    "name": form_data.get('APMicro2', None),
                    "email": form_data.get('APMicro3', None)
                },
                "AP Psychology": {
                    "quantity": form_data.get('APPsych1', None),
                    "name": form_data.get('APPsych2', None),
                    "email": form_data.get('APPsych3', None)
                },
                "AP US Government and Politics": {
                    "quantity": form_data.get('APGovPol1', None),
                    "name": form_data.get('APGovPol2', None),
                    "email": form_data.get('APGovPol3', None)
                },
                "AP US History": {
                    "quantity": form_data.get('APUSH1', None),
                    "name": form_data.get('APUSH2', None),
                    "email": form_data.get('APUSH3', None)
                },
                "AP World History": {
                    "quantity": form_data.get('APWorldHist1', None),
                    "name": form_data.get('APWorldHist2', None),
                    "email": form_data.get('APWorldHist3', None)
                },
            }
        ]
        form_data["processed_data"] = processed_data
        print(form_data)  # Prints the processed data to the console

        try:
            quantities_list = [int(v.get('quantity')) for v in list(processed_data[0].values()) if len(v.get('quantity')) > 0]
        except Exception as e:
            log("Didn't submit a number in the orders textbox")
            return render_template("error.html", error = e)
        if len(quantities_list) == 0:
            return render_template("Form.html", error = "Please place an order!")
        for quantity in quantities_list:
            if quantity < 10:
                return render_template("Form.html", error = "Unfortunately, you cannot order an Ultimate Review Packet for less than 10 licenses. Please increase your order size.")
            else:
                pass
        services_list  = [k + " " + "Ultimate Review Packet" for k,v in list(processed_data[0].items()) if len(v.get('quantity')) > 0]
        amounts_list = [15*int(quantity) for quantity in quantities_list]
        form_data['quantities_list'] = quantities_list
        form_data["services_list"] = services_list
        form_data['amounts_list'] = amounts_list
        print(form_data)
        thinkificCodes = []
        workSheetCodes = []
        sampleCodes = []
        product_ids_list = []
        services = [k  for k,v in list(processed_data[0].items()) if len(v.get('quantity')) > 0] 
        for service in services:
            try:
                value = service_id_mapping.get(service, None)
                thinkificCode = value.get('ThinkificCode', None)
                thinkificCodes.append(thinkificCode)
                workSheetCode = value.get('WorksheetCodes', None)
                workSheetCodes.append(workSheetCode)
                sampleCode = value.get('SampleCodes', None)
                sampleCodes.append(sampleCode)
                product_id = value.get('ID')
                product_ids_list.append(product_id)
            except:
                pass

        form_data['thinkificCodes'] = thinkificCodes
        form_data['workSheetCodes'] = workSheetCodes
        form_data['sampleCodes'] = sampleCodes
        form_data['product_ids_list'] = product_ids_list
        form_data['ID'] = session_id
        try:
            form_data["timestamp"] = time.time()
            file = request.files['purchaseOrderFile']
            if file.filename == '':
                flash('No selected fil')
                return redirect(request.url)
                #log('No selected fil', client)
                pass
            else:
                filename = secure_filename(file.filename)
                file_url = upload_blob(
                    session_id, filename, file
                    )
                form_data['purchaseOrderURL'] = file_url
        except:
            print("No file")
            #log("no file logged", client)
        if validate_data(form_data['processed_data']):
        # Continue your program...
            pass
        else:
            return render_template("Form.html", error="Please make sure to fill out all required fields including Quantity, Teacher Name Who Will Be Using The Resources and Email")
        try:
            doc_ref = db.collection(u'Sessions').document(session_id)
            doc_ref.set(form_data)
        except:
            pass
        try:
            emails_list = [str(v.get('email')) for v in list(processed_data[0].values()) if len(v.get('email')) > 0]
            names_list = [str(v.get('name')) for v in list(processed_data[0].values()) if len(v.get('name')) > 0]
            form_data['emails_list'] = emails_list
            form_data['names_list'] = names_list
            print(form_data)
            response = requests.post(
            "https://hooks.zapier.com/hooks/catch/6860943/3tpp32p/", json=form_data
        )
        except Exception as e:
            print("error" + str(e))
        return redirect(url_for("route_success", order_id=session_id))

@app.route("/success/<order_id>")
def route_success(order_id):
    return render_template("success.html", order_id=order_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
