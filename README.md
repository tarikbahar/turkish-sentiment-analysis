## Turkish Sentiment Analysis
Sentiment Analysis of the movie and series reviews in the Turkish language

- Developed `yorumCek.py` for collect data
- Collected reviews from turkcealtyazi.org with `yorumCek.py`
- Labeled reviews as positive and negative.
- Cleared and edited data (such as stopword removal)
- Developed `sentimentAnalizi.py` for sentiment analysis
- Used CountVectorizer, TfidfVectorizer and n-gram
- Trained with LogisticRegression Algorithm
- Tested results with accuracy score and roc-auc-score

## Türkçe Duygu Analizi
Türkçe dizi ve film yorumları üzerine bir duygu analizi

- Veri toplamak için `yorumCek.py` geliştirildi.
- turkcealtyazi.org sitesinden `yorumCek.py` kullanılarak yorumlar toplandı.
- Toplanan veriler pozitif ve negatif olarak etiketlendi.
- Etkisiz kelimelerin silinmesi gibi işlemlerle toplanan veriler temizlendi.
- Duygu analizi için `sentimentAnalizi.py` dosyası geliştirildi.
- CountVectorizer, TfidfVectorizer ve n-gram yöntemleri kullanıldı.
- Lojistik Regresyon Algoritması ile eğitildi.
- Sonuçlar doğruluk ve eğri altında kalan alan skorları ile test edildi.
