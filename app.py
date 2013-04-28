#!/usr/bin/env python
# -*- encoding:utf-8 -*-

"""from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
"""

import os
from flask import Flask, render_template, url_for, redirect, \
        session, request, flash, jsonify
from twython import Twython
#from pprint import pprint
#from json import dump

app_key='lEB2S7yylnjyg9eSpDRQ'
app_secret='rradOOyNFm9T1d9Dq8rKTbN5TrYp4HHoRFEu5ftkAs'
callback_url='http://127.0.0.1:5000/get_callback'

DEBUG = True
SECRET_KEY = '\x9b7\xeb;x\xb5\x8e\xed/\x88\x9e\x07W\xb1/\xc5)\xaaG#\x81\x99w\xe7'


# set the secret key.  keep this really secret:
#application.secret_key = '\x9b7\xeb;x\xb5\x8e\xed/\x88\x9e\x07W\xb1/\xc5)\xaaG#\x81\x99w\xe7'
"""
t = Twython(app_key='lEB2S7yylnjyg9eSpDRQ',
            app_secret='rradOOyNFm9T1d9Dq8rKTbN5TrYp4HHoRFEu5ftkAs',
            callback_url='http://127.0.0.1:5000/')
"""

application = Flask(__name__)
#application.config['DEBUG'] = True
application.config.from_object(__name__)


@application.route('/')
def index():
    screen_name = session.get('screen_name')
    if screen_name != None:
        token = session.get('request_token')
        oauth_token = token[0]
        oauth_token_secret = token[1]
        entry = {}
        t = Twython(app_key='lEB2S7yylnjyg9eSpDRQ',
            app_secret='rradOOyNFm9T1d9Dq8rKTbN5TrYp4HHoRFEu5ftkAs',
            oauth_token=oauth_token,
            oauth_token_secret=oauth_token_secret)
        #return jsonify(**t.getHomeTimeline())
        #return jsonify([t.getHomeTimeline()])

        tweets = t.getHomeTimeline()
        #return dump(t.getHomeTimeline())
        return render_template('index.html', tweets=tweets)

    else:
        return render_template('index.html')

@application.route('/login')
def login():

    #t = Twython(app_key,app_secret,callback_url)

    t = Twython(app_key=app_key,
            app_secret=app_secret,
            callback_url=callback_url)
    auth_props = t.get_authentication_tokens()
    session['request_token'] = (auth_props['oauth_token'], auth_props['oauth_token_secret'])
    #oauth_token = auth_props['oauth_token']
    #oauth_token_secret = auth_props['oauth_token_secret']
    return redirect(auth_props['auth_url'])
    #return oauth_token + ":" + oauth_token_secret

@application.route('/get_callback')
def get_callback():
    verifier = request.args.get('oauth_verifier', '')
    token = session.get('request_token')
    del session['request_token']
    
    #auth = Twython(app_key,app_secret)
    oauth_token = token[0]
    oauth_token_secret = token[1]
    t = Twython(app_key=app_key,
            app_secret=app_secret,
            oauth_token=oauth_token,
            oauth_token_secret=oauth_token_secret)
    #print t.getHomeTimeline()
    try:
        auth_tokens = t.get_authorized_tokens(verifier)
    except:
        flash('Error! Failed to get access token.')

    session['logged_in'] = True
    session['screen_name'] = auth_tokens['screen_name']
    session['request_token'] = (auth_tokens['oauth_token'], auth_tokens['oauth_token_secret'])

    flash(auth_tokens['screen_name'] + ' were signed in')

    #return jsonify(**auth_tokens)
    return redirect(url_for('index'))


@application.route('/logout')
def logout():
    session.pop('screen_name', None)
    session.pop('logged_in', None)
    session.pop('request_token', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)
