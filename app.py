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

  # We don't want to reply to ourselves!
	
  if data['name'] != 'Test Quiz Bot':
    if "quiz" in data['text']:
      if "today" in data['text'] and day == 0:
        msg = '{}, yes. There is a quiz today.'.format(data['name'])
      elif "today" in data['text'] and day != 0:
        msg = '{}, no. The next quiz is on Monday the 29th.'.format(data['name'])
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