# Çalışma Notu #05 — s1: Simple Test-Time Scaling - arXiv:2501.19393

- **Kategori:** Test Anı Akıl Yürütme (Test-Time Compute)
- **Kaynak / Makale:** [Yerel PDF (`05_s1_Simple_Test_Time_Scaling.pdf`)](../../papers/05_s1_Simple_Test_Time_Scaling.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2501.19393)
- **İlgili SENTINEL Düğümleri:** [`Node 1`](../../src/nodes/node_1_metacognitive_controller.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Gelişmiş akıl yürütme modellerinin başarısının arkasındaki temel dinamik, çıkarım anında modele ayrılan düşünme bütçesidir (Test-Time Compute). Makalede gösterildiği üzere; 1.000 adet kaliteli akıl yürütme verisiyle eğitilen görece küçük bir model, çıkarım sırasında özel jetonlarla ("Wait", duraklatma ve gerekçe genişletme) yönlendirilip düşünce zinciri uzatıldığında, kendisinden çok daha büyük modellerin doğruluk seviyesini yakalayabilmektedir.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL'de 70B parametreli modelleri çalıştırma imkanımız yok. Ancak 2B–7B aralığındaki modellerimize kritik sistem yönetimi ve veritabanı kararlarında `Budget Forcing` tekniği uygulayabiliriz.
Model aceleyle nihai bir aksiyon komutu vermeye kalktığında araya girilerek alternatif senaryoları, geri alma adımlarını ve güvenlik kısıtlarını incelemesi yönünde ek düşünme jetonu harcamaya zorlanacak. Böylece küçük modelin analiz derinliği artırılacak.

## 3. Taslak Uygulama ve Mimari Mantık
```python
def generate_deliberative_plan(prompt, min_thinking_tokens=500):
    context = f"{prompt}\n<think>\n"
    tokens_produced = 0

    while tokens_produced < min_thinking_tokens:
        chunk = core_slm.generate_chunk(context, max_tokens=128)
        context += chunk
        tokens_produced += len(chunk.split())

        # Model erken sonuç bildirmeye çalışırsa düşünmeye devam ettir
        if "</think>" in chunk or "Sonuc olarak:" in chunk:
            if tokens_produced < min_thinking_tokens:
                context += "\n[Sistem: Henuz karar verme. Geri alma (rollback) adimlarini ve kenar durumlari tekrar degerlendir...]\n"

    context += "\n</think>\n[AKSIYON PLANI]:"
    return core_slm.generate_final(context)
```

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- CPU üzerinde düşünme jetonlarının artması yanıt süresini 10–25 saniye uzatacaktır. Bu nedenle mekanizma basit durum kontrollerinde değil, yalnızca riskli konfigürasyon değişikliklerinde devreye alınmalıdır.
