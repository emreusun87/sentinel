# Çalışma Notu #06 — DeepSeek-R1 (Saf Takviyeli Öğrenme ile Akıl Yürütme) - arXiv:2501.12948

- **Kategori:** Test Anı Akıl Yürütme (Test-Time Compute)
- **Kaynak / Makale:** [Yerel PDF (`06_DeepSeek_R1_Reasoning.pdf`)](../../papers/06_DeepSeek_R1_Reasoning.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2501.12948)
- **İlgili SENTINEL Düğümleri:** [`Node 1`](../../src/nodes/node_1_metacognitive_controller.py), [`Node 2`](../../src/nodes/node_2_world_model_hypothesis.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Geniş ölçekli takviyeli öğrenme (GRPO) kullanılarak modellerin insan denetimli eğitime gerek duymaksızın kendi kendine akıl yürütme, hata fark etme ve strateji değiştirme becerisi kazanabileceğini kanıtlayan çalışma. Model `<think>` blokları içinde kendi adımlarını sorgulamakta ve bu akıl yürütme paternleri 1.5B ve 7B'lik küçük açık kaynaklı modellere (Qwen tabanlı) başarıyla aktarılabilmektedir.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL'in birincil çekirdeği ($M_{\text{core}}$) olarak `DeepSeek-R1-Distill-Qwen-1.5B` ve `7B` modellerinin 4-bit GGUF sürümlerini CPU üzerinde konumlandırıyoruz.
Model, karmaşık bir Linux veya veritabanı krizinde doğrudan körlemesine komut üretmek yerine;
1) Düşünce zincirinde olası arıza sebeplerini sıralar,
2) Yanlış varsayımlarını fark edip düzeltir,
3) Doğrulanmış nihai komutu çıktı olarak verir.

## 3. Taslak Uygulama ve Mimari Mantık
- Modelden dönen metin çift kanala ayrılır:
  - `<think> ... </think>` aralığı: Sistemin iç telemetri günlüğüne yazılır (üst-biliş denetimi ve analiz için saklanır).
  - `[ACTION] ... [/ACTION]` aralığı: Canlı terminalde çalıştırılacak doğrulanmış komut olarak icra katmanına iletilir.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Distile modeller bazen iç monologda döngüye girip gereksiz uzayabilir; bu durumu önlemek için maksimum düşünme jetonu sınırı (`max_reasoning_tokens=1024`) tanımlanmalıdır.
