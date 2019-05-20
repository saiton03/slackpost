from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

import re
import datetime as dt
from . import densuke


@respond_to(r'^\s*attend')
def mention_fun(message):
  text=message.body['text']
  m=re.search(r"https?:\/\/densuke\.biz\/list\?cd=\S{16}",text)
  if m:
    message.reply("```"+densuke.attend(m.group(0))+"```")
  else:
    message.reply('伝助のスケジュールのurlを正しく入れよう')  


@respond_to(r'wake\s*up|good\s*morning|おはよう|こんばん|こんにち',re.IGNORECASE)
def show_info(message):
  nowtime=dt.datetime.now()
  nowcom=nowtime.hour*100+nowtime.minute
  
  if nowcom>400 and nowcom<1000:
    message.reply('おはよう')
    message.react('sunrise')
  elif nowcom<1800:
    message.reply('こんにちは')
    message.react('sunny')
  else:
    message.reply('こんばんは')
    message.react('night_with_stars')


