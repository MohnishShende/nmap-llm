#!/usr/bin/env python3
import argparse
from pathlib import Path
from .config import OLLAMA_MODEL
from .llm import ollama_generate
from .scanner import run_nmap
from .parser import parse_nmap_xml, save_json
from .utils import new_run_paths, write_text, parse_llm_json_block

GEN_PROMPT_SYSTEM = """You are a defensive cybersecurity assistant.
You must output ONLY valid JSON. Do not include any extra text or explanations.

Your JSON must contain exactly these keys:
- "nmap_cmd"
- "explanation"
- "port_set_hint"

Rules:
1. Use -sT and -Pn.
2. Never use --script or intrusive options.
3. Only private IPv4 targets.
4. Output strictly one JSON object, nothing else.

Example:
{"nmap_cmd":"nmap -sT -Pn -p 22,80,443,3389 -sV 192.168.1.45","explanation":"Scan SSH, web, and RDP services.","port_set_hint":"22,80,443,3389"}
"""

TRIAGE_PROMPT_SYSTEM = """You are a defensive security analyst.
Given structured Nmap results in JSON, analyze only legitimate network risks.

Output a Markdown report with sections:
- **Summary**
- **Findings** (label High, Medium, Low)
- **Recommendations**
"""

def cmd_nl(nl_text: str):
    log, xml, jsn, rpt = new_run_paths("nl")
    user_prompt = GEN_PROMPT_SYSTEM + "\nUSER_REQUEST:\n" + nl_text + "\nIMPORTANT: Output only JSON."
    llm_out = ollama_generate(user_prompt)
    write_text(log, f"NL: {nl_text}\n\nLLM raw:\n{llm_out}\n")

    blob = parse_llm_json_block(llm_out)
    if not blob or "nmap_cmd" not in blob:
        print("=== RAW LLM OUTPUT START ===")
        print(llm_out)
        print("=== RAW LLM OUTPUT END ===")
        raise RuntimeError("Failed to parse JSON from LLM response.")

    nmap_cmd = blob["nmap_cmd"]
    run_nmap(nmap_cmd, xml)
    obj = parse_nmap_xml(xml)
    save_json(jsn, obj)

    triage_prompt = TRIAGE_PROMPT_SYSTEM + "\n\nDATA:\n" + Path(jsn).read_text(encoding="utf-8")
    report = ollama_generate(triage_prompt)
    Path(rpt).write_text(report, encoding="utf-8")

    print(f"Done.\nXML: {xml}\nJSON: {jsn}\nReport: {rpt}\nLog: {log}")

def cmd_scan(nmap_cmd: str):
    log, xml, jsn, rpt = new_run_paths("scan")
    write_text(log, f"CMD: {nmap_cmd}\n")
    run_nmap(nmap_cmd, xml)
    obj = parse_nmap_xml(xml)
    save_json(jsn, obj)

    triage_prompt = TRIAGE_PROMPT_SYSTEM + "\n\nDATA:\n" + Path(jsn).read_text(encoding="utf-8")
    report = ollama_generate(triage_prompt)
    Path(rpt).write_text(report, encoding="utf-8")

    print(f"Done.\nXML: {xml}\nJSON: {jsn}\nReport: {rpt}\nLog: {log}")

def cmd_analyze(xml_path: str):
    xml_path = Path(xml_path)
    if not xml_path.exists():
        raise FileNotFoundError(xml_path)
    log, _, jsn, rpt = new_run_paths("analyze")
    write_text(log, f"Analyze: {xml_path}\n")
    obj = parse_nmap_xml(xml_path)
    save_json(jsn, obj)

    triage_prompt = TRIAGE_PROMPT_SYSTEM + "\n\nDATA:\n" + Path(jsn).read_text(encoding="utf-8")
    report = ollama_generate(triage_prompt)
    Path(rpt).write_text(report, encoding="utf-8")

    print(f"Done.\nJSON: {jsn}\nReport: {rpt}\nLog: {log}")

def main():
    parser = argparse.ArgumentParser(description="LLM assisted Nmap tool")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_nl = sub.add_parser("nl", help="Natural language scan")
    p_nl.add_argument("text", help="Scan request text")

    p_scan = sub.add_parser("scan", help="Run explicit Nmap command")
    p_scan.add_argument("cmd", help="Nmap command")

    p_an = sub.add_parser("analyze", help="Analyze Nmap XML")
    p_an.add_argument("xml_path", help="Path to XML file")

    args = parser.parse_args()
    if args.mode == "nl":
        cmd_nl(args.text)
    elif args.mode == "scan":
        cmd_scan(args.cmd)
    elif args.mode == "analyze":
        cmd_analyze(args.xml_path)

if __name__ == "__main__":
    main()
