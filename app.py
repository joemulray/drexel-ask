#!/usr/bin/env python

from configparser import ConfigParser, DuplicateOptionError, Error
from flask import Flask, render_template, jsonify
from flask_ask import Ask, statement, question , session, convert_errors
from datetime import datetime
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
user = None
username = None
password = None



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
		try:
			self.authkey = str(response.json()['AuthKey'])
		except KeyError as error:
			app.logger.error("Could not obtain key from D1M")
			exit(1)

		time.ctime()
		timestring = time.strftime('%Y%m%d%H%M%S') + '+00'
		furl = host + '/Student/CourseSections' + timestring
		hashed = hmac.new(self.authkey, furl, sha1)
		self.token = self.username + ':' + hashed.digest().encode("base64").rstrip('\n') + ':' + timestring


	def __request_class_info(self):
		if self.token:
			repsonse = requests.get(host + '/Student/CourseSections', headers={'Authorization':self.token})
			self.courses = json.dumps(repsonse.json())


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
def welcome():
	app.logger.debug('welcome')
	return question(render_template("welcome_message"))


@ask.intent("ClassIntent")
@supervise.guide
def promptclassinfo():
	app.logger.debug('promptclassinfo')
	pass


@ask.intent("ClassIntent")
@supervise.guide
def promptnextclass():
	app.logger.debug('promptnextclass')
	pass

@ask.intent("ClassIntent")
@supervise.guide
def promptdistance():
	app.logger.debug("promptdistance")



@ask.intent("SemesterIntent")
@supervise.guide
def promptsemester():
	app.logger.debug("promptsemester")
	pass


@ask.intent("AMAZON.YesIntent")
@supervise.guide
def calculate_rundown():
	app.logger("calculate_rundown")

	if session.attributes["Refresh"]:
		global user
		user = Student(username, password)
		session.attributes["Refresh"] = False
		return statement(render_template("refreshed_message"))

	if self.courses:
		for course in self.courses:
			pass

	else:
		#no classes found
		session.attributes["Refresh"] = True
		return question(render_template("noclasses_message"))



@ask.intent("ClassIntent")
@supervise.guide
def chooseclass():
	app.logger.debug("chooseclass")
	pass

@ask.intent("SemesterIntent")
@supervise.guide
def choosesemester():
	app.logger.debug("choosesemester")
	pass


def global_init():
	global username, password, user
	config.read(userconfig)
	for key in config["Drexel User"]:
		username = key
		password = config["Drexel User"][key]

if __name__ == '__main__':
	global_init()
	if username is not None and password is not None:
		user = Student(username, password)
		app.run(debug=True)

