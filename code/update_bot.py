from bs4 import BeautifulSoup
import requests
import schedule
import telepot
import time
import os
import ast
from pprint import pprint
import pdb
import json

known = ''
known_versions = {}

def get_current(tp):
    global known_versions
    with open('known_versions.json','r') as verfile:
        known_versions = json.load(verfile)
        known = str(known_versions[tp][-1])

def append_known(tp, version):
    global known_versions

    if version not in known_versions[tp]:
        known_versions[tp].append(unicode(version))
        with open('known_versions.json','w') as verfile:
            verlist = json.dumps(known_versions, indent=4, sort_keys=True)
            verfile.write(verlist)
    else:
        print("Version already known.")

def send_bot_msg(message):
    user_id = os.environ['USER_ID']
    bot = telepot.Bot(os.environ['BOT_TOKEN'])
    bot.sendMessage(user_id, message)

def find_g870a_update():
    get_current('g870a')

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
    version = xml[verpos:verpos+13]

    # Previous version
    prev = xml.rfind("Previous versions required:",0)
    prev_ver = xml.find("G870A",prev+27)
    previous_version = xml[prev_ver:prev_ver+13]

    url =  'https://xdmd.sl.attcompute.com/agents/42998/1488/SS-' + previous_version + '-to-' + version[7:] + '-UP'
    message = 'A new update for the G870A is released:\n' + version + '\nDownload here: ' + url

    if version != known:
        send_bot_msg(message)
        print(url)
        append_known('g870a', version)

def find_qbt_update():
    get_current('qbt')

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
        append_known('qbt', version)

schedule.every().day.at("12:00").do(find_g870a_update)
schedule.every().day.at("12:00").do(find_qbt_update)

find_g870a_update()
find_qbt_update()

try:
    while True:
        schedule.run_pending()

        time.sleep(30)

except KeyboardInterrupt:
    print "Terminated!"
