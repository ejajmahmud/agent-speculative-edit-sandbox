"""Core Speculative Edit Sandbox implementation."""
import ast
import os
from typing import Dict, List, Optional, Tuple, Any


class StageResult:
    def __init__(self, filename: str, valid: bool, error: str = "", ast_nodes: int = 0):
        self.filename = filename
        self.valid = valid
        self.error = error
        self.ast_nodes = ast_nodes


class SpeculativeSandbox:
    def __init__(self):
        self.overlay_files: Dict[str, str] = {}  # filepath -> content
        self.disk_backups: Dict[str, Optional[str]] = {}  # filepath -> original_content

    def stage_file(self, filename: str, content: str) -> StageResult:
        # Check syntax if python file
        if filename.endswith(".py"):
            try:
                tree = ast.parse(content)
                node_count = len(list(ast.walk(tree)))
            except SyntaxError as e:
                return StageResult(filename, False, f"SyntaxError at line {e.lineno}: {e.msg}")
            except Exception as e:
                return StageResult(filename, False, f"ParseError: {e}")
        else:
            node_count = 0

        self.overlay_files[filename] = content
        return StageResult(filename, True, ast_nodes=node_count)

    def get_staged_content(self, filename: str) -> Optional[str]:
        return self.overlay_files.get(filename)

    def discard_staged(self, filename: Optional[str] = None):
        if filename:
            self.overlay_files.pop(filename, None)
        else:
            self.overlay_files.clear()

    def commit_to_disk(self, target_dir: str) -> List[str]:
        committed_files = []
        for rel_path, content in self.overlay_files.items():
            full_path = os.path.join(target_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            committed_files.append(rel_path)
        self.overlay_files.clear()
        return committed_files
