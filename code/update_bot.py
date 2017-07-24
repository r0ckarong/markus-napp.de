from bs4 import BeautifulSoup
import requests
import schedule
import telepot
import time
import os

def send_bot_msg(message):
    user_id = os.environ['USER_ID']
    bot = telepot.Bot(os.environ['BOT_TOKEN'])
    bot.sendMessage(user_id, message)

def find_g870a_update():
    known = 'G870AUCS2DQD1'
    headers = {'Accept': 'application/json'}

    r = requests.get('https://services.att.com/kmservices/v2/contents/KM1126238?app-id=esupport', headers=headers)

    data = r.json()

    xml = data['resultBody']['contentTypeProperties']['currentsoftdetails']
    xml2 = data['resultBody']['contentTypeProperties']['currentsoftupd']

    # soup = BeautifulSoup(xml,'html.parser')
    # print(soup.find_all('span'))

    # Current version
    pos = xml.find("Baseband version:",0)
    verpos = xml.find("G870A",pos+17,pos+57)
    current_version = xml[verpos:verpos+13]

    # Previous version
    prev = xml.rfind("Previous versions required:",0)
    prev_ver = xml.find("G870A",prev+27)
    previous_version = xml[prev_ver:prev_ver+13]

    url =  'https://xdmd.sl.attcompute.com/agents/42998/1488/SS-' + previous_version + '-to-' + current_version[7:] + '-UP'
    message = 'A new update for the G870A is released:\n' + current_version + '\n' + ')\nDownload here: ' + url

    if current_version != known:
        send_bot_msg(message)
        print(url)
        known = current_version

    # print (current_version + ' ' + previous_version + ' ' + version_changes)

def find_qbt_update():
    known = 'v3.3.14'

    html = requests.get('https://www.qbittorrent.org/news.php')
    soup = BeautifulSoup(html.text,'html.parser')
    verstring = soup.p.string

    endpos = verstring.find(' was',0)
    verpos = verstring.find('3', 0)
    version = str(verstring[verpos-1:endpos])
    url = 'https://sourceforge.net/projects/qbittorrent/files/qbittorrent/qbittorrent-' + version[1:] + '/qbittorrent-' + version[1:] + '.tar.gz/download'

    message = 'qBittorrent ' + version + ' has been released.\nGo here to download:\n' + url

    if version != known:
        send_bot_msg(message)
        print(url)
        known = version

schedule.every().day.at("12:00").do(find_g870a_update)
schedule.every().day.at("12:00").do(find_qbt_update)

find_g870a_update()
find_qbt_update()

try:
    while True:
        schedule.run_pending()

        time.sleep(30)

except KeyboardInterrupt:
    print "Crashed!"
