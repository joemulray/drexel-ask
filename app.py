#!/usr/bin/env python

from configparser import ConfigParser, DuplicateOptionError, Error
from flask import Flask, render_template, jsonify
from flask_ask import Ask, statement, question , session, convert_errors
from afg import Supervisor
from hashlib import sha1
import requests
import hmac
import time
import json

app =Flask("Drexel Ask")
ask = Ask(app, "/")
supervise = Supervisor("scenario.yml")

userconfig = "user.ini"
config = ConfigParser()

#drexel one api
host = "https://d1m.drexel.edu/api/v2.0"

class Student():
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.classes = None
		self.authkey = None
		self.token = None
		self.__request_token()
		self.__request_class_info()


	def __request_token(self):
		headerdata = {}
		headerdata["UserId"] = self.username
		headerdata["Password"] = self.password
		headerdata["ForceNewKey"] = "false"
		response = requests.post(host + '/Authentication/', json=headerdata, \
			headers={'X-Http-Method-Override':'PUT'})
		self.authkey = str(response.json()['AuthKey'])

		time.ctime()
		timestring = time.strftime('%Y%m%d%H%M%S') + '+00'
		furl = host + '/Student/CourseSections' + timestring
		hashed = hmac.new(self.authkey, furl, sha1)
		self.token = self.username + ':' + hashed.digest().encode("base64").rstrip('\n') + ':' + timestring


	def __request_class_info(self):
		if self.token:
			repsonse = requests.get(host + '/Student/CourseSections', headers={'Authorization':self.token})
			self.courses = repsonse.json()


@ask.on_session_started
@supervise.start
def new_session():
    app.logger.debug('new session started')


@supervise.stop
def close_user_session():
    app.logger.debug("user session stopped")


@ask.session_ended
def session_ended():
    close_user_session()
    return "", 200

@ask.launch
@supervise.guide
def launched():
	return question(render_template("welcome"))


@ask.intent('ClassIntent')
@supervise.guide
def promptclassinfo():
	pass


@ask.intent('ClassIntent')
@supervise.guide
def promptnextclass():
	pass

@ask.intent('ClassIntent')
@supervise.guide
def promptdistance():
	pass


@ask.intent('SemesterIntent')
@supervise.guide
def promptsemester():
	pass


@ask.intent('ClassIntent')
@supervise.guide
def chooseclass():
	pass

@ask.intent('SemesterIntent')
@supervise.guide
def choosesemester():
	pass

if __name__ == '__main__':

	username = None
	password = None

	config.read(userconfig)
	for key in config["Drexel User"]:
		username = key
		password = config["Drexel User"][key]

	if username is not None and password is not None:

		student = Student(username, password)
		app.run(debug=True)

