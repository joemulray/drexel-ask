#!/usr/bin/env python

from flask import Flask, render_template, jsonify
from flask_ask import Ask, statement, question , session, convert_errors
from afg import Supervisor


app =Flask("Drexel Ask")
ask = Ask(app, "/")
supervise = Supervisor("scenario.yml")


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
	app.run(debug=True)

