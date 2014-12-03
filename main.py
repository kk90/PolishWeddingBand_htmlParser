__author__ = 'krzysiek'
from BeautifulSoup import BeautifulSoup
import urllib2
import thread
bands=[]
i=0
threadsCount=5
class Band:
    name=""
    telephone=""
    video=""
    address=""
    href=""


# tasklist=0
# def threadManagment(task, args):
#     global tasklist
#     while(tasklist>threadsCount):
#         pass
#     tasklist=tasklist+1
#     thread.start_new_thread(task,args)
#     print "added"

def getUrisOfBand(html):
    urisstrings=[]
    soup = BeautifulSoup(html)
    articles= soup.findAll('article',)
    for art in articles:
        uris= art.findAll('a', href=True)
        urisstrings.append(uris[0]['href'])
        #print uris[0]['href']
    return urisstrings

def parseOneBand(uri):
    try:
        band =Band()
        f = urllib2.urlopen(uri)
        html = f.read()
        soup = BeautifulSoup(html)
        name=soup.find('h1',itemprop="name")
        if not name is None:
            band.name=name.string
        telephone=soup.find('span',itemprop="telephone")
        if not telephone is None:
            band.telephone=telephone.string
        video=soup.find('object',type="application/x-shockwave-flash")
        if not video is None:
                band.video=video["data"]
        address=soup.find('div',itemprop="address").getText()
        if not address is None:
            band.address=address
        band.href=uri
        bands.append(band)

        v=soup.findAll('meta',itemprop="reviewRating")
        if not v is None:
            for vi in v:
                if not vi["content"]=="5":
                    print band.href
                    print vi["content"]
    except:
        pass
    print "OK"


def getBandData(list):
    for uri in list:
        #parseOneBand(uri)
        thread.start_new_thread(parseOneBand,(uri,))



def getWojewodzctwo(baseURL,range_):
    for x in range(1,range_):
        f = urllib2.urlopen(baseURL+"/"+str(x))
        html = f.read()
        list =getUrisOfBand(html)
        thread.start_new_thread(getBandData,(list,))
        #getBandData(list)


def htmlResult():
    page="<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Bands</title></head><body>"
    i=0
    for bnd in bands:

        i+=1
        page+="<h1>"+str(i)+" "+bnd.name+"</h1>"
        page+="<br/><a href='"+bnd.href+"'a>klik</a> "
        if not bnd.telephone is None:
            page+="<br/>"+bnd.telephone
        page+="<br/>"+bnd.address
        if not bnd.video=="":
            page+="<br/><a href='"+bnd.video+"'a>VIDEO</a> "
        page+="<br/><br/></br>"
    page+="</body></html>"
    text_file = open("bands.html", "w")
    text_file.write(page.encode('UTF-8', 'ignore'))
    text_file.close()


all = urllib2.urlopen('http://www.zespoly-weselne.pl/')
html = all.read()
soup = BeautifulSoup(html)
v=soup.find('ul',{"class":"menu"})
li=v.findAll("a",)
for a in li:
    baseUrl=a["href"]
    f = urllib2.urlopen(baseUrl)
    html = f.read()
    soup = BeautifulSoup(html)
    num=soup.find("nav",{"class":"pagination"})
    num= num.findAll('a',)
    count=len(num)+2
    print count
    print baseUrl
    #getWojewodzctwo(baseUrl,count)
    thread.start_new_thread(getWojewodzctwo,(baseUrl,count,))



htmlResult()


