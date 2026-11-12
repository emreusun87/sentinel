# Çalışma Notu #03 — BitNet b1.58 2B4T (1.58-Bit Ternary Ağırlık Mimarisi) - arXiv:2504.12285

- **Kategori:** Kısıtlı Donanım, Kuantizasyon ve SLM Motoru
- **Kaynak / Makale:** [Yerel PDF (`03_BitNet_b1_58_2B4T.pdf`)](../../papers/03_BitNet_b1_58_2B4T.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2504.12285)
- **İlgili SENTINEL Düğümleri:** [`Node 1`](../../src/nodes/node_1_metacognitive_controller.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Geleneksel derin öğrenmedeki kayan nokta (FP16/BF16) matris çarpımlarının yerine tüm model ağırlıklarının {-1, 0, 1} üçlü (ternary) değer kümesine sıkıştırıldığı 1-bit mimarisidir. Bu sayede hesaplama açısından pahalı Matrix Multiplication operasyonları, basit tam sayı toplama ve çıkarma işlemlerine indirgenir. 2 milyar parametreli bir model 4 trilyon token ile eğitildiğinde FP16 kalitesine yaklaşırken; bellek tüketiminde 3.5 kata, enerji ve işlemci gecikmesinde ise 4-8 kata varan verimlilik sağlar.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL projesinin en büyük donanım kısıtı harici GPU bulunmamasıdır. Standart bir x86 işlemcide AVX-512 veya AVX2 komut setleri ile ternary tam sayı toplama operasyonları son derece yüksek verimle çalışır.
2 milyar parametreli bir BitNet modeli bellek üzerinde yalnızca ~500–600 MB RAM tüketir. Bu durum, SENTINEL'in mütevazı sunucularda veya dizüstü CPU kaynaklarında dahi saniyede 30–40 token üretim hızına ulaşarak 7/24 çalışabilmesini mümkün kılar.

## 3. Taslak Uygulama ve Mimari Mantık
- Çıkarım altyapısı olarak `bitnet.cpp` derlenip sisteme entegre edilecek.
- Derleme bayrakları hedef işlemci mimarisine göre (`-march=native -mavx512f -mavx512vnni`) optimize edilecek.
- SENTINEL yerel çıkarım sınıfı doğrudan bu kütüphaneyi çağıracak:
```python
class LocalBitNetEngine:
    def __init__(self, model_path="models/bitnet_2b4t.bin"):
        self.model = BitNetCppWrapper(
            model_path=model_path,
            threads=4,
            use_simd=True,
            context_size=4096
        )
    def generate(self, prompt):
        return self.model.stream_generate(prompt, temp=0.2)
```

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Sıfırdan model ön-eğitimi yapmayacağımız için açık kaynaklı ön-eğitilmiş BitNet b1.58 modelleri kullanılmalı ve sistem yönetimi görevleri için LoRA veya prompt şablonlarıyla uyarlanmalıdır.
