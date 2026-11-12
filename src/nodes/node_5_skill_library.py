"""
SENTINEL MİMARİSİ // NODE 5: KALICI BELLEĞE KATMA VE PROSEDÜREL KÜTÜPHANE
================================================================================
Atıf Yapılan Node: [SkillLib] - Kalıcı Belleğe Katma & Prosedürel Bellek
Görevi: Sandbox testinden tam not alan araçları genel yetenek kütüphanesine
(`.skills/` veya `sentinel/skills/`) kalıcı olarak kaydetmek, semantik indeksini
çıkarmak ve gelecekteki görevlerde rutin icra (Exploit) için hazır hale getirmek.
================================================================================
"""

import os
import json

class SkillLibraryManager:
    def __init__(self, skills_dir="sentinel/skills"):
        self.skills_dir = skills_dir
        os.makedirs(self.skills_dir, exist_ok=True)
        self.index_path = os.path.join(self.skills_dir, "skills_index.json")
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_path):
            with open(self.index_path, "r", encoding="utf-8") as f:
                self.index = json.load(f)
        else:
            self.index = {}

    def _save_index(self):
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def commit_new_skill(self, tool_name: str, tool_code: str, hypothesis: dict) -> str:
        """
        Doğrulanmış yeni kodu kalıcı depoya yazar ve anlamsal indeksini günceller.
        """
        file_path = os.path.join(self.skills_dir, tool_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(tool_code)

        capability_name = hypothesis.get("required_capability", tool_name)
        self.index[capability_name] = {
            "file": tool_name,
            "description": hypothesis.get("root_cause_hypothesis", ""),
            "keywords": hypothesis.get("search_keywords", []),
            "version": 1
        }
        self._save_index()
        print(f"[NODE-5] Yeni Yetenek Kalıcı Kütüphaneye Eklendi: {capability_name} -> {file_path}")
        return file_path

    def find_best_match(self, task_query: str) -> tuple:
        """
        Mevcut kütüphanede sorguyla örtüşen araç arar.
        """
        task_query_lower = task_query.lower()
        for cap_name, meta in self.index.items():
            if cap_name.lower() in task_query_lower or any(kw in task_query_lower for kw in meta.get("keywords", [])):
                return True, meta["file"], 0.95
        return False, None, 0.1

