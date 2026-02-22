# Readme 

# Ev Fiyatı Tahmini Projesi

Ev özelliklerine göre fiyat tahmini yapan **makine öğrenmesi** modeli ve bu modeli kullanan **web uygulaması**. Proje üç katmandan oluşur: veri analizi ve model eğitimi (Jupyter Notebook), REST API (FastAPI) ve tek sayfalık arayüz (HTML/JS).

---

## Proje Özeti

- **Notebook:** CSV verisiyle keşifsel analiz, özellik mühendisliği, Linear Regression eğitimi ve eğitilmiş model + scaler'ın `House_price_regression.pkl` olarak kaydedilmesi.
- **API:** `app.py` ile FastAPI; ana sayfa HTML formu, tahmin için `/predict` POST endpoint'i. Model ve scaler pickle dosyasından yüklenir.
- **Arayüz:** `templates/index.html` ile ev özellikleri formu; tahmin TRY formatında gösterilir.

---

## Proje Yapısı

```
proje/
├── app.py                          # FastAPI uygulaması (/, /predict)
├── House_price_regression.ipynb     # Veri analizi + model eğitimi + pkl kaydetme
├── House_price_regression.pkl       # Kaydedilmiş model + scaler (pickle)
├── house_price_regression_dataset.csv
├── requirements.txt
├── templates/
│   └── index.html                  # Ev fiyatı tahmin formu (tek sayfa)
└── README.md
```

---

## 1. Veri Seti

**Dosya:** `house_price_regression_dataset.csv`

| Sütun (CSV)           | Açıklama                    | API/Form alanı        |
|-----------------------|-----------------------------|------------------------|
| Square_Footage        | Alan (ft²)                  | `square_footage`       |
| Num_Bedrooms          | Yatak odası sayısı          | `bedrooms`             |
| Num_Bathrooms         | Banyo sayısı                | `bathrooms`            |
| Year_Built            | Yapım yılı                  | — (notebook'ta ev yaşına dönüştürülür) |
| Lot_Size              | Arsa büyüklüğü (dönüm)      | `lot_size`             |
| Garage_Size           | Garaj kapasitesi (araç)     | `garage`               |
| Neighborhood_Quality  | Mahalle puanı (1–10)        | `neighborhood_score`   |
| House_Price           | Hedef: ev fiyatı            | —                      |

Notebook'ta `Year_Built` kullanılarak **ev yaşı** (`house_age`) hesaplanır; API ve form doğrudan `house_age` (yıl) alır.

---

## 2. House_price_regression.ipynb

- **Kütüphaneler:** pandas, numpy, matplotlib, seaborn, scikit-learn.
- **İşlemler:**
  - Veri yükleme, `head` / `info` ile inceleme.
  - Özellik mühendisliği: `Age_Built` = 2026 − `Year_Built`, sonra `Year_Built` atılır.
  - Sütun isimleri: `square_footage`, `bedrooms`, `bathrooms`, `lot_size`, `garage`, `neighborhood_score`, `house_price`, `house_age`.
  - Görselleştirme (korelasyon, dağılım vb.).
  - Train/test: `train_test_split(X, y, test_size=0.2, random_state=42)`.
  - **StandardScaler** ile ölçeklendirme; sadece eğitim verisiyle `fit`, test verisiyle `transform`.
  - **LinearRegression** ile eğitim; R², MAE, MSE ve gerçek–tahmin scatter grafiği.
  - Model ve scaler'ı pickle ile kaydetme:
    ```python
    pickle.dump({"model": lineer, "scaler": scaler}, f)
    ```
    Çıktı dosyası: `House_price_regression.pkl`.

---

## 3. House_price_regression.pkl

- **İçerik:** Tek bir pickle dosyasında sözlük:
  - `"model"`: Eğitilmiş `sklearn.linear_model.LinearRegression` nesnesi.
  - `"scaler"`: Eğitim verisiyle fit edilmiş `sklearn.preprocessing.StandardScaler` nesnesi.
- **Kullanım:** `app.py` başlangıçta bu dosyayı açar; her tahminde gelen 7 özellik (modelin eğitiminde kullanılan sıra ve isimlerle) scaler ile dönüştürülüp modele verilir.

---

## 4. app.py (FastAPI)

- **Framework:** FastAPI, şablonlar için Jinja2 (`templates` klasörü).
- **Başlangıç:** `House_price_regression.pkl` okunur; `saved_data["model"]` ve `saved_data["scaler"]` global kullanılır.
- **Modeller:** Pydantic `HousePrice`:
  - `square_footage` (int), `bedrooms` (int), `bathrooms` (int), `lot_size` (float), `garage` (int), `neighborhood_score` (int), `house_age` (int).
- **Endpoint'ler:**
  - `GET /`: `templates/index.html` döner (ev fiyatı tahmin formu).
  - `POST /predict`: JSON gövdesi `HousePrice` ile gelir; DataFrame yapılır, scaler ile scale edilir, model ile tahmin alınır; `{"prediction": <float>}` döner.

---

## 5. templates/index.html

- **Dil:** Türkçe (`lang="tr"`).
- **İçerik:** Tek sayfa, tek form. Kullanıcıdan alınan alanlar:
  - Alan (ft²), yatak odası, banyo, arsa büyüklüğü (dönüm), garaj kapasitesi, mahalle puanı (1–10), ev yaşı (yıl).
- **Stil:** Koyu gradient arka plan, kart yapısı, buton ve input stilleri; başarı/hata mesajları için `.result.success` ve `.result.error`.
- **JavaScript:** Form submit’te `POST /predict` çağrılır; gelen `prediction` değeri Türk Lirası (TRY) formatında `.price` alanında gösterilir; hata durumunda `.result.error` ile mesaj gösterilir.

---

## Gereksinimler ve Çalıştırma

### Bağımlılıklar

```bash
pip install -r requirements.txt
```

Öne çıkan paketler: `fastapi`, `uvicorn`, `Jinja2`, `pandas`, `pydantic`, `scikit-learn`, `numpy`.

### Modeli yeniden eğitmek (isteğe bağlı)

1. Jupyter’da `House_price_regression.ipynb` dosyasını açın.
2. Tüm hücreleri sırayla çalıştırın; son hücreler `House_price_regression.pkl` dosyasını oluşturur/günceller.

### Web uygulamasını çalıştırmak

1. Proje kök dizininde (`app.py` ve `House_price_regression.pkl` aynı dizinde olmalı):
   ```bash
   uvicorn app:app --reload
   ```
2. Tarayıcıda `http://127.0.0.1:8000` adresine gidin; formu doldurup “Fiyat Tahmin Et” ile tahmin alın.

### API kullanımı (örnek)

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"square_footage\": 2000, \"bedrooms\": 3, \"bathrooms\": 2, \"lot_size\": 2.5, \"garage\": 1, \"neighborhood_score\": 7, \"house_age\": 15}"
```

Yanıt örneği: `{"prediction": 450000.123}`.

---

## Özet Tablo

| Bileşen              | Dosya / Konum          | Açıklama                                      |
|----------------------|------------------------|-----------------------------------------------|
| Veri                 | `house_price_regression_dataset.csv` | Ham ev özellikleri ve fiyatlar        |
| Analiz & model      | `House_price_regression.ipynb`       | EDA, özellik mühendisliği, eğitim, pkl kayıt |
| Kayıtlı model        | `House_price_regression.pkl`         | `model` + `scaler` sözlüğü                    |
| Backend              | `app.py`               | FastAPI: `/`, `/predict`                     |
| Frontend             | `templates/index.html` | Tahmin formu ve TRY formatında sonuç          |

Bu proje eğitim amaçlıdır.
