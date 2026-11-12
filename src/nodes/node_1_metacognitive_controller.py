"""
SENTINEL MİMARİSİ // NODE 1: ÜST-BİLİŞSEL DENETLEYİCİ
================================================================================
Atıf Yapılan Node: [MetaCtrl] - 1. Üst-Bilişsel Denetleyici (Metacognitive Controller)
Görevi: Gelen görevi (dışarıdan veya içsel merak motorundan) epistemik belirsizlik
açısından analiz etmek, mevcut yetenek kütüphanesini taramak ve "Rutin İcra" mı
yoksa "Keşif ve Araç Sentezi" mi kararı vermek.
================================================================================
"""

import math

class MetacognitiveController:
    def __init__(self, core_slm, skill_registry, uncertainty_threshold=0.35):
        self.slm = core_slm
        self.skills = skill_registry
        self.epsilon = uncertainty_threshold  # Epistemik belirsizlik eşik değeri

    def measure_epistemic_uncertainty(self, task: dict) -> float:
        """
        Görevin mevcut dünya modeli altındaki Shannon entropisini / belirsizliğini hesaplar.
        Modelin token olasılık dağılımı ve hafıza benzerlik skoru üzerinden ölçülür.
        """
        task_text = task.get("challenge", str(task))
        
        # 1. Mevcut beceri kütüphanesinde doğrudan eşleşen araç var mı?
        has_skill, skill_name, match_score = self.skills.find_best_match(task_text)
        if has_skill and match_score > 0.85:
            return 0.05  # Neredeyse sıfır belirsizlik (Bildiğimiz alan)

        # 2. SLM logit entropisi tahmini
        entropy_estimate = self.slm.estimate_output_entropy(task_text)
        
        # 3. Bileşik belirsizlik skoru: H(Y | g, W_t)
        epistemic_uncertainty = (1.0 - match_score) * 0.6 + entropy_estimate * 0.4
        return epistemic_uncertainty

    def decide_cognitive_path(self, task: dict) -> str:
        """
        Karar Kuralı:
        Action(g) = Exploit(S_t)      eğer H <= epsilon
        Action(g) = Explore(W_t)      eğer H > epsilon
        """
        uncertainty = self.measure_epistemic_uncertainty(task)
        print(f"[NODE-1] Görev: {task.get('task_id', 'anon')} | Epistemik Belirsizlik: {uncertainty:.3f} | Eşik: {self.epsilon}")

        if uncertainty <= self.epsilon:
            print("[NODE-1] -> Karar: RUTİN İCRA (Exploit) - Hazır beceri çağrılıyor.")
            return "ROUTE_ROUTINE_EXPLOIT"
        else:
            print("[NODE-1] -> Karar: DÜNYA MODELİ VE KEŞİF (Explore) - Bilgi/araç eksikliği tespit edildi.")
            return "ROUTE_EXPLORE_AND_SYNTHESIZE"

