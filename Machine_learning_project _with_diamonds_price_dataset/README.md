# Elmas Fiyat Tahmini Projesi

Bu proje, elmasların temel fiziksel ve kalite özelliklerine bakarak **tahmini fiyatlarını hesaplayan** bir makine öğrenmesi çalışmasıdır.  
Amaç; gerçek hayattaki elmas fiyatlandırma problemine benzer bir yapıyı, veriye dayalı bir modelle örneklemek ve makine öğrenmesinin uçtan uca nasıl kullanılabileceğini göstermektir.

---

## Projenin Amacı

- Elmasların özellikleri ile fiyatları arasındaki ilişkiyi incelemek
- Bu ilişkiyi kullanarak **otomatik fiyat tahmini** yapabilen bir model oluşturmak
- Modeli bir web arayüzü üzerinden herkesin kolayca deneyebileceği hale getirmek
- Makine öğrenmesi projelerinde:
  - Veri → Özellikler → Model → Tahmin akışını
  - Modelin bir web servisine (API) entegre edilmesini
göstermek

---

## Kullanılan Elmas Özellikleri

Model, her elmas için şu bilgileri kullanır:

- **Karat (`carat`)**: Elmasın ağırlığı
- **Kesim kalitesi (`cut`)**: Fair, Good, Very Good, Premium, Ideal gibi kategoriler
- **Renk (`color`)**: D–J aralığında, renksizden daha sarı tonlara doğru giden sınıflar
- **Berraklık (`clarity`)**: I1, SI2, SI1, VS2, VS1, VVS2, VVS1, IF gibi saflık sınıfları
- **Derinlik oranı (`depth`)**: Elmasın derinliğinin boyutlarına göre yüzdesel oranı
- **Tabla oranı (`table`)**: Üst yüzeyin (tabla) büyüklüğünün yüzdesel oranı
- **Fiziksel ölçüler (`x`, `y`, `z`)**: Elmasın milimetre cinsinden uzunluk, genişlik ve derinliği

Bu özellikler, veri setindeki örneklerden öğrenilerek, yeni bir elmas için **tahmini fiyat** üretmekte kullanılır.

---

## Model ve Dosya Yapısı Hakkında

Projede, eğitim süreci tamamlandıktan sonra elde edilen model, aşağıdaki dosyada saklanır:

- `diamond_model_complete.pkl`

Bu dosyanın içinde:
- **Eğitimli model** (örneğin bir scikit-learn regresyon modeli)
- **Kategorik değişkenler için dönüştürücüler** (`encoders`)
- **Özelliklerin ölçeklenmesi için kullanılan scaler** (`scaler`)
bulunur.

Uygulama çalışırken:
1. Kullanıcının girdiği özellikler alınır.
2. Kategorik alanlar (cut, color, clarity) uygun sayısal forma dönüştürülür.
3. Tüm özellikler aynı ölçeğe getirilir (scaling).
4. Model bu veriyi kullanarak tahmini fiyatı hesaplar.

---

## Teknik Altyapı (Kısa Özet)

- **Backend (API)**:
  - Framework: **FastAPI**
  - Ana Python dosyası: `app.py`
  - Uygulama giriş noktası: `main.py`
  - Tahmin için `POST /predict` endpoint'i bulunur.

- **Web Arayüzü**:
  - Şablon: `templates/index.html`
  - Teknolojiler: HTML, CSS, **Bootstrap**
  - Kullanıcı dostu bir form üzerinden girdi alır, sonucu sayfa üzerinde gösterir.

- **Veri Bilimi / Makine Öğrenmesi**:
  - Kütüphaneler: **scikit-learn**, **pandas**
  - Model dosyası: `diamond_model_complete.pkl`
  - Ek olarak örnek/test veri dosyası: `30-test_scaled.csv` (analiz veya test amaçlı kullanılabilir)
