from bs4 import BeautifulSoup
import requests
import schedule



known = 'v3.3.14'

html = requests.get('https://www.qbittorrent.org/news.php')
soup = BeautifulSoup(html.text,'html.parser')
verstring = soup.p.string

endpos = verstring.find(' was',0)
verpos = verstring.find(known, 0)
version = str(verstring[verpos:endpos])
dl = 'https://sourceforge.net/projects/qbittorrent/files/qbittorrent/qbittorrent-' + verstring[1:] + '/qbittorrent-' + verstring[1:] + '.tar.gz/download'
print('qBittorrent ' + verstring + ' has been released.\nGo here to download:\n' + dl)
