# Çalışma Notu #01 — Darwin Gödel Machine (DGM) - arXiv:2505.22954

- **Kategori:** Öz-Yinelemeli Gelişim (RSI) ve Ajan Evrimi
- **Kaynak / Makale:** [Yerel PDF (`01_Darwin_Godel_Machine.pdf`)](../../papers/01_Darwin_Godel_Machine.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2505.22954)
- **İlgili SENTINEL Düğümleri:** [`Node 4`](../../src/nodes/node_4_sandbox_verifier.py), [`Node 6`](../../src/nodes/node_6_meta_evaluator.py), [`Node 7`](../../src/nodes/node_7_metacognitive_recompiler.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Jürgen Schmidhuber'in klasik Gödel Machine yaklaşımı, sistemin kendi kaynak kodunu formel matematiksel kanıtlarla doğrulayarak güncellemesini öngörüyordu. Ancak karmaşık yazılım ortamlarında formel matematiksel kanıt üretmek pratikte imkansıza yakındır. Bu çalışmada yazarlar formel kanıt yerine Darwinci evrimsel arama ve ampirik test doğrulaması getirmişler. Model kendi ajan yürütme kodunu (Python seviyesinde) değiştiriyor; ardından oluşturulan mutasyon bir test/benchmark setinde koşturuluyor. Yeni kod eski sürümden daha yüksek performans gösterirse ana koda merge ediliyor, aksi halde iptal ediliyor.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
Bizim kısıtlı donanım şartlarımızda (yalnızca CPU, harici GPU yok) 2B-7B'lik kuantize küçük modellerle çalışıyoruz. Modeli sıfırdan eğitmek veya sürekli fine-tune etmek imkansız. Ancak DGM mantığıyla modelin sadece harici araçları değil, bizzat Üst-Bilişsel Denetleyiciyi (`controller.py`, `orchestrator.py`) çalışma zamanında yeniden derlemesini (2. Derece RSI) sağlayabiliriz.
Örneğin bir sunucu teşhisinde sistem sürekli yanlış belirsizlik kararı veriyor veya gereksiz döngülere giriyorsa, SENTINEL kendi üst-biliş denetim kodunu hata kayıtları ışığında revize eder; meta-benchmark testinden geçirip onaylarsa kendi karar mekanizmasını günceller.

## 3. Taslak Uygulama ve Mimari Mantık
```python
def execute_self_mutation_cycle(failure_trace, test_suite):
    with open("sentinel/orchestrator.py", "r", encoding="utf-8") as f:
        current_code = f.read()

    prompt = f"""
    Ajan orkestrasyonunda su hata meydana geldi:
    {failure_trace}
    Mevcut Kod:
    {current_code}
    Gorev: Kendi kodunu bu senaryoyu basariyla yonetecek sekilde revize et.
    Yalnizca gecerli Python kodu uret.
    """
    mutated_code = call_core_slm(prompt)

    # Guvenlik denetimi: AST uzerinden sentaks kontrolu
    if not validate_python_ast(mutated_code):
        return False

    # Izole sandbox ortaminda birim test dogrulamasi
    test_result = run_in_sandbox(mutated_code, test_suite)
    if test_result.is_superior:
        backup_current_version("sentinel/orchestrator.py")
        with open("sentinel/orchestrator.py", "w", encoding="utf-8") as f:
            f.write(mutated_code)
        return True
    return False
```

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Modelin ürettiği koddaki sözdizimi hatalarını engellemek için doğrudan çalıştırmadan önce `ast.parse` kontrolü zorunlu tutulmalıdır.
- Sonsuz döngü veya bellek sızıntısı riskine karşı sandbox ortamında mutlaka işlem zaman aşımı (timeout) ve maksimum RAM sınırı konulmalıdır.
