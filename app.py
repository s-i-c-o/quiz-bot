import os
import json
import datetime

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  usrmg = data['text'].lower()
  now = datetime.datetime.today()
  day = now.weekday()
  tomorrow = now.weekday()
  if day + 1 > 6:
    tomorrow = 0
  else:
    tomorrow = day + 1
  
  msg = ''
	
  if data['name'] != 'Principles Quiz Bot':
    if "quiz" in usrmg and "exam" in usrmg:
      msg = '{}, please specify if you are talking about a quiz or exam.'.format(data['name'])
    elif "quiz" in usrmg:
      if "today" in usrmg and day == 0:
        msg = '{}, there are no more quizzes. Just the final.'.format(data['name'])
      elif "today" in usrmg and day != 0:
        msg = '{}, there are no more quizzes. Just the final.'.format(data['name'])
      elif "tomorrow" in usrmg:
        if tomorrow == 0:
          msg = '{}, there are no more quizzes. Just the final.'.format(data['name'])
        else:
          msg = '{}, there are no more quizzes. Just the final.'.format(data['name'])
      elif "when" in usrmg or "what day" in usrmg:
        msg = '{}, there are no more quizzes. Just the final.'.format(data['name'])
      elif "quiz about" in usrmg or "cover" in usrmg or "over" in usrmg or "about" in usrmsg:
        msg = '{}, there are no more quizzes. Just the final.'.format(data['name'])
    elif "final" in usrmg or "exam" in usrmg:
      if "when" in usrmg:
        msg = '{}, the final exam is on Monday, May 6th at 4:30PM.'.format(data['name'])
      if "notes" in usrmg:
        msg = '{}, you get 3 pages (front and back) of notes for the final.'.format(data['name'])
      if "about" in usermg:
        msg = '{}, the final will be 80 percent past quizzes and 20 percent questions about homeworks and general programming language questions.'.format(data['name'])
  if len(msg) != 0:
      send_message(msg)

  return "ok", 200


def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()