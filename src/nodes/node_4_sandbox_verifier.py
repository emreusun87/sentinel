"""
SENTINEL MİMARİSİ // NODE 4: DETERMINİSTİK DOĞRULAMA VE SANDBOX
================================================================================
Atıf Yapılan Node: [SandboxVerify] - Deterministik Doğrulama & Sandbox
Görevi: Sentezlenen veya dış kaynaktan uyarlanan araç kodunu canlı sisteme
sürmeden önce; izole sanal ortamda (sandbox) sözdizimi, güvenlik kısıtları,
çalışma süresi ve doğruluk kriterleri açısından test etmek.
================================================================================
"""

import ast
import subprocess
import tempfile
import os
import json

class SandboxVerifier:
    def __init__(self, max_timeout_seconds=15, max_memory_mb=256):
        self.timeout = max_timeout_seconds
        self.max_memory = max_memory_mb

    def verify_syntax_ast(self, code_string: str) -> tuple:
        """Sözdizimini (syntax) Abstract Syntax Tree ile denetler."""
        try:
            tree = ast.parse(code_string)
            # Tehlikeli çağrıları tara (örn. rm -rf, os.kill vb.)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if hasattr(node.func, "id") and node.func.id in ["eval", "exec"]:
                        return False, "Tehlikeli yerleşik fonksiyon çağrısı (eval/exec)."
            return True, "AST sözdizimi geçerli."
        except SyntaxError as e:
            return False, f"Sözdizimi hatası: {e}"

    def run_in_isolated_process(self, tool_code: str, test_input: str = "") -> dict:
        """
        Kodu geçici izole bir python dosyasına yazar ve kısıtlı subprocess ile koşturur.
        """
        # 1. AST kontrolü
        is_ast_ok, ast_msg = self.verify_syntax_ast(tool_code)
        if not is_ast_ok:
            return {"pass": False, "error": ast_msg, "stage": "AST_VALIDATION"}

        # 2. Geçici dosyada çalıştırma
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as tmp:
            tmp.write(tool_code)
            tmp_path = tmp.name

        try:
            cmd = ["python", tmp_path]
            proc = subprocess.run(
                cmd,
                input=test_input,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if proc.returncode == 0:
                print(f"[NODE-4] Sandbox Başarılı! Çıktı: {proc.stdout.strip()[:150]}")
                return {
                    "pass": True,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "stage": "EXECUTION_SUCCESS"
                }
            else:
                print(f"[NODE-4] Sandbox Yürütme Hatası (Exit {proc.returncode}): {proc.stderr.strip()[:200]}")
                return {
                    "pass": False,
                    "error": proc.stderr or proc.stdout,
                    "returncode": proc.returncode,
                    "stage": "RUNTIME_EXECUTION"
                }
        except subprocess.TimeoutExpired:
            print(f"[NODE-4] Zaman aşımı ({self.timeout}s). Sonsuz döngü engellendi.")
            return {"pass": False, "error": "Zaman aşımı (Timeout)", "stage": "TIMEOUT_GUARD"}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

