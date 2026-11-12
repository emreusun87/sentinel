# Çalışma Notu #13 — MemGPT: Towards LLMs as Operating Systems - arXiv:2310.08560

- **Kategori:** Bilişsel Mimari ve Bellek Hiyerarşisi
- **Kaynak / Makale:** [Yerel PDF (`13_MemGPT_LLM_OS.pdf`)](../../papers/13_MemGPT_LLM_OS.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2310.08560)
- **İlgili SENTINEL Düğümleri:** [`Node 2`](../../src/nodes/node_2_world_model_hypothesis.py), [`Node 5`](../../src/nodes/node_5_skill_library.py)

---

## 1. Makalenin Özeti ve Temel Fikri
İşletim sistemlerindeki sanal bellek (Virtual Memory) ve sayfalama (paging) hiyerarşisini doğrudan LLM bağlam penceresine uyarlayan mimari. LLM bağlamı "RAM", harici SQLite ve vektör depoları "Disk Depolama" olarak kurgulanır. Model sayfa taşıma çağrılarıyla (`page_in`, `page_out`) ne zaman eski veriyi diske boşaltacağına ve ne zaman eski veriyi bağlama alacağına kendisi karar verir.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
CPU üzerinde bağlam penceresini 4.096 tokenın üzerine çıkarmak KV-cache şişmesine ve çıkarım hızının ciddi şekilde düşmesine yol açar.
MemGPT mimarisi sayesinde aktif bağlamı 4K tokenla sınırlandırıp, geçmiş telemetri kütüklerini SQLite tablosunda tutacağız. Model geçmiş bir sunucu hatasına ihtiyaç duyduğunda `search_archival_memory` fonksiyon çağrısıyla o veriyi sayfalar halinde bağlamına alacaktır.

## 3. Taslak Uygulama ve Mimari Mantık
```
[SENTINEL Aktif Bağlam (4K Token - RAM)]
       ▲                             │
       │ page_in (Sorgu ile yükle)   │ page_out (Eski logu tahliye et)
       │                             ▼
[SQLite & Yerel İndeks (Arşiv Belleği - Disk)]
```

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Modelin her adımda gereksiz sayfalama çağrısı yapmasını engellemek için sistem promptunda arşiv arama kuralları net tanımlanmalıdır.
