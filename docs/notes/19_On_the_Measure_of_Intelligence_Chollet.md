# Çalışma Notu #19 — On the Measure of Intelligence (Chollet AGI Metriği) - arXiv:1911.01547

- **Kategori:** Zeka Ölçümü, Felsefe ve İnsan-YZ Simbiyozu
- **Kaynak / Makale:** [Yerel PDF (`19_On_the_Measure_of_Intelligence_Chollet.pdf`)](../../papers/19_On_the_Measure_of_Intelligence_Chollet.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/1911.01547)
- **İlgili SENTINEL Düğümleri:** [`Node 0`](../../src/nodes/node_0_autotelic_task_generator.py), [`Node 3`](../../src/nodes/node_3_autonomous_tool_acquisition_rsi.py)

---

## 1. Makalenin Özeti ve Temel Fikri
François Chollet'in yapay zekanın ezber yeteneğiyle değil, genelleme ve yeni beceri edinme verimliliğiyle ölçülmesi gerektiğini savunduğu temel referans manifestosu.
Chollet'e göre zeka: "Bir sistemin daha önce hiç karşılaşmadığı durumlarda; minimum ön-bilgi, minimum veri ve minimum hesaplama kaynağı harcayarak yeni bir beceriyi ne kadar hızlı edinebildiğinin (Skill-Acquisition Efficiency) ölçüsüdür."

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL mimarisinin varoluş felsefesi ve başarı metriği doğrudan bu tanıma dayanır.
Projemizde zekayı modelin parametre sayısı ile değil; birim CPU maliyeti ve model boyutu başına sisteme kazandırdığı yeni doğrulanmış yetenek miktarı ile ölçüyoruz:
$$\mathcal{I}_{\text{SENTINEL}} = \frac{\Delta \mathcal{S}}{\log(C_{\text{CPU}}) \cdot |\theta_{\text{quant}}|}$$
Kısıtlı CPU donanımında çalışan 2B'lik bir kuantize model, bilinmeyen bir sistem krizinde kendi aracını yazıp problemi başarıyla çözebiliyorsa; statik bir trilyon parametreli modelden çok daha yüksek bir zeka verimliliğine sahiptir.

## 3. Taslak Uygulama ve Mimari Mantık
- Sistemin benchmark değerlendirmesi sabit soru setleriyle değil; daha önce görmediği yeni sunucu senaryolarında kendi başına araç kodlayıp problemi çözme başarısıyla yapılacaktır.

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Test senaryolarının modelin eğitim verisinde bulunmayan özgün ortam ve araç kombinasyonlarından seçilmesi zorunludur.
