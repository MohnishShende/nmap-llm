# Nmap LLM  
### AI-Assisted Network Scanner and Triage Tool  

**Nmap LLM** is an offline, ethical cybersecurity tool that transforms **natural-language requests** into safe, validated Nmap commands using a local **LLM via Ollama**. It then parses the results and generates a clear, Markdown-based triage report.  

> ⚠️ **Legal Notice:** Only scan systems that you own or have written authorization to test. Unauthorized scanning is illegal.

---

## 🧩 Features
- Converts plain English into safe, validated Nmap commands.  
- Scans restricted to private IPv4 ranges only.  
- Parses Nmap XML → JSON and generates Markdown triage reports.  
- Operates fully offline using **Ollama** (no external API).  
- Each run is timestamped and logged for reproducibility.

---

## 🧠 Tech Stack
- **Python 3.10+**  
- **Nmap** (TCP connect mode, non-intrusive)  
- **Ollama (Mistral model)**  
- **macOS / Linux compatible**

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/MohnishShende/nmap-llm.git
cd nmap-llm

# Create and activate virtual environment
python3 -m venv venv --upgrade-deps
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Nmap
brew install nmap  # macOS
# or use your distro package manager for Linux

# Install Ollama and pull a model
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull mistral:latest
````

---

## 🚀 Usage

### 1. Natural-language scan

```bash
python3 -m src.main nl "scan 192.168.1.181 for web, ssh and rdp with version detection"
```

### 2. Run an explicit Nmap command

```bash
python3 -m src.main scan "nmap -sT -Pn -p 22,80,3389 -sV 192.168.1.181"
```

### 3. Analyze an existing XML scan

```bash
python3 -m src.main analyze runs/results-YYYYMMDD-HHMMSS.xml
```

---

## 📁 Output Files

Each scan creates a timestamped record in the `runs/` directory:

| File             | Description                                    |
| ---------------- | ---------------------------------------------- |
| `results-*.xml`  | Raw Nmap XML output                            |
| `results-*.json` | Parsed JSON data                               |
| `report-*.md`    | LLM-generated triage report                    |
| `run-*.log`      | Log file with prompts, commands, and responses |

Example:

```bash
cat runs/report-20251030-060301.md
```

---

## 🧰 Troubleshooting

**Module not found (requests/xmltodict):**

```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Ollama connection error (404):**

```bash
ollama serve
curl http://127.0.0.1:11434/api/tags
```

**Model not installed:**

```bash
ollama pull mistral:latest
```

---

## 🧠 Example Output

```
## Summary
Host 192.168.1.181 was scanned for web, ssh, and rdp.

## Findings
- **Low:** RDP (3389/tcp) open, Microsoft Terminal Services detected.
- **Closed:** SSH (22/tcp), HTTP (80/tcp).

## Recommendations
Restrict RDP access, enforce strong authentication, and monitor sessions.
```

---

## 🧑‍💻 Contributing

Pull requests are welcome. Open an issue to discuss new features or improvements.

---

## 🪪 License

```
MIT License

Copyright (c) 2025 Mohnish Shende

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🔗 Author

**Mohnish Shende**
GitHub: [https://github.com/MohnishShende](https://github.com/MohnishShende)
Cybersecurity Researcher | AI & Network Security Automation

