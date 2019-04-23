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
  now = datetime.datetime.today()
  day = now.weekday()
  msg = ''
  # We don't want to reply to ourselves!
	
  if data['name'] != 'Quiz Bot':
    if "quiz" in data['text']:
      if "today" in data['text'] and day == 0:
        msg = '{}, yes. There is a quiz today.'.format(data['name'])
      elif "today" in data['text'] and day != 0:
        msg = '{}, no. The next quiz is on Monday the 29th.'.format(data['name'])
      elif "tomorrow" in data['text']:
        if day + 1 == 0:
          msg = '{}, yes. There is a quiz tomorrow.'.format(data['name'])
        else:
          msg = '{}, no. There is NOT a quiz tomorrow.'.format(data['name'])
      elif "when" in data['text'] or "what day" in data['text']:
        msg = '{}, the next quiz is on Monday the 29th.'.format(data['name'])
      elif "quiz about" in data['text'] or "cover" in data['text'] or "over" in data['text']:
        msg = '{}, I do not know what the next quiz is over because my creator had a dentist appointment.'.format(data['name'])
    if "final" in data['text'] or "exam" in data['text']:
      if "when" in data['text']:
        msg = '{}, the final exam is on Monday, May 6th at 4:30PM.'.format(data['name'])
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