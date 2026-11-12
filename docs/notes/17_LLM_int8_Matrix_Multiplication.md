# Çalışma Notu #17 — LLM.int8(): 8-bit Matrix Multiplication - arXiv:2208.07339

- **Kategori:** Kısıtlı Donanım, Kuantizasyon ve SLM Motoru
- **Kaynak / Makale:** [Yerel PDF (`17_LLM_int8_Matrix_Multiplication.pdf`)](../../papers/17_LLM_int8_Matrix_Multiplication.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2208.07339)
- **İlgili SENTINEL Düğümleri:** [`Node 1`](../../src/nodes/node_1_metacognitive_controller.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Modeller 6.7B parametre sınırını aştığında aktivasyon vektörlerinde beliren aykırı değerleri (emergent outliers) tespit eden ve bu aykırı özellikleri (%0.1) FP16'da tutarken geri kalan %99.9 ağırlığı INT8 ile çarpan iki yollu matris çarpım mimarisi. Performans kaybı yaşamadan modellerin düşük bitlerde çalışabilmesinin teorik zeminini oluşturmuştur.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL çekirdeğinin sayısal kararlılığı ve CPU üzerinde INT8 vektör komutlarının (VNNI) hassasiyet kaybı yaşamadan çalışabilmesinin teorik güvencesidir. Kuantize modellerimizde aykırı değerlerin doğru yönetildiğinden emin olmamızı sağlar.

## 3. Taslak Uygulama ve Mimari Mantık
- CPU çıkarım motorunda vektör tabanlı kuantizasyon rutinlerinin seçimi ve doğrulanması.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Çok düşük bit kuantizasyonlarında (örn. 2-bit) aykırı değerlerin kırpılması riskine karşı dikkatli olunmalıdır.
