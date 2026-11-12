# Çalışma Notu #08 — ADAS (Ajan Sistemlerinin Otomatik Tasarımı) - arXiv:2408.08435

- **Kategori:** Öz-Yinelemeli Gelişim (RSI) ve Ajan Evrimi
- **Kaynak / Makale:** [Yerel PDF (`08_ADAS_Automated_Design_Agentic_Systems.pdf`)](../../papers/08_ADAS_Automated_Design_Agentic_Systems.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2408.08435)
- **İlgili SENTINEL Düğümleri:** [`Node 3`](../../src/nodes/node_3_autonomous_tool_acquisition_rsi.py), [`Node 7`](../../src/nodes/node_7_metacognitive_recompiler.py)

---

## 1. Makalenin Özeti ve Temel Fikri
İnsan mühendislerin elle sabit alt-ajan iş akışları (ReAct, Reflexion vb.) kurgulaması yerine, bir "Meta-Ajan"ın problemin yapısına göre çalışma zamanında yeni alt-ajan topolojileri, haberleşme grafikleri ve işbirlikleri kodlamasını sağlayan araştırma. Üretilen mimariler test edilir ve başarılı olanlar mimari arşivine kaydedilir.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
Sistem analizlerinde tek bir ajan mimarisi her probleme uymaz. Basit bir dosya izin kontrolü için çoklu ajan zinciri kurmak gereksiz CPU tüketirken; çok sunuculu bir senkronizasyon analizinde tekil ajan yetersiz kalır.
ADAS yaklaşımıyla SENTINEL bünyesinde hafif bir `MetaOrchestrator` bulunduracağız:
- Problem karmaşıklığı analiz edilir.
- Gerektiğinde çalışma anında yönlü çizge (DAG) tabanlı bir alt-ajan ekibi derlenir (örn: `prober` -> `trace_analyzer` -> `report_builder`).
- İşlem tamamlandığında bu başarılı topoloji şablonu gelecekteki benzer durumlar için saklanır.

## 3. Taslak Uygulama ve Mimari Mantık
- Görev: "Çok katmanlı kimlik doğrulama darboğazı".
- Meta-Ajan çıktısı: 2 adet alt-ajan kodu ve aralarındaki JSON haberleşme şeması.
- Yürütme: Alt-ajanlar hafif bellek profiliyle çalıştırılıp özet veriler birleştiriciye aktarılır.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- CPU üzerinde çok sayıda eşzamanlı ajan çalıştırmak bellek darboğazına yol açar; bu nedenle alt-ajanlar paralel değil, sıralı DAG akışında çalıştırılmalıdır.
