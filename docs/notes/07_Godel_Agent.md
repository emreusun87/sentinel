# Çalışma Notu #07 — Gödel Agent (Öz-Gönderimli Ajan Mimarisi) - arXiv:2410.04444

- **Kategori:** Öz-Yinelemeli Gelişim (RSI) ve Ajan Evrimi
- **Kaynak / Makale:** [Yerel PDF (`07_Godel_Agent.pdf`)](../../papers/07_Godel_Agent.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2410.04444)
- **İlgili SENTINEL Düğümleri:** [`Node 3`](../../src/nodes/node_3_autonomous_tool_acquisition_rsi.py), [`Node 6`](../../src/nodes/node_6_meta_evaluator.py), [`Node 7`](../../src/nodes/node_7_metacognitive_recompiler.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Sabit araç setleri ve statik prompt şablonları yerine; çalışma zamanında (runtime) kendi karar mekanizmasını, promptlarını ve fonksiyon modüllerini inceleyip değiştirebilen öz-gönderimli (self-referential) ilk formal ajan çerçevesidir. Model karşılaştığı görevi çözemediğinde, dışarıdan müdahale beklemek yerine kendi kod yapısındaki mantıksal eksikliği tespit edip yeni bir araç fonksiyonu sentezleyerek sisteme dahil eder.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL'in Otonom Yetenek Sentezi (RSI) katmanının çift kademeli omurgasını bu mantık oluşturur:
1. **1. Kademe (Araç Seviyesi):** Sistem yeni bir servis türüyle (örn. özel bir proxy/cache) karşılaştığında `sentinel/skills/dynamic_tool_{id}.py` yazar, sandbox'ta test edip `importlib` ile dinamik yükler.
2. **2. Kademe (Üst-Biliş Seviyesi):** Ajan sadece araç yazmakla kalmaz; karar alma mantığında (araç seçimi, belirsizlik tespiti, planlama) kronik bir zafiyet fark ettiğinde bizzat `controller.py` modülünü yeniden kodlar, meta-testlerden geçirir ve çalışma anında kendi yönetim beynini yeniden derler (Metacognitive Self-Recompilation).

## 3. Taslak Uygulama ve Mimari Mantık
```python
import importlib

def integrate_dynamic_skill(skill_name, python_code):
    file_path = f"sentinel/skills/{skill_name}.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(python_code)

    # Modülü çalışma anında dinamik içeri al
    spec = importlib.util.spec_from_file_location(skill_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Ajanın yetenek sözlüğüne kaydet
    sentinel_tool_registry[skill_name] = module.execute
```

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Dinamik yüklenen kodların sistem genelinde tahribat yaratmaması için dosya yazma ve ağ erişimi izinleri katı güvenlik kurallarıyla sınırlandırılmalıdır.
