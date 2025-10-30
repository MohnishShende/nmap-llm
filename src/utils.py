import json
import re
import time
from pathlib import Path
from typing import Tuple
from .config import (
    ALLOWED_FLAGS, DISALLOWED_PATTERNS, PRIVATE_IP_REGEX, RUNS_DIR
)

def ts_now() -> str:
    return time.strftime("%Y%m%d-%H%M%S")

def is_private_ip(ip: str) -> bool:
    return bool(PRIVATE_IP_REGEX.match(ip))

def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")

def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def parse_llm_json_block(text: str):
    """Extract JSON from an LLM response even if it has markdown, comments, or chatter."""
    cleaned = text.strip()
    cleaned = cleaned.replace("```json", "").replace("```", "")
    cleaned = cleaned.replace("“", "\"").replace("”", "\"")  # normalize quotes
    cleaned = re.sub(r'^[^{]*', '', cleaned)  # drop anything before first {
    cleaned = re.sub(r'[^}]*$', '', cleaned)  # drop anything after last }
    try:
        return json.loads(cleaned)
    except Exception:
        # last resort repair: try to find the first {...} block
        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            return None
        candidate = m.group(0)
        try:
            return json.loads(candidate)
        except Exception:
            repaired = candidate.replace("\n", " ").replace("\r", "")
            repaired = re.sub(r",\s*}", "}", repaired)
            repaired = re.sub(r",\s*\]", "]", repaired)
            try:
                return json.loads(repaired)
            except Exception:
                return None

def validate_nmap_command(nmap_cmd: str) -> Tuple[bool, str]:
    import shlex
    tokens = shlex.split(nmap_cmd)
    if not tokens or tokens[0].lower() != "nmap":
        return False, "Command must start with nmap."
    joined = " ".join(tokens)
    for pat in DISALLOWED_PATTERNS:
        if re.search(pat, joined):
            return False, f"Disallowed pattern matched: {pat}"
    i = 1
    target_found = False
    while i < len(tokens):
        t = tokens[i]
        if t.startswith("-"):
            base = t.split("=")[0]
            if base not in ALLOWED_FLAGS:
                return False, f"Flag not allowed: {base}"
            if base in {"-p", "-oX", "-oN", "-oG", "--host-timeout", "--min-rate", "--max-retries", "--version-intensity"}:
                i += 1
        else:
            target_found = True
        i += 1
    if not target_found:
        return False, "No target specified."
    return True, "OK"

def new_run_paths(prefix: str):
    now = ts_now()
    base = RUNS_DIR / f"{prefix}-{now}"
    log = RUNS_DIR / f"run-{now}.log"
    xml = RUNS_DIR / f"results-{now}.xml"
    jsn = RUNS_DIR / f"results-{now}.json"
    rpt = RUNS_DIR / f"report-{now}.md"
    return log, xml, jsn, rpt
