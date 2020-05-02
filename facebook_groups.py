import pandas
import http.cookiejar
import urllib.request
import requests
import bs4
import random
import re
import time


# Store the cookies and create an opener that will hold them
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Add our headers
opener.addheaders = [('User-agent', 'dfdf')]

# Install our opener (note that this changes the global opener to the one
# we just made, but you can also just call opener.open() if you want)
urllib.request.install_opener(opener)

# The action/ target from the form
authentication_url = 'https://m.facebook.com/login.php'

# Input parameters we are going to send
payload = {
    'email': 'email',
    'pass': 'password'
}

# Use urllib to encode the payload
data = urllib.parse.urlencode(payload).encode("utf-8")

# Build our Request object (supplying 'data' makes it a POST)
req = urllib.request.Request(authentication_url, data)
regex = r"/groups/"

# Make the request and read the response
resp = urllib.request.urlopen(req)
contents = resp.read()
# print(contents)
q = "services"
url = "https://m.facebook.com/search/groups/?q="+q
data = requests.get(url, cookies=cj)
soup = bs4.BeautifulSoup(data.text, 'html.parser')
# print(soup.prettify())
# z = 0
# print(soup.find("div", {"id": "objects_container"})

see_more = []
group_urls = []

count = 0
while len(group_urls) <= 20:
    time.sleep(random.randint(1, 3))
    links = soup.find("div", {"id": "objects_container"}).findAll(
        "a", {"href": re.compile("/groups/")})
    for link in links:
        group_urls.append(link['href'])
    group_urls = list(set(group_urls))
    r = re.compile("https://m.facebook.com/search/groups/")
    newlist = list(filter(r.match, group_urls))
    if len(newlist) == 0:
        break
    group_urls.remove(newlist[0])
    see_more.append(newlist[0])
    data = requests.get(see_more[count], cookies=cj)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    links = soup.find("div", {"id": "objects_container"}).findAll(
        "a", {"href": re.compile("/groups/")})
    count += 1

public_groups = []
members = []
titles = []
for i in group_urls:
    data = requests.get(
        "https://m.facebook.com/"+i, cookies=cj)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    public = soup.find(
        "h1").next_element.next_element.next_element.getText()
    if public == "Public group":
        print(True)
        public_groups.append(i)
        print(i)
        member = soup.findAll("span", {"id": "u_0_1"})
        print(member)
        if len(member) == 0:
            member.append(0)
        else:
            for m in member:
                if m != None:
                    members.append(m.text)
                else:
                    members.append(0)
        title = soup.find("h1").getText()
        titles.append(title)


df = pandas.DataFrame(
    data={"col1": group_urls, "col2": titles, "col3": members})
df.to_csv("./file.csv", sep=',', index=False)
