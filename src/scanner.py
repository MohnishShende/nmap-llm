import shlex
import subprocess
from pathlib import Path
from .config import NMAP_BIN
from .utils import validate_nmap_command

def ensure_oX(xml_path: Path, nmap_cmd: str) -> str:
    tokens = shlex.split(nmap_cmd)
    if "-oX" not in tokens:
        nmap_cmd = f"{nmap_cmd} -oX {str(xml_path)}"
    else:
        parts = tokens[:]
        for i, t in enumerate(parts):
            if t == "-oX" and i+1 < len(parts):
                parts[i+1] = str(xml_path)
                break
        nmap_cmd = " ".join(parts)
    return nmap_cmd

def run_nmap(nmap_cmd: str, xml_path: Path) -> None:
    ok, msg = validate_nmap_command(nmap_cmd)
    if not ok:
        raise ValueError(f"Validation failed. {msg}")
    nmap_cmd = ensure_oX(xml_path, nmap_cmd)
    if not nmap_cmd.startswith("nmap"):
        nmap_cmd = nmap_cmd.replace("nmap", NMAP_BIN, 1)
    print(f"Running: {nmap_cmd}")
    subprocess.run(shlex.split(nmap_cmd), check=True)
