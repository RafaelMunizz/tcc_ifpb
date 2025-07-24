from bs4 import BeautifulSoup
import requests
import pandas as pd


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

url='https://www.google.com/search?q=drogon&num=10'
html = requests.get(url,headers=headers)

print(html.status_code)

soup = BeautifulSoup(html.text, 'html.parser')

allData = soup.find_all("div",{"class":"g"})

g=0
Data = [ ]
l={}
for i in range(0,len(allData)):
                    link = allData[i].find('a').get('href')

                    if(link is not None):
                        if(link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1):
                            g=g+1
                            l["link"]=link
                            try:
                                l["title"]=allData[i].find('h3',{"class":"DKV0Md"}).text
                            except:
                                l["title"]=None

                            try:
                                l["description"]=allData[i].find("div",{"class":"VwiC3b"}).text
                            except:
                                l["description"]=None

                            l["position"]=g

                            Data.append(l)

                            l={}

                        else:
                            continue

                    else:
                        continue


print(Data)
df = pd.DataFrame(Data)
df.to_csv('google.csv', index=False, encoding='utf-8')