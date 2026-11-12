import os
import sys
import time
import ssl
import socket
import urllib.request
import urllib.parse
import urllib.error

sys.stdout.reconfigure(line_buffering=True)
socket.setdefaulttimeout(20)
ctx = ssl._create_unverified_context()

papers = [
    {
        "num": "01",
        "key": "Darwin_Godel_Machine",
        "title": "Darwin Gödel Machine (DGM): Open-Ended Evolution of Self-Improving Agents",
        "urls": ["https://arxiv.org/pdf/2505.22954.pdf", "https://arxiv.org/abs/2505.22954"]
    },
    {
        "num": "02",
        "key": "Absolute_Zero",
        "title": "Absolute Zero: Reinforced Self-play Reasoning with Zero Data",
        "urls": ["https://arxiv.org/pdf/2505.03335.pdf", "https://arxiv.org/abs/2505.03335"]
    },
    {
        "num": "03",
        "key": "BitNet_b1_58_2B4T",
        "title": "BitNet b1.58 2B4T Technical Report",
        "urls": ["https://arxiv.org/pdf/2504.12285.pdf", "https://arxiv.org/pdf/2402.17764.pdf"]
    },
    {
        "num": "04",
        "key": "A_MEM_Agentic_Memory",
        "title": "A-MEM: Agentic Memory for LLM Agents",
        "urls": ["https://arxiv.org/pdf/2502.12110.pdf", "https://arxiv.org/abs/2502.12110"]
    },
    {
        "num": "05",
        "key": "s1_Simple_Test_Time_Scaling",
        "title": "s1: Simple Test-Time Scaling",
        "urls": ["https://arxiv.org/pdf/2501.19393.pdf"]
    },
    {
        "num": "06",
        "key": "DeepSeek_R1_Reasoning",
        "title": "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning",
        "urls": ["https://arxiv.org/pdf/2501.12948.pdf"]
    },
    {
        "num": "07",
        "key": "Godel_Agent",
        "title": "Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement",
        "urls": ["https://arxiv.org/pdf/2410.04444.pdf"]
    },
    {
        "num": "08",
        "key": "ADAS_Automated_Design_Agentic_Systems",
        "title": "ADAS: Automated Design of Agentic Systems",
        "urls": ["https://arxiv.org/pdf/2408.08435.pdf"]
    },
    {
        "num": "09",
        "key": "Scaling_LLM_Test_Time_Compute",
        "title": "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters",
        "urls": ["https://arxiv.org/pdf/2408.03314.pdf"]
    },
    {
        "num": "10",
        "key": "Open_Endedness_DeepMind",
        "title": "Open-Endedness is Essential for Artificial Superhuman Intelligence",
        "urls": ["https://arxiv.org/pdf/2406.04268.pdf"]
    },
    {
        "num": "11",
        "key": "Self_Rewarding_Language_Models",
        "title": "Self-Rewarding Language Models",
        "urls": ["https://arxiv.org/pdf/2401.10020.pdf"]
    },
    {
        "num": "12",
        "key": "AWQ_Activation_aware_Weight_Quantization",
        "title": "AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration",
        "urls": [
            "https://arxiv.org/pdf/2306.00978.pdf",
            "https://proceedings.mlsys.org/paper_files/paper/2024/file/42a452cbafa9dd64e9ba4aa95cc1ef21-Paper-Conference.pdf"
        ]
    },
    {
        "num": "13",
        "key": "MemGPT_LLM_OS",
        "title": "MemGPT: Towards LLMs as Operating Systems",
        "urls": ["https://arxiv.org/pdf/2310.08560.pdf"]
    },
    {
        "num": "14",
        "key": "CoALA_Cognitive_Architectures",
        "title": "CoALA: Cognitive Architectures for Language Agents",
        "urls": ["https://arxiv.org/pdf/2309.02427.pdf"]
    },
    {
        "num": "15",
        "key": "Voyager_Open_Ended_Agent",
        "title": "Voyager: An Open-Ended Embodied Agent with Large Language Models",
        "urls": ["https://arxiv.org/pdf/2305.16291.pdf"]
    },
    {
        "num": "16",
        "key": "Reflexion_Verbal_Reinforcement",
        "title": "Reflexion: Language Agents with Verbal Reinforcement Learning",
        "urls": ["https://arxiv.org/pdf/2303.11366.pdf"]
    },
    {
        "num": "17",
        "key": "LLM_int8_Matrix_Multiplication",
        "title": "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale",
        "urls": ["https://arxiv.org/pdf/2208.07339.pdf"]
    },
    {
        "num": "18",
        "key": "STaR_Bootstrapping_Reasoning",
        "title": "STaR: Bootstrapping Reasoning With Reasoning",
        "urls": ["https://arxiv.org/pdf/2203.14465.pdf"]
    },
    {
        "num": "19",
        "key": "On_the_Measure_of_Intelligence_Chollet",
        "title": "On the Measure of Intelligence",
        "urls": ["https://arxiv.org/pdf/1911.01547.pdf"]
    }
]

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target_dir = os.path.join(repo_root, "papers")
os.makedirs(target_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,*/*'
}

def download_stream(url, out_path):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
        first_chunk = resp.read(2048)
        if b'%PDF' not in first_chunk:
            raise Exception("Response is not a valid PDF header")
        with open(out_path, 'wb') as f:
            f.write(first_chunk)
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
    return os.path.getsize(out_path)

if __name__ == "__main__":
    print(f"=== SENTINEL PDF DOWNLOADER -> {target_dir} ({len(papers)} Papers) ===")
    report = []

    for idx, p in enumerate(papers, 1):
        fname = f"{p['num']}_{p['key']}.pdf"
        fpath = os.path.join(target_dir, fname)
        if os.path.exists(fpath) and os.path.getsize(fpath) > 50000:
            sz = os.path.getsize(fpath)
            print(f"[{idx:02d}/19] [EXISTS] {fname} ({sz/(1024*1024):.2f} MB)")
            report.append((p['num'], p['key'], True, sz, "cached"))
            continue

        print(f"[{idx:02d}/19] [DOWNLOADING] {p['title']}...")
        downloaded = False
        for u in p['urls']:
            try:
                print(f"       -> GET {u}")
                sz = download_stream(u, fpath)
                print(f"       [+] OK: {fname} ({sz/(1024*1024):.2f} MB)")
                downloaded = True
                report.append((p['num'], p['key'], True, sz, u))
                time.sleep(1.0)
                break
            except Exception as e:
                print(f"       [-] Failed with {u}: {e}")
                if os.path.exists(fpath):
                    try:
                        os.remove(fpath)
                    except OSError:
                        pass
                time.sleep(0.5)

        if not downloaded:
            print(f"       [!] CRITICAL: Failed to download {fname}")
            report.append((p['num'], p['key'], False, 0, "failed"))

    print("\n=== SUMMARY ===")
    success_total = sum(1 for r in report if r[2])
    print(f"Completed: {success_total}/{len(papers)} successfully verified in papers/.")

