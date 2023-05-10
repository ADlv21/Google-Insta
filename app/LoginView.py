from app import app

from flask import render_template, request, redirect, make_response
from google.cloud import datastore
from google.cloud import storage
from app import local_constants, customutils
import google.oauth2.id_token
from google.auth.transport import requests
import time

# get access to the datastore client so we can add and store data in the datastore
datastore_client = datastore.Client()

# get access to a request adapter for firebase as we will need this to authenticate users
firebase_request_adapter = requests.Request()


def create_user(email, user_id, name):
    entity = datastore.Entity(key=datastore_client.key('UserProfile', user_id))
    entity.update(
        {
            'userId': user_id,
            'email': email,
            'name': name
        }
    )
    datastore_client.put(entity)


@app.route('/')
def redirectLogin():
    return redirect('/login')


@app.route('/login')
def root():
    # query firebase for the request token and set other variables to none for now
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    userId = ''
    email = ''
    name = ''
    resp = None

    # if we have an ID token then verify it against firebase if it doesn't check out then
    # log the error message that is returned
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            userId = claims['user_id']
            email = claims['email']
            name = claims.get('name', '')

            create_user(user_id=claims['user_id'], email=claims['email'], name=claims.get('name', ''))

        except ValueError as exc:
            error_message = str(exc)

    resp = make_response(render_template('index.html', user_data=claims, error_message=error_message))
    resp.set_cookie('userId', userId)
    resp.set_cookie('email', email)
    resp.set_cookie('name', name)

    return resp
