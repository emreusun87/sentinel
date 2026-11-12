# Çalışma Notu #11 — Self-Rewarding Language Models - arXiv:2401.10020

- **Kategori:** Test Anı Akıl Yürütme (Test-Time Compute)
- **Kaynak / Makale:** [Yerel PDF (`11_Self_Rewarding_Language_Models.pdf`)](../../papers/11_Self_Rewarding_Language_Models.pdf) | [arXiv Kaynağı](https://arxiv.org/abs/2401.10020)
- **İlgili SENTINEL Düğümleri:** [`Node 4`](../../src/nodes/node_4_sandbox_verifier.py), [`Node 6`](../../src/nodes/node_6_meta_evaluator.py)

---

## 1. Makalenin Özeti ve Temel Fikri
İnsan geri bildirimine dayalı takviyeli öğrenme (RLHF) darboğazını aşmak için modelin hem yanıt üretici hem de bu yanıtları nesnel kriterlere göre puanlayan bir yargıç (LLM-as-a-Judge) olarak konumlandırılmasıdır. Model iteratif olarak kendi çıktılarını değerlendirerek iki rolünü de eşzamanlı olarak geliştirir.

## 2. SENTINEL Projesindeki Olası Kullanımı ve Mimari Entegrasyon
Yerel ortamlarda her komut için kullanıcı onayı almak otonom çalışma prensibini bozar.
SENTINEL karar aşamasında kendi eylem planını nesnel kurallarla puanlayacak:
- Güvenlik kriterleri (veri kaybı riski, parola sızıntısı, kesinti ihtimali).
- Modelin kendi verdiği puan belirlenen eşiğin (örn: 4/5) altındaysa plan doğrudan yürütülmez; model planı düzeltene kadar içsel revizyon döngüsüne girer.

## 3. Taslak Uygulama ve Mimari Mantık
```python
def self_evaluate_action_plan(plan, safety_rubric):
    eval_prompt = f"""
    Asagidaki aksiyon planini verilen guvenlik rubrigine gore 1-5 arasi puanla:
    Rubrik: {safety_rubric}
    Plan: {plan}
    Cikti: PUAN: X | GEREKCE: ...
    """
    score_text = core_slm.generate(eval_prompt)
    score = extract_score(score_text)
    return score >= 4, score_text
```

## 4. Teknik Kısıtlar ve Dikkat Edilecek Noktalar
- Modelin kendi hatalarını görmezden gelme (self-enhancement bias) eğilimine karşı rubrik maddeleri kesin ve ikili (var/yok) mantıkla netleştirilmelidir.
