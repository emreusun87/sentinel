# Çalışma Notu #04 — A-MEM (Ajan Tabanlı Dinamik Bellek Mimarisi) - arXiv:2502.12110

- **Kategori:** Bilişsel Mimari ve Bellek Hiyerarşisi
- **Kaynak / Makale:** [Yerel PDF (`04_A_MEM_Agentic_Memory.pdf`)](../../papers/04_A_MEM_Agentic_Memory.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2502.12110)
- **İlgili SENTINEL Düğümleri:** [`Node 2`](../../src/nodes/node_2_world_model_hypothesis.py), [`Node 5`](../../src/nodes/node_5_skill_library.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Geleneksel vektör tabanlı RAG sistemleri pasif bir depolama mantığıyla çalışır ve arama anında bağlam penceresini gereksiz veri yığınlarıyla doldurur. A-MEM yaklaşımında ise bellek aktif, kendi kendini organize eden bir yapı olarak ele alınır. Yeni bir tecrübe edinildiğinde sistem; mevcut anılarla bağlantı kurar (Link), çelişen bilgileri günceller (Update), güncelliğini yitirmiş detayları eler (Prune) ve birden fazla gözlemden tekil nedensel kurallar soyutlar (Consolidate).

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
Sunucu teşhislerinde yüzlerce satırlık ham telemetri ve log çıktısı üretilir. Bu çıktıların tamamını bağlam penceresine yüklemek CPU tabanlı modelin çıkarım hızını ciddi şekilde düşürür.
A-MEM prensibi doğrultusunda SENTINEL'de `MemoryConsolidator` katmanı oluşturulacak:
- Okunan log analiz edilecek ("Örn: Apache process havuzunun dolması sebebiyle 502 hatası oluştu").
- Bu analiz tek cümlelik bir kural olarak soyutlanıp SQLite tablosuna yazılacak.
- Ham loglar diskten temizlenecek; bir sonraki oturumda sadece soyutlanmış kural bağlama alınacak.

## 3. Taslak Uygulama ve Mimari Mantık
```python
def consolidate_execution_memory(task_id, raw_output, status):
    # Ham çıktıyı tek cümlelik nedensel ilkeye dönüştür
    rule = core_slm.summarize(
        f"Gorev: {task_id}\nCikti: {raw_output[:400]}\nDurum: {status}\n"
        f"Gelecek oturumlar icin tek satirlik sistem prensibi cikar:"
    )
    # Benzer kayıtlarla karşılaştır ve gerekirse birleştir
    existing_rules = query_similar_rules(rule)
    if existing_rules:
        merged_rule = core_slm.merge(existing_rules, rule)
        update_rule_in_db(existing_rules[0].id, merged_rule)
    else:
        insert_rule_to_db(task_id, rule)
```

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Konsolidasyon işleminin kendisi de model çağrısı gerektirdiğinden, işlem her komuttan sonra değil, yalnızca kritik teşhisler ve oturum sonlarında çalıştırılmalıdır.
