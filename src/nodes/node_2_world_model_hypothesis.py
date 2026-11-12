"""
SENTINEL MİMARİSİ // NODE 2: DÜNYA MODELİ VE HİPOTEZ ÜRETİMİ
================================================================================
Atıf Yapılan Node: [WorldModel] - 2. Dünya Modeli & Hipotez Üretimi
Görevi: Bilinmeyen veya belirsizliği yüksek durumlarda doğrudan körlemesine
komut çalıştırmak yerine; çevre durumunu (OS telemetrisi, prosesler, loglar)
gözlemleyerek nedensel bir teşhis hipotezi (Causal Hypothesis) kurmak.
================================================================================
"""

import subprocess
import json

class WorldModelHypothesisEngine:
    def __init__(self, core_slm, telemetry_harvester):
        self.slm = core_slm
        self.harvester = telemetry_harvester

    def observe_environment_state(self) -> dict:
        """
        Sistem ortamından salt-okunur telemetri toplar (CPU, RAM, açık portlar, slow logs).
        """
        telemetry = {
            "top_processes": self.harvester.get_top_cpu_processes(limit=5),
            "disk_io": self.harvester.get_io_wait_stat(),
            "active_sockets": self.harvester.get_listening_ports(),
            "recent_kernel_errors": self.harvester.get_dmesg_errors(tail=10)
        }
        return telemetry

    def formulate_causal_hypothesis(self, task: dict, telemetry: dict) -> dict:
        """
        Telemetriyi ve görevi birleştirerek 'Nedensel Hipotez' ve 'Gerekli Araç İhtiyacı' üretir.
        """
        prompt = f"""
        [DÜNYA MODELİ VE NEDENSEL HİPOTEZ KURMA]
        Görev: {task.get('challenge')}
        Gözlemlenen Sistem Telemetrisi:
        {json.dumps(telemetry, indent=2)}

        Soru 1: Bu problemin olası kök nedeni nedir? (Nedensel Teşhis)
        Soru 2: Bunu çözmek için hangi araç veya yetenek eksiktir?
        Soru 3: Eksik araç için arama kriterleri (GitHub/Web/Python) ne olmalıdır?

        Format:
        {{
            "root_cause_hypothesis": "Açıklama...",
            "required_capability": "Eksik yetenek adı",
            "search_keywords": ["anahtar1", "anahtar2"],
            "test_acceptance_criteria": "Hangi komut çıktısı hipotezi doğrular?"
        }}
        """
        response_json = self.slm.generate(prompt)
        hypothesis = json.loads(response_json)
        print(f"[NODE-2] Kurulan Hipotez: {hypothesis['root_cause_hypothesis']}")
        print(f"[NODE-2] İhtiyaç Duyulan Yetenek: {hypothesis['required_capability']}")
        return hypothesis

