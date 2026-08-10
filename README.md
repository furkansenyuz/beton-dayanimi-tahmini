# Beton Basınç Dayanımı Tahmini

TRAI bootcamp final ödevim. İnşaat sektöründe çalışıyorum, o yüzden kendime yakın bir konu seçtim: beton karışım bileşenlerinden (çimento, su, agrega, yaş vb.) basınç dayanımını tahmin etmek. Doğrusal regresyon, polinom regresyon (degree=2), random forest, Lasso ve Ridge denedim; üstüne su/çimento oranıyla öznitelik mühendisliği, k-fold çapraz doğrulama, RandomizedSearchCV ile hiperparametre araması ve SHAP ile açıklanabilirlik ekledim. En iyi sonuç: su_cimento özelliği + randomized search ile ayarlanmış random forest (test R2 0.893, rmse 5.25 MPa; 5-fold cv ortalaması 0.91). Veriyi kontrol edince 1030 satırın aslında 427 benzersiz karışım olduğunu, aynı karışımın farklı yaşlarda tekrar ölçüldüğünü gördüm; rastgele KFold bunu sızdırıyor. GroupKFold ile dürüst rakam R2 0.89, rmse 5.50 MPa. Veri seti: Concrete Compressive Strength (Yeh, 1998), Kaggle/UCI.

Demoda ayrıca TS EN 206-1 katmanı var: model tahmini Çizelge 14 uygunluk kriteriyle karakteristik dayanıma çevriliyor, sonuç Çizelge F.1'deki etki sınıfı sınır değerleriyle (en büyük su/çimento, en küçük dayanım sınıfı, en az çimento) karşılaştırılıyor. Uçucu kül k-değeri Madde 5.2.5.2.2'ye göre uygulanıyor.

Notebook: beton_dayanimi_tahmini.ipynb (Google Colab'da çalışır), grafikler grafikler/ klasöründe, Medium yazısının taslağı medium_yazisi.md dosyasında.

Canlı demo: https://furkansenyuz.com/beton-dayanimi-tahmini/demo/ (model tarayıcıda çalışıyor, sunucu yok)

Medium yazısı:

Veri seti: https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength

Furkan Şenyüz
