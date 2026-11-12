"""
SENTINEL MİMARİSİ // NODE 0: OTONOM İÇSEL GÖREV VE MERAK MOTORU
================================================================================
Atıf Yapılan Node: [AutotelicEngine] - Otonom İçsel Görev ve Merak Motoru
Görevi: Dışarıdan kullanıcı girdisi gelmediğinde (Idle / Boşta durumu), sistemin
kendi bilişsel derinliğini artırmak, kör noktalarını tespit etmek ve yetenek
uzayını genişletmek amacıyla kendi kendine görevler (Self-Generated Tasks) üretmesi.
================================================================================
"""

import time
import json
import random

class AutotelicTaskGenerator:
    def __init__(self, core_slm, memory_bank):
        self.slm = core_slm
        self.memory = memory_bank
        self.idle_threshold_seconds = 30
        self.last_user_activity = time.time()

    def notify_user_activity(self):
        """Kullanıcı girdiğinde sayacı sıfırlar."""
        self.last_user_activity = time.time()

    def is_idle(self) -> bool:
        return (time.time() - self.last_user_activity) > self.idle_threshold_seconds

    def generate_intrinsic_curiosity_task(self) -> dict:
        """
        Model, geçmiş başarısızlık ve zayıf güven kütüklerini tarayarak
        kendi yetenek sınırında (Zone of Proximal Development) bir meydan okuma üretir.
        """
        # Hafızadaki en zayıf yetenek veya en sık hata alınan alanları bul
        weak_spots = self.memory.get_lowest_confidence_domains()
        
        prompt = f"""
        [İÇSEL MERAK VE ÖZ-GÖREV ÜRETİM DÖNGÜSÜ]
        Mevcut Bilişsel Zayıf Noktalar: {weak_spots}
        Görev: Sistem boşta modunda. SENTINEL'in sistem yönetimi, Linux çekirdeği,
        ağ teşhisi veya veritabanı optimizasyonu konusundaki kapasitesini sınayacak,
        uç senaryo (edge case) içeren, doğrulanabilir sentetik bir problem kurgula.
        
        Çıktı Formatı (JSON):
        {{
            "task_id": "auto_task_xxx",
            "domain": "Linux Kernel / MySQL / Network",
            "challenge": "Problemin teknik tanımı",
            "verification_metric": "Başarının doğrulanacağı bash/python kriteri",
            "difficulty": 1-5
        }}
        """
        task_json_str = self.slm.generate(prompt, temperature=0.7)
        task_data = json.loads(task_json_str)
        task_data["source"] = "INTRINSIC_CURIOSITY_ENGINE"
        task_data["priority"] = "LOW_BACKGROUND"
        return task_data

    def run_idle_step(self):
        if self.is_idle():
            print("[NODE-0] Sistem boşta. Otonom içsel görev üretiliyor...")
            new_task = self.generate_intrinsic_curiosity_task()
            print(f"[NODE-0] Yeni Görev Üretildi: {new_task['challenge']}")
            return new_task
        return None

