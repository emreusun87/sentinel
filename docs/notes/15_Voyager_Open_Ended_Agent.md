# Çalışma Notu #15 — Voyager: An Open-Ended Embodied Agent - arXiv:2305.16291

- **Kategori:** Öz-Yinelemeli Gelişim (RSI) ve Ajan Evrimi
- **Kaynak / Makale:** [Yerel PDF (`15_Voyager_Open_Ended_Agent.pdf`)](../../papers/15_Voyager_Open_Ended_Agent.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2305.16291)
- **İlgili SENTINEL Düğümleri:** [`Node 0`](../../src/nodes/node_0_autotelic_task_generator.py), [`Node 3`](../../src/nodes/node_3_autonomous_tool_acquisition_rsi.py), [`Node 5`](../../src/nodes/node_5_skill_library.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Minecraft ortamında insan müdahalesi olmadan sıfırdan araç ve teknoloji keşfeden otonom ajan. Başarısı üç temel sütuna dayanır: Merak odaklı otomatik müfredat, çalıştırılabilir kodlardan oluşan yinelemeli Beceri Kütüphanesi (Skill Library) ve çevreden gelen hata geri bildirimleriyle kendini düzelten icra mekanizması.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
Voyager'ın "Beceri Kütüphanesi" yaklaşımı SENTINEL'in kalıcı hafızasını oluşturur.
SENTINEL bir sunucuda "MySQL slow log analizi" veya "Nginx worker optimizasyonu" için yeni bir Python fonksiyonu kodlayıp doğruladığında, bunu metin olarak bırakmaz. Fonksiyonu `sentinel/skills/` dizinine bağımsız bir modül olarak kaydeder.
Benzer bir problem geldiğinde sıfırdan düşünmez; kütüphanedeki hazır aracı çağırarak hızlıca icra eder.

## 3. Taslak Uygulama ve Mimari Mantık
- Yeni beceri sentezlendi -> Sandbox birim testinden geçti -> `sentinel/skills/{skill_name}.py` olarak kaydedildi -> Gelecekteki görevlerde doğrudan tool tanımı olarak sunuldu.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Kütüphanedeki fonksiyon sayısı arttıkça modelin doğru aracı seçebilmesi için her fonksiyonun başlığı ve parametre açıklaması (docstring) standartlaştırılmalıdır.
