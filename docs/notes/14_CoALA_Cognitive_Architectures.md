# Çalışma Notu #14 — CoALA: Cognitive Architectures for Language Agents - arXiv:2309.02427

- **Kategori:** Bilişsel Mimari ve Bellek Hiyerarşisi
- **Kaynak / Makale:** [Yerel PDF (`14_CoALA_Cognitive_Architectures.pdf`)](../../papers/14_CoALA_Cognitive_Architectures.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2309.02427)
- **İlgili SENTINEL Düğümleri:** [`Node 1`](../../src/nodes/node_1_metacognitive_controller.py), [`Node 2`](../../src/nodes/node_2_world_model_hypothesis.py), [`Node 5`](../../src/nodes/node_5_skill_library.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Princeton Üniversitesi tarafından bilişsel bilimdeki SOAR ve ACT-R mimarilerinin modern dil modellerine uyarlandığı referans çerçevesidir. Dil ajanını sadece bir prompt döngüsü olarak değil; Çalışan (Working), Epizodik (Episodic), Anlamsal (Semantic) ve Prosedürel (Procedural) olmak üzere 4 temel bellek katmanı ve karar döngüsüyle tanımlar.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL'in temel mimari iskeleti doğrudan CoALA spesifikasyonuna dayanır:
- Çalışan Bellek: Modelin o anki prompt alanı ve KV önbelleği (4K sınırında).
- Epizodik Bellek: `logs/` altında saklanan geçmiş hata izleri ve operasyon kütükleri.
- Anlamsal Bellek: Sunucu erişim envanteri ve konfigürasyon kuralları.
- Prosedürel Bellek: `.skills/` dizini altındaki Python ve Shell araçları.

## 3. Taslak Uygulama ve Mimari Mantık
Sistem spagetti kodlar yerine CoALA bellek katmanları üzerinden modüler olarak organize edilir; karar döngüsü (Planlama -> Seçim -> İcra -> Öğrenme) deterministik bir state machine olarak işletilir.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Bellek katmanları arasındaki veri akışı kesin JSON şemalarıyla doğrulanmalı; katmanlar arası veri kirliliği önlenmelidir.
