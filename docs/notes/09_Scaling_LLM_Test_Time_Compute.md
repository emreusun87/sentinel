# Çalışma Notu #09 — Scaling Test-Time Compute Optimally - arXiv:2408.03314

- **Kategori:** Test Anı Akıl Yürütme (Test-Time Compute)
- **Kaynak / Makale:** [Yerel PDF (`09_Scaling_LLM_Test_Time_Compute.pdf`)](../../papers/09_Scaling_LLM_Test_Time_Compute.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2408.03314)
- **İlgili SENTINEL Düğümleri:** [`Node 1`](../../src/nodes/node_1_metacognitive_controller.py), [`Node 4`](../../src/nodes/node_4_sandbox_verifier.py)

---

## 1. Makalenin Özeti ve Temel Fikri
Test anında arama ve doğrulama bütçesini (Test-Time Compute) optimal ölçeklemenin, model parametrelerini katlarca büyütmekten çok daha etkili olduğunu matematiksel ve deneysel olarak kanıtlayan çalışma. Küçük bir modelle üretilen birden fazla aday çözümün (Best-of-N, Beam Search) bir doğrulayıcı (verifier) eşliğinde puanlanıp seçilmesi, çok daha büyük modellerin doğrudan yanıtlarından daha yüksek başarı oranı sunabilmektedir.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
SENTINEL'in CPU odaklı varoluş stratejisinin en sağlam dayanağıdır.
CPU üzerinde 70B'lik bir modelle çıkarım yapmaya çalışmak yerine; 2B veya 7B'lik kuantize bir modelle 3-4 farklı çözüm planı üretilip, bunlar yerel doğrulama kurallarıyla puanlanacak ve en tutarlı olan seçilecektir.
Böylece donanım masrafına girmeden yüksek doğruluklu kararlar alınabilir.

## 3. Taslak Uygulama ve Mimari Mantık
```python
def select_best_diagnostic_path(issue_context, n_samples=3):
    candidates = []
    for _ in range(n_samples):
        plan = core_slm.generate(issue_context, temperature=0.6)
        candidates.append(plan)

    scored_candidates = []
    for plan in candidates:
        score = evaluate_plan_heuristics(plan) # Geri alma adimi, guvenlik, format kontrolu
        scored_candidates.append((score, plan))

    # En yüksek puanlı planı yürütmeye gönder
    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    return scored_candidates[0][1]
```

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Aday sayısı (N) CPU çekirdek sayısı ve zaman kısıtı dikkate alınarak dengelenmelidir (N=3 genellikle hız-doğruluk dengesini sağlar).
