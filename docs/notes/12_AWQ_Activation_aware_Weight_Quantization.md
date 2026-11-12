# Çalışma Notu #12 — AWQ: Activation-aware Weight Quantization - arXiv:2306.00978

- **Kategori:** Kısıtlı Donanım, Kuantizasyon ve SLM Motoru
- **Kaynak / Makale:** [Yerel PDF (`12_AWQ_Activation_aware_Weight_Quantization.pdf`)](../../papers/12_AWQ_Activation_aware_Weight_Quantization.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2306.00978)
- **İlgili SENTINEL Düğümleri:** [`Node 1`](../../src/nodes/node_1_metacognitive_controller.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Klasik kuantizasyon tüm ağırlıkları eşit kabul ederek düşük bitlerde (INT4/INT3) modelin anlama kapasitesini bozar. AWQ, modelin zekasını taşıyan kritik ağırlıkların yalnızca %1 civarında olduğunu ve bu ağırlıkların aktivasyon büyüklüklerine bakılarak korunabileceğini gösterir. Bu kritik ağırlıklar korunarak model 4-bit seviyesine sıkıştırılabilir; herhangi bir ek eğitim veya backpropagation gerektirmez.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL'in CPU bellek yönetimi için temel yapı taşıdır. 7B-8B parametreli modeller normalde 16 GB bellek gerektirirken; 4-bit AWQ / GGUF (Q4_K_M) formatıyla 4.5 GB RAM sınırına indirilir.
Bu sayede standart 16 GB RAM'e sahip bir makinede hem işletim sistemi ve veritabanı servisleri rahat çalışır hem de SENTINEL arka planda kesintisiz hizmet verir.

## 3. Taslak Uygulama ve Mimari Mantık
- Çekirdek model formatı: Q4_K_M GGUF veya AWQ optimize ağırlıklar.
- CPU SIMD döngülerinde INT4 ağırlıkların işlenmesiyle bellek bant genişliği darboğazı aşılır.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Kuantizasyon seviyesi INT3'ün altına düşürülmemelidir; akıl yürütme ve kodlama sentaksında bozulmalar yaşanabilir.
