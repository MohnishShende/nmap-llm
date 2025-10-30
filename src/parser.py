import xmltodict
import json
from pathlib import Path

def parse_nmap_xml(xml_path: Path):
    data = xmltodict.parse(xml_path.read_bytes())
    hosts_raw = data.get("nmaprun", {}).get("host", [])
    if not isinstance(hosts_raw, list):
        hosts_raw = [hosts_raw]
    hosts = []
    for h in hosts_raw:
        if not h:
            continue
        # address
        addr = None
        address = h.get("address")
        if isinstance(address, list):
            for a in address:
                if a.get("@addrtype") == "ipv4":
                    addr = a.get("@addr")
                    break
            if not addr and address:
                addr = address[0].get("@addr")
        elif isinstance(address, dict):
            addr = address.get("@addr")
        # ports
        ports = []
        ports_section = h.get("ports", {}).get("port", [])
        if not isinstance(ports_section, list):
            ports_section = [ports_section]
        for p in ports_section:
            if not p:
                continue
            try:
                portid = int(p.get("@portid"))
            except Exception:
                continue
            state = None
            service = None
            version = None
            st = p.get("state")
            if isinstance(st, dict):
                state = st.get("@state")
            sv = p.get("service")
            if isinstance(sv, dict):
                service = sv.get("@name")
                v = sv.get("@version")
                prod = sv.get("@product")
                extrainfo = sv.get("@extrainfo")
                parts = [prod, v, extrainfo]
                version = " ".join([x for x in parts if x]) if any(parts) else None
            ports.append({
                "port": portid,
                "state": state,
                "service": service,
                "version": version
            })
        hosts.append({"addr": addr, "ports": ports})
    return {"hosts": hosts}

def save_json(json_path: Path, obj) -> None:
    json_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
