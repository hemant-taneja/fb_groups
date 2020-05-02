import openpyxl
import bs4
import requests
import pandas


wb = openpyxl.load_workbook('groups.xlsm')
ws = wb['Sheet8']
urls = []
for i in range(2, 51):
    urls.append((ws.cell(row=i, column=1).hyperlink.target))

members = []
for i in range(len(urls)):
    a = "https://m"+urls[i][11:]
    data = requests.get(a)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    public = soup.find("h1").next_element.next_element.next_element.getText()
    member = soup.findAll("span", {"id": "u_0_1"})
    print(member)
    if (member) == []:
        member.append("null")
    else:
        for m in member:
            if m != None:
                members.append(m.text)
            else:
                members.append(0)
print(len(members))

df = pandas.DataFrame(data={"members": members})
df.to_csv("./file.csv", sep=',', index=False)
