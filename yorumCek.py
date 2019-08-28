# -*- coding: utf-8 -*-
"""
Created on Aug 2019

@author: tarikbahar
"""
#Yorumları çekeceğimiz BeautifulSoup ve 
#excel işlemlerini yapacağımız openpyxl kütüphanelerini import edelim
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook

#Kodumuzu çalıştırmadan önce çektiğimiz yorumları kaydedeceğimiz excel dosyasını oluşturmalıyız !!!
#.py dosyası ile oluşturduğumuz excel dosyası aynı dizinde bulunmalı!

file = load_workbook("olusturdugumuz_excel_dosyası.xlsx")
sheet = file.active

def yorumCek(url):
    
    r = requests.get(url) #url'imize bağlanalım
    #print(r.status_code) #200 döndük başarılı

    soup = BeautifulSoup(r.content,"lxml") #ilgili url'in içeriğini parçaladık, uygun formata getirdik
    
    #turkcealtyazi.org sitesinde yorumların tutulduğu XPath'i öğrendik == class'ı ny8 olan div'de tutuluyormuş.
    yorumlar = soup.find_all("div", attrs={"class":"ny8"}) #Çektiğimiz tüm yorumları "yorumlar" değişkenine atadık.
#üstteki kod satırı uygun şekilde değiştirilebilirse bu kod herhangi bir siteden herhangi bir şeyi çekmekte ve excel'e yazmakta kullanılabilir..
    
    for yorum in yorumlar:
        sheet.append([yorum.text]) #Çekilen tüm yorumları tek tek döndük ve excel sheetine yazdık.
    
    print("Yorumlar Çekiliyor....")
    
#yorumları çekeceğimiz sayfaların url'lerini buraya ekleyebiliriz.
url_list = ["https://turkcealtyazi.org/yorumlar/0097165/dead-poets-society.html",
            "https://turkcealtyazi.org/yorumlar/0109830/forrest-gump.html",
            "https://turkcealtyazi.org/yorumlar/.....",
            "https://turkcealtyazi.org/yorumlar/.....",
            "https://turkcealtyazi.org/yorumlar/.....",
            ]

for url in url_list:
    yorumCek(url)  #url_list'e eklediğimiz url'leri tek tek yorumCek fonksiyonuna yollayalım
    
print("İşlem Tamamlandı")

file.save("olusturdugumuz_excel_dosyası.xlsx") #yazdığımız excel dosyasını kaydedelim ve kapatalım
file.close()

