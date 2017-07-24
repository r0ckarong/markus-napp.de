import requests
# from bs4 import BeautifulSoup

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

# Changes
new = xml2.rfind("What's new:",0)
endnew = xml2.rfind('li>',new+11)
news = xml2.find(' ',new+11)
version_changes = xml2[news+1:endnew-2]

print (current_version + ' ' + previous_version + ' ' + version_changes)

url =  "https://xdmd.sl.attcompute.com/agents/42998/1488/SS-" + previous_version + "-to-" + current_version[7:] + "-UP"
print(url)
