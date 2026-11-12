# Çalışma Notu #16 — Reflexion: Language Agents with Verbal RL - arXiv:2303.11366

- **Kategori:** Test Anı Akıl Yürütme (Test-Time Compute)
- **Kaynak / Makale:** [Yerel PDF (`16_Reflexion_Verbal_Reinforcement.pdf`)](../../papers/16_Reflexion_Verbal_Reinforcement.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2303.11366)
- **İlgili SENTINEL Düğümleri:** [`Node 6`](../../src/nodes/node_6_meta_evaluator.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Geleneksel pekiştirmeli öğrenmedeki ağırlık güncellemeleri yerine; ajanın karşılaştığı hataları sözel olarak eleştirmesi ("Nerede hata yaptım? X komutunda parametre eksikti"), bu eleştiriyi bir bellek tamponunda tutması ve bir sonraki denemenin bağlamına eklemesiyle başarı oranının artırılabileceğini gösteren çalışma.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
Yerel CPU ortamında ağırlık güncellemesi (fine-tuning) yapamayacağımız için Reflexion yaklaşımı bizim öğrenme motorumuzdur.
SENTINEL uzak sunucuda bir SSH komutunda "Permission Denied" veya "Syntax Error" aldığında:
- İçsel eleştiri üretilir: `[REFLEXION]: Bu komut normal kullanıcı yetkisiyle çalıştırılamıyor. Bir sonraki adımda sudo ön-eki ile denenmeli.`
- Bu not kısa süreli epizodik belleğe kaydedilir ve ikinci denemede doğrudan bağlama eklenir.

## 3. Taslak Uygulama ve Mimari Mantık
- Deneme 1 (Başarısız) -> Hata Çıktısı -> Sözel Eleştiri Üretimi -> Deneme 2 (Öz-Eleştiri ile Güçlendirilmiş Prompt) -> Başarılı İcra.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Modelin aynı hatada takılı kalmaması için maksimum yansıma döngüsü 3 deneme ile sınırlandırılmalı; 3. denemede de çözülemezse teknik blokaj olarak raporlanmalıdır.
