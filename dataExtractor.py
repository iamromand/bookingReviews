import os


def clea():
    clear = lambda: os.system('cls')
    clear()

def replaceAphos(stri):
    code = ["'", "&#39;"]
    stri = stri.replace(code[0], code[1])
    return stri


def getInsiderInner(htmlStr, strStart, strEnd):
    start = htmlStr.find(strStart, 0)
    if start != -1:
        htmlStr = htmlStr[start+len(strStart):]
    else:
        return ""
    if strEnd != "":
        return htmlStr[:htmlStr.find(strEnd, 0)]
    else:
        return htmlStr

def getInsider(htmlStr, strStart, strEnd):
    strin = getInsiderInner(htmlStr, strStart, strEnd)
    if len(strin) > 0:
        if strin[0] == "\n":
            strin = strin[1:]
    if len(strin) > 0:
        if strin[len(strin)-1] == "\n":
            strin = strin[:len(strin)-1]
    if len(strin) > 0:
        if strin[0] == "\"":
            strin = strin[1:]
    if len(strin) > 0:
        if strin[len(strin)-1] == "\"":
            strin = strin[:len(strin)-1]
    return strin


def all_occurences(strin, strStart, strEnd):
    initial = 0
    while True:
        initial = strin.find(strStart, initial)
        if initial == -1: return
        yield initial
        initial += len(strStart)
        initial = strin.find(strEnd, initial)
        if initial == -1: return
        yield initial
        initial += len(strEnd)

import sys
sys.path.append("C:/Python34/Lib/site-packages")
import goslate

def checkForNext(index, lang, hotel):
    redo = True
    gs = goslate.Goslate()
    content=open("out.html", encoding="UTF-8").read()
    #size = int(getInsider(content,"<p class=\"page_showing\">","</p>")[len("Showing\n"):])
    size = getInsider(content,"<p class=\"page_showing\">","</p>").split("-")
    sizeSt = size[0]
    sizeSt = sizeSt[len("Showing\n"):]
    if len(sizeSt) > 1:
        er = open("error.txt", "a")
        sizeSt = int(sizeSt[:len(sizeSt)-1])
        sizeEnd = int(size[1][1:])
        size = sizeEnd - sizeSt
        sz = (size+1)/10
        siz = size
        gen = all_occurences(content, "<li class=\"review_item clearfix\">", "</div>\n</li>")
        outputtxt = ''
        count = 0
        while size != 0:
            if(size % 10 == 0):
                count = count + 1
                count=count*(100/sz)
                print(str(int(count)) + "%")
                count = count/(100/sz)
            stInd = next(gen)
            try:
                endInd = next(gen)
            except StopIteration:
                endInd = len(content)
            newStr = content[stInd:endInd]
            reviewer = getInsider(newStr,"<div class=\"review_item_reviewer\">","</div>")
            outputtxt = outputtxt + "\"" + getInsider(getInsider(reviewer,"<h4","</h4>"), ">\n", "") + "\"," #name
            outputtxt = outputtxt + "\"" + getInsider(getInsider(
                getInsider(getInsider(newStr,"<span class=\"reviewer_country","</span>\n<"), ">", "")
                ,"</span",""), ">", "") + "\"," #country
            outputtxt = outputtxt + "\"" + getInsider(getInsider(reviewer,"<p class=\"reviewer_customer_type","</p>"),">", "") + "\"," #customerType
            outputtxt = outputtxt + "\"" + getInsider(getInsider(newStr,"<div class=\"review_item_review_score","</div>"),">","") + "\"," #score
            outputtxt = outputtxt + "\"" + getInsider(newStr,"<div class=\"review_item_header_content\">","</div>") + "\"," #scoreMeaning
            outputtxt = outputtxt + "\"" + getInsider(newStr,"<div class=\"review_item_header_date\">","</div>") + "\"," #Date
            prosCons = getInsider(newStr,"<div class=\"review_item_review_content","</div>") + "\"," #ProsAndCons
            pros = getInsider(getInsider(prosCons,"<p class=\"review_pos","</p>"),">","")
            if redo and len(pros) > 0:
                redo = False
            if len(pros) > 0:
                if pros[0] == "-":
                    pros = pros[1:]
            if lang != "non":
                try:
                    prosTr = gs.translate(pros, lang)
                    outputtxt = outputtxt + "\"" + prosTr + "\"," #Pros Translated
                except:
                    outputtxt = outputtxt + "\"" + "" + "\"," #Pros Translated
                    er.write(hotel + " " + str(int(index)*100 + (siz - size + 1)) + " Pro")
            cons = getInsider(getInsider(prosCons,"<p class=\"review_neg","</p>"),">","")
            if redo and len(cons) > 0:
                redo = False
            if len(cons) > 0:
                if cons[0] == "-":
                    cons = cons[1:]
            if lang != "non":
                try:
                    consTr = gs.translate(cons, lang)
                    outputtxt = outputtxt + "\"" + consTr + "\"," #Cons Translated
                except:
                    outputtxt = outputtxt + "\"" + "" + "\"," #Pros Translated
                    er.write(hotel + " " + str(int(index)*100 + (siz - size + 1)) + " Con")
            respon = getInsider(newStr,"data-full-response=\"","\">")
            if lang != "non":
                try:
                    responTr = gs.translate(respon, lang)
                    outputtxt = outputtxt + "\"" + responTr + "\"," #Response Translated
                except:
                    outputtxt = outputtxt + "\"" + "" + "\"," #Pros Translated
                    er.write(hotel + " " + str(int(index)*100 + (siz - size + 1)) + " Rev")
            outputtxt = outputtxt + "\"" + pros + "\"," #Pros
            outputtxt = outputtxt + "\"" + cons + "\"," #Cons
            outputtxt = outputtxt + "\"" + respon + "\"," #Response
            outputtxt = outputtxt + "\n"
            size = size - 1
        #text_file = open("selective.html", "w", encoding="UFT-8")
        #text_file.write(newStr)
        #text_file.close()
        if siz == 99:
            print(str(int(index) + 1) + " page(100 reviews per page) done!")
        else:
            print("Done!")
        text_file1 = open(hotel + "_" + lang + ".csv", "a", encoding="UTF-8", newline='')
        text_file1.write(outputtxt)
        text_file1.close()
        er.close()
    else:
        return -1
    return redo


#   while size != 0:
#       stInd = next(gen)
#       endInd = next(gen)
#       newStr = newStr + content[stInd:endInd]
#       size = size - 1


import urllib.request
import codecs

def mainFunc(hotel,startPos, lang):

    initURL = "http://www.booking.com/reviewlist.en-gb.html?sid=0;dcid=4;cc1=de;dist=1;pagename=" + hotel + ";type=total&;offset=" + str(startPos) + ";rows=100"
    req= urllib.request.Request(initURL,
    headers={'User-Agent' : "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"})
    html = urllib.request.urlopen(req).read()
    html = html.decode(encoding='UTF-8')
    text_file = open("out.html", "w", encoding="UTF-8")
    text_file.write(html)
    text_file.close()
    #text_file_c = open("out"+ str(startPos) + ".html", "w", encoding="UTF-8")
    #text_file_c.write(html)
    #text_file_c.close()
    if checkForNext(startPos/100, lang, hotel) == -1:
        return 0
    return len(html)

import html
import time
import html.parser
def singleFile(url, lang):
    start = time.time()
    hotel = url.split('?')[0]
    hotel = hotel.split('/')
    hotel = hotel[len(hotel)-1].split('.')[0]
    i=0
    print(hotel)
    f = open(hotel + "_" + lang + ".csv", "wb")
    f.write(codecs.BOM_UTF8)
    if lang == "non":
        st = "\"Name\",\"Country\",\"Traveler Type\",\"Score\",\"Score Explanation\",\"Date\",\"Pros\",\"Cons\",\"Response\"\n"
    else:
        st = "\"Name\",\"Country\",\"Traveler Type\",\"Score\",\"Score Explanation\",\"Date\",\"Pros\",\"Cons\",\"Response\",\"Pros Original\",\"Cons Original\",\"Response Original\"\n"
    f.close()
    f = open(hotel + "_" + lang + ".csv", "a")
    f.write(st)
    f.close()
    er = open("error.txt", "w")
    er.close()
    lenOfHtml = mainFunc(hotel,i, lang)
    while lenOfHtml>100:
        i = i + 100
        lenOfHtml = mainFunc(hotel,i,lang)
    content=open(hotel + "_" + lang + ".csv", encoding="UTF-8").read()
    #content = html.unescape(content)
    content = html.parser.HTMLParser().unescape(contents)
    f1 = open(hotel + "_" + lang + ".csv", "w", encoding="UTF-8", newline='')
    f1.write(content)
    f1.close()
    end = time.time()
    print (end - start)
    os.remove("out.html")

fileORSingle = input("enter F in order to get the info from txt file with list of links ( separated by enters ) or S for direct single input: ")
if(fileORSingle == "F"):
    lang = input("Please write he for Hebrew, en for English or ru for Russian or non (On all files): ")
    fileLoc = input("Please enter file name: ")
    listOfUrls=open(fileLoc).read()
    listOfUrls = listOfUrls.split("\n")
    for url in listOfUrls:
        singleFile(url, lang)
else:
    url = input("Please enter hotel link from booking.com: ")
    lang = input("Please write he for Hebrew, en for English or ru for Russian or non: ")
    singleFile(url, lang)

#u = urllib.request.urlopen(urllib.request.Request(initURL, headers={'User-Agent': user_agent}))
#raw_data = u.read()
#with urllib.request.urlopen(initURL) as url:
#    s = url.read()
#I'm guessing this would output the html source code?
#print(raw_data)