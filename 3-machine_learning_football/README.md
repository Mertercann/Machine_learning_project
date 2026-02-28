# Futbolcu Değer Tahmini

Bu proje, bir futbolcunun istatistiklerine ve oynadığı takıma göre **tahmini piyasa değerini** (transfer değerini) hesaplayan bir web uygulamasıdır. Amacı, makine öğrenmesi ile futbolcu verilerinden anlamlı bir değer çıkarmak ve bunu kart tarzı bir arayüzle göstermektir.

## Proje Hakkında

Transfer dönemlerinde futbolcuların piyasa değerleri tartışılır; bu değerler kulüpler, menajerler ve taraftarlar için önemlidir. Bu projede, bir futbolcunun **takımı**, **pozisyonu**, **yaşı**, **maç sayısı**, **gol**, **asist** ve **pas isabeti** gibi temel istatistikleri kullanılarak, makine öğrenmesi modeli ile tahmini bir değer (milyon euro cinsinden) üretilir.

Veri seti olarak Kaggle üzerinden alınan **synthetic_football_stats_2025** kullanılmıştır. Bu veri seti üzerinde eğitilen model, ön işleme (preprocessor) ve ölçekleme (scaler) ile birlikte projede saklanır; web arayüzü kullanıcının girdiği bilgileri bu modele gönderir ve dönen tahmini değeri gösterir.

## Nasıl Çalışır?

1. **Veri ve model**  
   Sentetik futbolcu istatistikleri ile eğitilmiş bir model, scaler ve preprocessor `synthetic_football_stats_2025.pkl` dosyasında tutulur. Uygulama açılırken bu dosya yüklenir.

2. **Web arayüzü**  
   Kullanıcı bir takım seçer (seçilen takımın amblemi ekranda görünür), pozisyon, yaş, maç sayısı, gol, asist ve pas isabeti gibi alanları doldurur. "Değer Hesapla" butonuna basıldığında bu bilgiler sunucuya gönderilir.

3. **Tahmin**  
   Sunucu, gelen veriyi modelin beklediği formata dönüştürür (ön işleme ve ölçekleme), modeli çalıştırır ve tahmini piyasa değerini milyon euro (M€) cinsinden hesaplar. Bu değer, ekranda futbolcu kartı görünümünde kullanıcıya gösterilir.

Böylece proje, hem makine öğrenmesi hem de web arayüzü ile bir futbolcu değer tahmin sistemi sunar; teknik detaylar (API, kurulum) bu amaca hizmet eder.

## Çalıştırmak İçin

Proje klasöründe bağımlılıklar yüklendikten sonra:

```bash
uvicorn app:app --reload
```

komutu ile sunucu başlatılır. Tarayıcıda **http://127.0.0.1:8000** adresi açılarak uygulama kullanılabilir. `synthetic_football_stats_2025.pkl` dosyasının proje kökünde bulunması gerekir.
