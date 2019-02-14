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




class Module(object):
	def __init__(self, object):
		 self.coursetitle = object.get("CourseTitle", "")
		 self.coursenumber = object.get("CourseNumber", "")
		 self.section = object.get("Section", "")
		 self.classmeetings = object.get("ClassMeetings", "")
		 self.scheduledescription = object.get("ScheduleDescription", "")
		 self.crn = object.get("Crn", "")


	def __str__(self):
		return "CourseTitle: %s CourseNumber: %s" %(self.coursetitle, self.coursenumber)

class Student():
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.classes = None
		self.authkey = None
		self.token = None
		self.courses = None
		self.term = {}


	def request_token(self):
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


	def request_class_info(self):
		if self.token:
			response = requests.get(host + '/Student/CourseSections', headers={'Authorization':self.token})
			self.rawcourses = json.dumps(response.json())
			self.courses = response.json()
			if response.status_code == 401:
				app.logger.error("Could not obtain token")
				exit(1)

			for course in self.courses:
				if course["Term"]["TermCode"] not in self.term:
					# create new module object
					self.term[course["Term"]["TermCode"]] = [Module(course)]
				else:
					self.term[course["Term"]["TermCode"]].append(Module(course))

			#now that we have the courses loaded up sort the keys
			sorted(self.term.items(), key=lambda mod: mod[1])

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

	currentterm = list(user.term.keys())[0]

	if user.term is not None:
		schedule = user.term[currentterm]

	CourseNames = ""

	for course in schedule:
		CourseNames += course.coursetitle + ", "

	return statement("You are registered for the following classes " +  CourseNames)



def promptnextclass():
	app.logger.debug('promptnextclass')
	pass

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
		user.request_token()
		user.request_class_info()
		app.run(debug=True, use_reloader=False)

