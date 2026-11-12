"""
SENTINEL MİMARİSİ // NODE 3: OTONOM ARAÇ VE YETENEK EDİNME (1. DERECE RSI)
================================================================================
Atıf Yapılan Node: [ToolAcquisitionRSI] - 3. Otonom Araç ve Yetenek Edinme RSI
Görevi: Hipotezin gerektirdiği eksik aracı sıfırdan Python ile kodlamak ya da
dış kaynakları (GitHub API, yerel dökümantasyon, web arama sonuçları) otonom tarayarak
açık kaynaklı çözümleri bulmak, uyarlamak ve doğrulanabilir araca dönüştürmek (Tool Foraging RSI).
================================================================================
"""

import json
import urllib.request
import urllib.parse

class AutonomousToolAcquisitionRSI:
    def __init__(self, core_slm, search_adapter=None, github_client=None):
        self.slm = core_slm
        self.search = search_adapter
        self.github = github_client

    def forage_external_knowledge(self, search_keywords: list) -> list:
        """
        GitHub ve Web üzerinde anahtar kelimelerle arama yaparak
        örnek scriptleri, API spesifikasyonlarını veya açık kaynak kütüphaneleri toplar.
        """
        snippets = []
        query = " ".join(search_keywords)
        print(f"[NODE-3] Açık kaynak ve repo araması yapılıyor: '{query}'...")
        
        # 1. Simüle veya canlı GitHub / Web araması
        search_hits = self.search.query_technical_sources(query, sources=["github", "docs", "stackoverflow"])
        for hit in search_hits[:3]:
            snippets.append({
                "source": hit["url"],
                "content_snippet": hit["code_or_text"][:800]
            })
        return snippets

    def synthesize_tool_code(self, hypothesis: dict, external_snippets: list) -> str:
        """
        Toplanan dış kod parçalarını ve hipotezi kullanarak
        SENTINEL ortamına tam uyumlu, izole çalışabilen bir Python aracı yazar.
        """
        prompt = f"""
        [1. DERECE RSI - OTONOM ARAÇ SENTEZİ]
        Çözülecek Problem: {hypothesis.get('root_cause_hypothesis')}
        Gerekli Yetenek: {hypothesis.get('required_capability')}
        Toplanan Dış Kaynak Kod Parçaları:
        {json.dumps(external_snippets, indent=2)}
        
        Kriterler:
        - Standart Python 3 kütüphanelerini kullan (harici ağır bağımlılık ekleme).
        - CLI argümanı veya bağımsız çalıştırılabilir 'run_diagnostic()' fonksiyonu içersin.
        - Çıktıyı deterministik JSON olarak dönsün: {{"status": "OK/FAIL", "metrics": {{...}}, "recommendation": "..."}}
        - Sadece geçerli Python kodu üret, ekstra markdown açıklaması yazma.
        """
        synthesized_code = self.slm.generate(prompt, temperature=0.2)
        print(f"[NODE-3] Yeni araç kodu sentezlendi. Uzunluk: {len(synthesized_code)} karakter.")
        return synthesized_code

    def acquire_and_synthesize(self, hypothesis: dict) -> tuple:
        keywords = hypothesis.get("search_keywords", ["linux diagnostic script"])
        external_context = self.forage_external_knowledge(keywords)
        tool_code = self.synthesize_tool_code(hypothesis, external_context)
        tool_name = f"dyn_{hypothesis.get('required_capability', 'tool').lower().replace(' ', '_')}.py"
        return tool_name, tool_code

