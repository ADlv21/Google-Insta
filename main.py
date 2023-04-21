import datetime
from flask import Flask, render_template, request, redirect
from google.cloud import datastore
import google.oauth2.id_token
from google.auth.transport import requests

app = Flask(__name__)

# get access to the datastore client so we can add and store data in the datastore
datastore_client = datastore.Client()

# get access to a request adapter for firebase as we will need this to authenticate users
firebase_request_adapter = requests.Request()


@app.route('/')
def redirectLogin():
    return redirect('/login')


@app.route('/login')
def root():
    # query firebase for the request token and set other variables to none for now
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    # if we have an ID token then verify it against firebase if it doesn't check out then
    # log the error message that is returned
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            error_message = str(exc)

    # render the template with the last times we have
    return render_template('index.html', user_data=claims, error_message=error_message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
