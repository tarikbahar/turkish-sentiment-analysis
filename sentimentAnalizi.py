# -*- coding: utf-8 -*-
"""
Created on Aug 2019

@author: tarikbahar
"""

#Kullanacağımız kütüphaneleri ekleyelim
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split #Data setimizi test ve eğitim olarak bölmek için,
from sklearn.feature_extraction.text import CountVectorizer #Metini özelliklerin geçme sıklığı matrisine çevirmek için,
from sklearn.metrics import roc_auc_score , accuracy_score #Sonuçlarımızı değerlendirmek için accuracy ve area under curve kriterlerini kullanacağız.
from sklearn.feature_extraction.text import TfidfVectorizer #Metini özelliklerin ağırlığı matrisine çevirmek için,
from sklearn.linear_model import LogisticRegression 

#Data setini ekleyip sütunları isimlendirelim
column = ['Yorum',"Değerlendirme"]
data = pd.read_excel('yorumlar.xlsx', encoding ='iso-8859-9', sep='"')
data.columns=column

#Data setindeki değerlendirme sütununu 0 ve 1 ile ifade edelim
data["Değerlendirme"] = data["Değerlendirme"].replace("Negatif", 0)
data["Değerlendirme"] = data["Değerlendirme"].replace("Pozitif", 1)

#Data setindeki Türkçe dolgu kelimelerini kaldıralım
def remove_stopwords(df_fon):
    stopwords = open('turkce-stop-words', 'r').read().split() 
    #nltk.corpus.stopwords.words('turkish') ile de yapılabilir ancak biz stop word'lere ekleme yaptık
    #turkce-stop-words dosyası aynı dizinde olmalı
    df_fon['stopwords_removed'] = list(map(lambda doc: [word for word in doc if word not in stopwords], df_fon['Yorum']))

remove_stopwords(data)

#Data setimizi test ve eğitim alt kümelerine rastgele şekilde bölelim
X_train, X_test, y_train, y_test = train_test_split(data['Yorum'], data['Değerlendirme'], random_state = 0)

#Data setimize ve eğitim kümemize ait detay bilgi isterseniz aşağıdaki satırları kullanabilirsiniz.
#print(data.info())
#print(data.head())
#print(X_train.head())
#print('X_train shape: ', X_train.shape)


print("################## COUNT VECTORIZER ##################\n")
#CountVectorizer sınıfından bir nesne üretiyoruz ve eğitim verilerimize uyguluyoruz.
vect = CountVectorizer(encoding ='iso-8859-9').fit(X_train)

#X_train'deki metinleri bir matrise dönüştürdük.
X_train_vectorized = vect.transform(X_train) 

#Programı, vektörize ettiğimiz X eğitim verilerini kullanarak lojistik regresyon ile eğiteceğiz.
model = LogisticRegression(solver='lbfgs')
model.fit(X_train_vectorized, y_train)

#Ardından da X_test verilerini kullanarak tahminler yapacağız
#Ve eğri puanının altındaki alan ile isabetliliği hesaplayacağız.
tahmin = model.predict(vect.transform(X_test))
print('AUC Score: ', roc_auc_score(y_test, tahmin))
print('Accuracy Score: ' ,accuracy_score(y_test, tahmin))

#Eğittiğimiz modelin bu tahminleri nasıl yaptığını daha iyi anlamak için, 
#oluşturduğumuz matrisin özelliklerini alalım.
#Daha sonra da sıralı modelimizdeki ilk 20 ve son 20 değerlerin karşılık geldiği özellikleri yazdıralım
ozellik_isimleri = np.array(vect.get_feature_names())
sorted_coef_index = model.coef_[0].argsort()
print('\nNegatif:\n',ozellik_isimleri[sorted_coef_index[:20]])
print('\nPozitif:\n',ozellik_isimleri[sorted_coef_index[:-21:-1]])
#print(feature_names[sorted_coef_index[:]])

print("\n################## TF-IDF VECTORIZER ##################\n")

#tf-idf vectorizer'ı sınıfından bir nesne üretiyoruz ve eğitim verilerimize uyguluyoruz 
#5 metinden daha az metinde gözüken kelimeleri, listemizden kaldıracağımız için min_df = 5 diyoruz.
vect = TfidfVectorizer(min_df = 5).fit(X_train)

#X_train'deki metinleri bir matrise dönüştürdük.
X_train_vectorized = vect.transform(X_train)

#Programı, vektörize ettiğimiz X eğitim verilerini kullanarak lojistik regresyon ile eğiteceğiz.
model = LogisticRegression(solver='lbfgs')
model.fit(X_train_vectorized, y_train)

#Ardından da X_test verilerini kullanarak tahminler yapacağız
#Ve eğri puanının altındaki alan ile isabetliliği hesaplayacağız.
tahmin = model.predict(vect.transform(X_test))
print('AUC Score: ', roc_auc_score(y_test, tahmin))
print('Accuracy Score: ' ,accuracy_score(y_test, tahmin))

#Eğittiğimiz modelin bu tahminleri nasıl yaptığını daha iyi anlamak için, 
#oluşturduğumuz matrisin özelliklerini alalım.
#Daha sonra da sıralı modelimizdeki ilk 20 ve son 20 değerlerin karşılık geldiği özellikleri yazdıralım
ozellik_isimleri = np.array(vect.get_feature_names())
sorted_tfidf_index = X_train_vectorized.max(0).toarray()[0].argsort()
print('\nMin Tf-Idf:\n',ozellik_isimleri[sorted_tfidf_index[:20]])
print('\nMax Tf-Idf:\n',ozellik_isimleri[sorted_tfidf_index[:-21:-1]])

print("\n################## N-GRAM ##################\n")
      
#n-gramlar, dizilimdeki (sequence) tekrar oranını bulmaya yarayan yöntemdir.
#Biz unigram ve bigram kullanacağız
#tf-idf'deki gibi min 5 metin limitimizi koyuyoruz. ardından da 1-gram ve 2-gram kullanarak data setimizi eğitiyoruz.
vect = CountVectorizer(min_df = 5, ngram_range = (1,2)).fit(X_train)

#X_train'deki metinleri bir matrise dönüştürdük.
X_train_vectorized = vect.transform(X_train)

#Programı, vektörize ettiğimiz X eğitim verilerini kullanarak lojistik regresyon ile eğiteceğiz.
model = LogisticRegression(solver='lbfgs')
model.fit(X_train_vectorized, y_train)

#Ardından da X_test verilerini kullanarak tahminler yapacağız
#Ve eğri puanının altındaki alan ile isabetliliği hesaplayacağız.
tahmin = model.predict(vect.transform(X_test))
print('AUC Score: ', roc_auc_score(y_test, tahmin))
print('Accuracy Score: ' ,accuracy_score(y_test, tahmin))

#Eğittiğimiz modelin bu tahminleri nasıl yaptığını daha iyi anlamak için, 
#oluşturduğumuz matrisin özelliklerini alalım.
#Daha sonra da sıralı modelimizdeki ilk 20 ve son 20 değerlerin karşılık geldiği özellikleri yazdıralım
ozellik_isimleri = np.array(vect.get_feature_names())
sorted_coef_index = model.coef_[0].argsort()
print('\nNegatif:\n',ozellik_isimleri[sorted_coef_index][:20])
print('\nPozitif:\n',ozellik_isimleri[sorted_coef_index][:-21:-1])

#Son olarak da kullanıcıdan çıkış yapmadığı sürece input olarak yorum alalım.
while(True):
    yorum=input("Yorumunuz Nedir?(Programı sonlandırmak için \'Q\' yazınız)\n")
    if(yorum == 'Q' or yorum == 'q'):
        break
    elif(len(yorum)<20):
        print("\nDaha uzun bir yorum giriniz!")
    else:
        if(model.predict(vect.transform([yorum]))==[0]):
            print("\nOLUMSUZ")
        elif(model.predict(vect.transform([yorum]))==[1]):
            print("\nOLUMLU")