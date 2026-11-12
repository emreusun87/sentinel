"""
SENTINEL Redoc Portal Veri Senkronizasyon Betiği
================================================
`docs/architecture.md`, `docs/notes/*.md`, `src/nodes/*.py` ve `papers/*.pdf`
dosyalarını tarayarak 3-sütunlu Redoc portalı için `docs/assets/portal_data.json`
ve `docs/assets/portal_data.js` dosyalarını sıfır bağımlılıkla üretir.

Kullanım:
    python scripts/build_portal_index.py
"""

import ast
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(ROOT, "docs")
NOTES_DIR = os.path.join(DOCS_DIR, "notes")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")
NODES_DIR = os.path.join(ROOT, "src", "nodes")
PAPERS_DIR = os.path.join(ROOT, "papers")

os.makedirs(ASSETS_DIR, exist_ok=True)

NODE_SPECS = [
    {
        "id": "node-0",
        "num": 0,
        "mermaid_id": "AutotelicEngine",
        "short_title": "Node 0: İçsel Görev & Merak Motoru",
        "title": "0. Otonom İçsel Görev ve Merak Motoru (Autotelic Engine)",
        "badge": "AUTOTELIC",
        "file": "node_0_autotelic_task_generator.py",
        "formula_latex": r"g_{\text{auto}}^* = \arg\max_{g \in \mathcal{G}_{\text{cand}}} \Big[ H(Y \mid g, W_t) - \mathbb{E}_{o}\big[ H(Y \mid g, W_t \cup \{o\}) \big] \Big] - \lambda \cdot C_{\text{CPU}}(g)",
        "philosophy": "Spinoza'nın Conatus ilkesi ve Schmidhuber'in Sıkıştırma İlerlemesi (Compression Progress): Sistem dış uyaran olmadığında pasifleşmez; kendi zayıf güven bölgelerini tarayıp içsel amaç üretir.",
        "papers": ["02", "10", "15", "19"],
    },
    {
        "id": "node-1",
        "num": 1,
        "mermaid_id": "MetaCtrl",
        "short_title": "Node 1: Üst-Bilişsel Denetleyici",
        "title": "1. Üst-Bilişsel Denetleyici (Metacognitive Controller)",
        "badge": "CORE",
        "file": "node_1_metacognitive_controller.py",
        "formula_latex": r"\text{Action}(g) = \begin{cases} \text{Exploit}(\mathcal{S}_t), & H(Y \mid g, W_t) \le \epsilon_t \\ \text{Explore \& Forage}(W_t \to W_{t+1}), & H(Y \mid g, W_t) > \epsilon_t \end{cases}",
        "philosophy": "Epistemik tevazu ve Sokratik öz-farkındalık ('ne bilmediğini bilmek'): Halüsinasyonu önlemek için entropi eşiğini aşan durumlarda doğrudan yanıt üretmeyi durdurup keşif kipine geçer.",
        "papers": ["03", "05", "06", "09", "12", "14", "17", "20"],
    },
    {
        "id": "node-2",
        "num": 2,
        "mermaid_id": "WorldModel",
        "short_title": "Node 2: Dünya Modeli & Hipotez",
        "title": "2. Dünya Modeli ve Nedensel Hipotez Üretimi (World Model)",
        "badge": "CAUSAL",
        "file": "node_2_world_model_hypothesis.py",
        "formula_latex": r"W_{t+1} = \text{Update}(W_t, o_t), \quad h^* = \arg\max_{h \in \mathcal{H}} P(h \mid W_{t+1}, \mathcal{M}_{\text{episodic}})",
        "philosophy": "Peirce'ün Abdüktif Akıl Yürütmesi (Abductive Inference): Kör deneme-yanılma yerine sistem telemetrisinden sınanabilir nedensel kök neden hipotezi kurar.",
        "papers": ["04", "06", "13", "14", "18"],
    },
    {
        "id": "node-3",
        "num": 3,
        "mermaid_id": "ToolAcquisitionRSI",
        "short_title": "Node 3: Araç Edinme & Sentez (RSI-L1)",
        "title": "3. Otonom Araç Edinme ve Açık Kaynak Keşfi (1. Derece RSI / Tool Foraging)",
        "badge": "RSI-L1",
        "file": "node_3_autonomous_tool_acquisition_rsi.py",
        "formula_latex": r"s_{\text{cand}} = \Psi_{\text{SLM}}\big(h^*, W_t, \mathcal{K}_{\text{ext}}(\text{GitHub, Docs, Web})\big)",
        "philosophy": "Genişletilmiş Zihin (Extended Mind - Clark & Chalmers): Zeka yalnızca içsel ağırlıklarda değil, dış bilgi ekosistemlerini (GitHub, dokümantasyon) tarayıp araca dönüştürme yetisindedir.",
        "papers": ["07", "08", "10", "15", "19"],
    },
    {
        "id": "node-4",
        "num": 4,
        "mermaid_id": "SandboxVerify",
        "short_title": "Node 4: Deterministik Sandbox",
        "title": "4. Deterministik Doğrulama ve AST Güvenlik Sandbox'ı",
        "badge": "VERIFY",
        "file": "node_4_sandbox_verifier.py",
        "formula_latex": r"\text{Verify}(s_{\text{cand}}) = \mathbb{I}[\text{AST\_Safe}(s_{\text{cand}})] \cdot \mathbb{E}_{\text{sandbox}}[\text{Pass}(s_{\text{cand}})] > \tau",
        "philosophy": "Popper'ın Yanlışlanabilirlik İlkesi ve Simbiyotik Güvenlik Sınırı: Ampirik ve deterministik sandbox sınamasından geçmeyen hiçbir sentezlenmiş kod gerçek sisteme temas edemez.",
        "papers": ["01", "02", "09", "11", "20"],
    },
    {
        "id": "node-5",
        "num": 5,
        "mermaid_id": "SkillLib",
        "short_title": "Node 5: Beceri Kütüphanesi (.skills)",
        "title": "5. Kalıcı Belleğe Katma ve Prosedürel Kütüphane (Skill Crystallization)",
        "badge": "MEMORY",
        "file": "node_5_skill_library.py",
        "formula_latex": r"\mathcal{S}_{t+1} = \mathcal{S}_t \cup \{s_{\text{cand}}\}, \quad \mathcal{M}_{\text{sem}} \leftarrow \text{Crystallize}(\mathcal{M}_{\text{sem}}, s_{\text{cand}})",
        "philosophy": "Maturana & Varela'nın Autopoiesis (Öz-Üretim) kavramı: Doğrulanan her geçici çözüm, sistemin kalıcı bilişsel-prosedürel organına dönüşerek gelecekteki entropiyi düşürür.",
        "papers": ["04", "13", "14", "15", "18"],
    },
    {
        "id": "node-6",
        "num": 6,
        "mermaid_id": "MetaEval",
        "short_title": "Node 6: Nedensel Meta-Değerlendirme",
        "title": "6. Nedensel Ders Çıkarımı ve Kök Neden Ayrıştırması (Meta-Evaluator)",
        "badge": "EVAL",
        "file": "node_6_meta_evaluator.py",
        "formula_latex": r"\text{Route}(e_t) = \begin{cases} \text{RSI-L1 (Araç Revizyonu)}, & \text{Fault}(e_t) \in \mathcal{S}_{\text{op}} \\ \text{RSI-L2 (Öz-Derleme)}, & \text{Fault}(e_t) \in \mathcal{M}_{\text{ctrl}} \end{cases}",
        "philosophy": "Argyris & Schön Çift Döngülü Öğrenme (Double-Loop Learning): Yalnızca hatayı düzeltmekle kalmaz, hataya yol açan karar normlarını ve eşiklerini de sorgular.",
        "papers": ["11", "16", "01", "07"],
    },
    {
        "id": "node-7",
        "num": 7,
        "mermaid_id": "Recompile",
        "short_title": "Node 7: Üst-Bilişsel Öz-Derleme (RSI-L2)",
        "title": "7. Üst-Bilişsel Öz-Derleme ve Hot-Reload (2. Derece RSI)",
        "badge": "RSI-L2",
        "file": "node_7_metacognitive_recompiler.py",
        "formula_latex": r"\mathcal{M}_{t+1} = \mathcal{M}_{\text{cand}} \iff \text{AST}(\mathcal{M}_{\text{cand}})=1 \land \text{MetaScore}(\mathcal{M}_{\text{cand}}) > \text{MetaScore}(\mathcal{M}_t) + \delta",
        "philosophy": "İkinci Derece Sibernetik (von Foerster) ve Gödelci Öz-Referans: Gözlemleyen ve yöneten mekanizmanın bizzat kendisini gözlemleyip çalışma zamanında yeniden derlemesi.",
        "papers": ["01", "07", "08", "20"],
    },
]

CATEGORIES_ORDER = [
    "Öz-Yinelemeli Gelişim (RSI) ve Ajan Evrimi",
    "Test Anı Akıl Yürütme (Test-Time Compute)",
    "Kısıtlı Donanım, Kuantizasyon ve SLM Motoru",
    "Bilişsel Mimari ve Bellek Hiyerarşisi",
    "Zeka Ölçümü, Felsefe ve İnsan-YZ Simbiyozu",
]


def parse_python_node(spec: dict) -> dict:
    fpath = os.path.join(NODES_DIR, spec["file"])
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)
    docstring = ast.get_docstring(tree) or ""
    classes = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            classes.append({"name": node.name, "methods": methods})

    # Extract concise summary from docstring
    role_desc = ""
    for ln in docstring.splitlines():
        if ln.strip().startswith("Görevi:"):
            idx = docstring.splitlines().index(ln)
            desc_lines = []
            for sub in docstring.splitlines()[idx:]:
                if sub.strip().startswith("===="):
                    break
                desc_lines.append(sub.replace("Görevi:", "").strip())
            role_desc = " ".join(desc_lines).strip()
            break

    return {
        **spec,
        "repo_path": f"src/nodes/{spec['file']}",
        "docstring": docstring,
        "summary": role_desc,
        "classes": classes,
        "code": code,
        "ast_valid": True,
        "line_count": len(code.splitlines()),
    }


def parse_markdown_note(md_path: str) -> dict:
    fname = os.path.basename(md_path)
    num = fname[:2]
    with open(md_path, "r", encoding="utf-8") as f:
        raw = f.read()

    title_match = re.search(r"^#\s+Çalışma Notu #\d+\s+—\s+(.+)$", raw, re.MULTILINE)
    full_title = title_match.group(1).strip() if title_match else fname

    cat_match = re.search(r"-\s+\*\*Kategori:\*\*\s+(.+)$", raw, re.MULTILINE)
    category = cat_match.group(1).strip() if cat_match else "Ar-Ge Notu"

    arxiv_match = re.search(r"\[arXiv Kaynağı\]\((https?://[^\)]+)\)", raw)
    arxiv_url = arxiv_match.group(1) if arxiv_match else None

    pdf_match = re.search(r"../../papers/([^\)]+\.pdf)", raw)
    pdf_file = pdf_match.group(1) if pdf_match else None
    pdf_size_mb = None
    if pdf_file:
        p_abs = os.path.join(PAPERS_DIR, pdf_file)
        if os.path.exists(p_abs):
            pdf_size_mb = round(os.path.getsize(p_abs) / (1024 * 1024), 2)

    node_refs = re.findall(r"\[`(Node \d+)`\]", raw)

    # Split sections by ## headings
    body_after_hr = raw.split("\n---\n", 1)[1].strip() if "\n---\n" in raw else raw
    sections = []
    extracted_code = ""
    parts = re.split(r"^##\s+(.+)$", body_after_hr, flags=re.MULTILINE)
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            sec_title = parts[i].strip()
            sec_body = parts[i + 1].strip()
            code_m = re.search(r"```python\s*(.*?)```", sec_body, flags=re.DOTALL)
            if code_m and not extracted_code:
                extracted_code = code_m.group(1).strip()
            # Remove code block from prose if desired or keep clean text
            sec_prose = re.sub(r"```[a-zA-Z]*\n.*?```", "", sec_body, flags=re.DOTALL).strip()
            sections.append({
                "heading": sec_title,
                "prose": sec_prose,
                "has_code": bool(code_m),
            })

    return {
        "id": f"paper-{num}",
        "num": num,
        "title": full_title,
        "category": category,
        "md_file": f"docs/notes/{fname}",
        "pdf_file": pdf_file,
        "pdf_rel_from_docs": f"../papers/{pdf_file}" if pdf_file else None,
        "pdf_size_mb": pdf_size_mb,
        "arxiv_url": arxiv_url,
        "arxiv_pdf_url": arxiv_url.replace("/abs/", "/pdf/") + ".pdf" if arxiv_url and "/abs/" in arxiv_url else None,
        "related_nodes": node_refs,
        "sections": sections,
        "sample_code": extracted_code,
    }


def extract_mermaid_from_arch() -> str:
    arch_path = os.path.join(DOCS_DIR, "architecture.md")
    with open(arch_path, "r", encoding="utf-8") as f:
        arch_md = f.read()
    m = re.search(r"```mermaid\s*(.*?)```", arch_md, flags=re.DOTALL)
    return m.group(1).strip() if m else ""


def main():
    nodes_data = [parse_python_node(s) for s in NODE_SPECS]
    notes_data = [
        parse_markdown_note(p)
        for p in sorted(glob.glob(os.path.join(NOTES_DIR, "*.md")))
    ]
    mermaid_code = extract_mermaid_from_arch()

    portal_payload = {
        "project": {
            "code": "SENTINEL",
            "title": "SENTINEL: Kısıtlı Donanımlarda Öz-Yinelemeli ve Simbiyotik AGI Bilişsel Mimarisi",
            "subtitle": "x86 CPU & 16 GB RAM Üzerinde Kuantize SLM, Çift Katmanlı RSI ve İnsan-YZ Simbiyozu Ar-Ge Spesifikasyonu",
            "stats": {
                "nodes_count": len(nodes_data),
                "papers_count": sum(1 for n in notes_data if n["pdf_file"]),
                "notes_count": len(notes_data),
                "rsi_layers": 2,
                "ram_budget_gb": 16,
            },
            "synthesis_latex": r"\text{SENTINEL} = \underbrace{\text{CoALA / A-MEM}}_{\text{Bellek İskeleti}} + \underbrace{\text{Gödel / DGM}}_{\text{Çift Katmanlı RSI}} + \underbrace{\text{s1 / DeepSeek-R1}}_{\text{Test Anı Düşünme}} + \underbrace{\text{BitNet / AWQ}}_{\text{Kuantize CPU Motoru}} + \underbrace{\text{Sentor Simbiyozu}}_{\text{Hizalama & Egemenlik}}",
        },
        "mermaid_diagram": mermaid_code,
        "equations": [
            {
                "id": "eq-1",
                "title": "1. İçsel Merak Ödülü ve Öz-Görev Seçimi (Schmidhuber Sıkıştırma İlerlemesi)",
                "node_ref": "node-0",
                "latex": r"g_{\text{auto}}^* = \arg\max_{g \in \mathcal{G}_{\text{cand}}} \Big[ H(Y \mid g, W_t) - \mathbb{E}_{o \sim \text{Env}(g)}\big[ H(Y \mid g, W_t \cup \{o\}) \big] \Big] - \lambda \cdot C_{\text{CPU}}(g)",
                "desc": "Sistem boşta (idle) kaldığında çok basit ya da tamamen gürültülü problemler yerine, beklenen epistemik bilgi kazancının (Bayesian Surprise) CPU maliyetine oranla maksimum olduğu uç senaryoyu üretir."
            },
            {
                "id": "eq-2",
                "title": "2. Epistemik Belirsizlik ve Keşif Kapısı (Shannon Entropisi)",
                "node_ref": "node-1",
                "latex": r"\text{Action}(g) = \begin{cases} \text{Exploit}(\mathcal{S}_t), & H(Y \mid g, W_t) \le \epsilon_t \\ \text{Explore \& Forage}(W_t \to W_{t+1}), & H(Y \mid g, W_t) > \epsilon_t \end{cases}",
                "desc": "Üst-Bilişsel Denetleyici mevcut bilgiyle yanıt üretmenin belirsizliğini ölçer; entropi eşiği aşılırsa halüsinasyonu engelleyip Dünya Modeli ve Araç Edinme döngüsünü tetikler."
            },
            {
                "id": "eq-3",
                "title": "3. Dış Kaynak Destekli Ucu Açık Yetenek Genişlemesi (1. Derece RSI)",
                "node_ref": "node-3",
                "latex": r"\mathcal{S}_{t+1} = \mathcal{S}_t \cup \left\{ s_{\text{new}} = \Psi(g, W_t, \mathcal{K}_{\text{ext}}) \;\middle\vert{}\; \mathbb{E}_{\text{sandbox}}\big[\text{Verify}(s_{\text{new}})\big] > \tau \right\}",
                "desc": "GitHub, teknik dokümantasyon ve web kaynaklarından devşirilen veya sıfırdan sentezlenen kodlar, izole sandbox doğrulama eşiğini (tau) geçtiğinde kalıcı .skills/ envanterine katılır."
            },
            {
                "id": "eq-4",
                "title": "4. Kısıtlı Donanımda Zeka Verimliliği (Chollet Metriği Uyarlaması)",
                "node_ref": "node-5",
                "latex": r"\mathcal{I}_{\text{SENTINEL}} = \frac{|\mathcal{S}_{t+T}| - |\mathcal{S}_t|}{\log(C_{\text{CPU}}) \cdot |\theta_{\text{quant}}|}",
                "desc": "Sistemin zekası statik ağırlık boyutuyla değil; birim CPU çevrimi ve kuantize parametre başına kazandığı doğrulanmış yeni beceri miktarıyla ölçülür."
            },
            {
                "id": "eq-5",
                "title": "5. Üst-Bilişsel Öz-Derleme ve Karar Güncellemesi (2. Derece RSI / Gödel Koşulu)",
                "node_ref": "node-7",
                "latex": r"\mathcal{M}_{t+1} = \begin{cases} \mathcal{M}_{\text{cand}}, & \text{eğer } \text{AST}(\mathcal{M}_{\text{cand}}) = 1 \;\land\; \mathbb{E}_{\mathcal{D}_{\text{meta}}}\big[\text{MetaScore}(\mathcal{M}_{\text{cand}})\big] > \text{MetaScore}(\mathcal{M}_t) + \delta \\ \mathcal{M}_t, & \text{aksi halde (Mevcut Denetleyiciyi Koru / Otomatik Rollback)} \end{cases}",
                "desc": "Üst-Bilişsel Denetleyici (controller.py), sistematik karar sapmalarında kendi kodunu yeniden yazar; AST güvenlik testi ve geçmiş senaryolar simülasyonunda delta marjını aşarsa çalışma zamanında bellekte yeniden derlenir."
            }
        ],
        "philosophy_pillars": [
            {
                "title": "Conatus & Ototelik Özne (Spinoza)",
                "tag": "Node 0",
                "desc": "Pasif komut bekleyen heteronom araçtan, boşta kaldığında kendi bilgisizlik sınırlarını keşfedip yetkinliğini artırmaya çalışan içsel amaçlı (autotelic) yapıya geçiş."
            },
            {
                "title": "Autopoiesis — Öz-Üretim (Maturana & Varela)",
                "tag": "Node 3 – Node 5",
                "desc": "Sistemin kendi operasyonel sınırlarını ve prosedürel beceri organlarını (.skills/) çevreyle etkileşim içinde çalışma zamanında bizzat üretmesi."
            },
            {
                "title": "İkinci Derece Sibernetik (Heinz von Foerster)",
                "tag": "Node 6 – Node 7",
                "desc": "Yalnızca dış sistemi gözlemleyen 1. derece geri beslemeden, karar alan denetleyicinin kendi eşiklerini gözlemleyip yeniden derlediği 2. derece özdüşünümselliğe sıçrama."
            },
            {
                "title": "İnsan-YZ Simbiyozu & Egemen Dışsal Korteks (Licklider & Engelbart)",
                "tag": "Not #20",
                "desc": "İnsan bilişini ikame edip körelten merkezi kara kutu yerine; yerel donanımda sahibine sadık çalışan, insanın etik/stratejik yönlendirmesiyle evrilen Sentor Zekası."
            }
        ],
        "categories": CATEGORIES_ORDER,
        "nodes": nodes_data,
        "notes": notes_data,
    }

    json_path = os.path.join(ASSETS_DIR, "portal_data.json")
    js_path = os.path.join(ASSETS_DIR, "portal_data.js")

    json_str = json.dumps(portal_payload, ensure_ascii=False, indent=2)
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(json_str)

    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// AUTO-GENERATED BY scripts/build_portal_index.py — DO NOT EDIT MANUALLY\n")
        f.write("window.SENTINEL_PORTAL_DATA = " + json_str + ";\n")

    print(f"[OK] Generated {json_path} ({len(json_str) / 1024:.1f} KB)")
    print(f"[OK] Generated {js_path} (Nodes: {len(nodes_data)}, Notes: {len(notes_data)})")


if __name__ == "__main__":
    main()

