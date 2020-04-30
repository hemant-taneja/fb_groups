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
    'email': 'your email',
    'pass': 'your password'
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
keyword = "usa"
url = "https://m.facebook.com/search/groups/?q="+keyword
data = requests.get(url, cookies=cj)
soup = bs4.BeautifulSoup(data.text, 'html.parser')
# print(soup.prettify())
# z = 0
# print(soup.find("div", {"id": "objects_container"})

links = soup.find("div", {"id": "objects_container"}
                  ).findAll("a", {"href": re.compile("/groups/")})
pages = 4
see_more = []
group_urls = []
for i in range(pages):
    time.sleep(random.randint(1, 3))
    for link in links:
        group_urls.append(link['href'])
    group_urls = list(set(group_urls))
    r = re.compile("https://m.facebook.com/search/groups/")
    newlist = list(filter(r.match, group_urls))
    see_more.append(newlist[0])
    # pages = soup.find("div", {"id": "see_more_pages"}).find("a")['href']
    data = requests.get(see_more[i], cookies=cj)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    links = soup.find("div", {"id": "objects_container"}
                      ).findAll("a", {"href": re.compile("/groups/")})

print(group_urls)

# for link in links:
#     group_urls.append(link['href'])
# group_urls.pop()
# group_urls = list(set(group_urls))
# print(group_urls)
