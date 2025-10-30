from pathlib import Path
import re

# Ollama settings
OLLAMA_HOST = "http://127.0.0.1:11434"
OLLAMA_MODEL = "mistral:latest"
  # pull first with: ollama pull gemma2:2b
OLLAMA_TIMEOUT = 60  # seconds

# Runtime paths
ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = ROOT / "runs"
RUNS_DIR.mkdir(exist_ok=True, parents=True)

# Nmap binary
NMAP_BIN = "nmap"

# Allowed Nmap flags whitelist
ALLOWED_FLAGS = {
    "-n", "-Pn", "-sT", "-p", "-T0", "-T1", "-T2", "-T3",
    "-oX", "-oN", "-oG", "-sV", "--version-intensity",
    "--open", "--host-timeout", "--min-rate", "--max-retries"
}

# Disallowed patterns for safety
DISALLOWED_PATTERNS = [
    r"--script\b",
    r"--script-args\b",
    r"-e\b",
    r"-D\b",
    r"--fuzz\b",
    r"--badsum\b"
]

# Private IPv4 regex
PRIVATE_IP_REGEX = re.compile(
    r"^(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})$"
)
