from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime as dt
import sys


def attend(url):
  reply="Getting infomation at "+str(dt.now().strftime("%Y/%m/%d %H:%M:%S"))+'\n'
  if re.compile('https:\/\/densuke\.biz').search(url)==None:
    return '*error*:伝助のURLではありません．または，"https://desuke.biz"で始めてください'
  # htmlを取得、BeautifulSoupで扱う
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser') # BeautifulSoupの初期化
  
  if r.status_code==404:
    return '*error*:URLが間違っています．404　Not Found'

  page=soup.find("h2")
  pagename=page.string.strip()
  if pagename=='メニュー': #存在しないスケジュールページの場合，伝助はエラーでもステータスコードは200を返す  
    return '*error*：URLが間違っています．存在しないスケジュールのページに飛んでいます' 
  
  reply+='伝助タイトル:'+pagename+'\n'

  # aタグの中から、memberdataに飛ぶものを抽出
  tags = soup.find_all("a", href=re.compile("javascript:memberdata"))
  names=[]
  times=[]
  for tag in tags:
    name=tag.string.strip() #登録者の名前
    timeoriginal=tag.get("title")
    if(timeoriginal==None):
      break
    names.append(name)
    if(timeoriginal==''):
      continue
    time=dt.strptime(timeoriginal, '%m/%d %H:%M')
    times.append(time)

  numofpeople=len(names)
  timessort=sorted(times,reverse=True)
  reply+='回答者数:'+str(numofpeople)+'人，最終更新日時:'+str(timessort[0].strftime("%m/%d %H:%M"))+'\n'

  #ミーティング日時等取得
  events=soup.find_all("td",nowrap=True)
  mtgs=[]
  for event in events[numofpeople:len(events)]:
    mtg=event.string.strip()
    if(mtg==""):
      continue
    mtgs.append(mtg)

  #回答取得
  answers=soup.find_all("div",class_=re.compile("col"))
  anses=[]
  for answer in answers:
    ans=answer.string.strip()
    anses.append(ans)

  numofevents=len(mtgs)
  participants=[]
  for i in range(numofevents):
    participants.append([])
    for j in range(numofpeople):
      if(anses[i*numofpeople+j]=='○'):
        participants[i].append(names[j])

# 表を作成
  for i in range(numofevents):
    shownames=','.join([str(n) for n in participants[i]])
    reply+=mtgs[i]+' | '+str(len(participants[i]))+'人 | '+shownames+'\n'
  return reply

if __name__=='__main__':
  u=input()
  print(attend(u))
