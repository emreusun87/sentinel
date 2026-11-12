"""
SENTINEL MİMARİSİ // NODE 6: NEDENSEL DERS VE META-DEĞERLENDİRME
================================================================================
Atıf Yapılan Node: [MetaEval] - 4. Nedensel Ders & Meta-Değerlendirme
Görevi: Doğrulama başarısız olduğunda hatanın kaynağını ayrıştırmak:
- Hata yazılan araç kodundan mı kaynaklandı? -> [1. Derece RSI: Aracı Düzelt]
- Hata üst-bilişsel stratejiden, belirsizlik eşiğinden veya hipotez modelinden mi?
  -> [2. Derece RSI: Denetleyiciyi Yeniden Derle]
================================================================================
"""

class MetaEvaluator:
    def __init__(self, core_slm, max_tool_retries=2):
        self.slm = core_slm
        self.max_retries = max_tool_retries
        self.retry_counts = {}

    def evaluate_failure_source(self, task: dict, tool_name: str, sandbox_result: dict, meta_history: list) -> str:
        """
        Başarısızlığı iki seviyede sınıflandırır:
        1. LOCAL_TOOL_FAILURE: Araç kodunda spesifik sentaks/lojik hatası var.
        2. METACOGNITIVE_BIAS_FAILURE: Üst-bilişsel denetleyici yanlış hipotez kurdu
           veya belirsizlik eşiğini yanlış kalibre etti.
        """
        error_msg = sandbox_result.get("error", "")
        current_retries = self.retry_counts.get(tool_name, 0)

        # Eğer araç 2 defadan az denendiyse ve hata basit bir python istisnasıysa
        if current_retries < self.max_retries and sandbox_result.get("stage") in ["AST_VALIDATION", "RUNTIME_EXECUTION"]:
            self.retry_counts[tool_name] = current_retries + 1
            print(f"[NODE-6] Teşhis: Lokal Araç Hatası (Deneme {self.retry_counts[tool_name]}/{self.max_retries}). 1. Derece RSI tetikleniyor.")
            return "TRIGGER_1ST_DEGREE_RSI_TOOL_REVISION"

        # Eğer arka arkaya 3 görevde belirsizlik tahmini tutmadıysa veya araç defalarca patladıysa
        print("[NODE-6] Teşhis: Üst-Bilişsel Karar Sapması (Metacognitive Systematic Bias). 2. Derece RSI tetikleniyor.")
        return "TRIGGER_2ND_DEGREE_RSI_RECOMPILE_CONTROLLER"

    def record_causal_lesson(self, task: dict, failure_reason: str):
        """Epizodik belleğe gelecekte aynı hataya düşmemek için nedensel kural yazar."""
        print(f"[NODE-6] Epizodik Belleğe Nedensel Ders Yazıldı: {failure_reason}")

