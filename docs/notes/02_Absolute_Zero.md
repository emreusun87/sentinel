# Çalışma Notu #02 — Absolute Zero (Sıfır Veriyle Self-Play Akıl Yürütme) - arXiv:2505.03335

- **Kategori:** Öz-Yinelemeli Gelişim (RSI) ve Ajan Evrimi
- **Kaynak / Makale:** [Yerel PDF (`02_Absolute_Zero.pdf`)](../../papers/02_Absolute_Zero.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2505.03335)
- **İlgili SENTINEL Düğümleri:** [`Node 0`](../../src/nodes/node_0_autotelic_task_generator.py), [`Node 4`](../../src/nodes/node_4_sandbox_verifier.py)

---

## 1. Makalenin Özeti ve Temel Fikri
AlphaZero'nun satranç ve Go alanında insan verisi kullanmaksızın kendi kendine oynayarak üst düzey seviyeye ulaşması mantığı, dil modellerinin akıl yürütme (reasoning) süreçlerine uyarlanmış. Dışarıdan derlenmiş soru-cevap veri setlerine ihtiyaç duymadan; sistem "Problem Üretici (Proposer)" ve "Problem Çözücü (Solver)" rollerine ayrılarak kendi kendine etkileşim kuruyor. Matematik ve programlama gibi alanlarda çıktı doğrudan Python REPL veya derleyici ile test edilebildiği için, sistem dış denetim olmadan kendi mantık zincirini güçlendirebiliyor.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL kapalı devre (air-gapped) kurumsal ortamlarda çalışacağı için sürekli harici veri beslemesi alamayacak. Sistemin boşta kaldığı (idle) zaman aralıklarında CPU kaynaklarını kullanarak kendi kendine problem üretip çözmesini sağlayabiliriz.
Örneğin Linux sistem yönetimi, SQL optimizasyonu ve Regex alanlarında sentetik teşhis senaryoları üretilip model tarafından çözülebilir; doğrulanan başarılı düşünce zincirleri yerel anlamsal belleğe eklenir.

## 3. Taslak Uygulama ve Mimari Mantık
- Sistem yükü %20'nin altına düştüğünde arka plan servisi tetiklenir (`sentinel_idle_daemon.py`).
- Model, bilinen sistem kurallarına göre zorlu bir senaryo kurgular (örn. "MySQL kilitlenme analizi için bash betiği").
- Ardından aynı model çözücü modunda bu problemi çözmeyi dener.
- Üretilen betik Python subprocess sandbox'ında yürütülüp doğrulanırsa, çözüm şablonu kalıcı bilgi bankasına işlenir.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Modelin önemsiz veya kolay sorular üreterek ödül fonksiyonunu yanıltması (reward hacking) engellenmeli; soru zorluk derecesi kademeli olarak artırılmalıdır.
- CPU kaynaklarının aşırı tüketilmemesi için arka plan süreci en düşük işletim sistemi önceliği (`nice -n 19` / `IDLE_PRIORITY_CLASS`) ile çalıştırılmalıdır.
