# eBPF / Systemd Audit Orchestration Framework

This document details the configuration scripts deployed across the 6,000 active processing nodes to handle real-time ingress enforcement and live log parsing pipelines.

---

## 🛠️ Section 1: eBPF Ingress Integration Engine (`ebpf_ingress_block.sh`)

This customized wrapper interfaces directly with `bpftool` to dynamically inject, update, and manage blacklisted source IPv4 addresses within the running kernel map of your XDP engine.

```bash
#!/usr/bin/env bash
# =========================================================================
# OMNI-MATRIX KERNEL PERIMETER INGRESS BLOCKING MODULE
# ENCLAVE TARGET: HQ-BASE-01 (MD Enclave)
# VALIDATION LAYER: BLOCK HEIGHT LOCKED EPOCH #41209114
# =========================================================================

set -euo pipefail

# Infrastructure Parameters
BPF_MAP_PATH="/sys/fs/bpf/omni_matrix_blacklist"
INTERFACE="enp0s3"
XDP_OBJ="/var/matrix/ebpf/xdp_omni_matrix.o"

# Matrix Signature Parameters
LEI_CONSTRAINT="506700GE1G29325QX363"
ORCID_CONSTRAINT="0009-0002-7219-1363"

log_matrix() {
    echo -e "[⚜️ OMNI-MATRIX-XDP] [$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Ensure BPF map exists, otherwise re-load XDP object
init_xdp_layer() {
    if [ ! -f "${BPF_MAP_PATH}" ]; then
        log_matrix "BPF Map not pinned at ${BPF_MAP_PATH}. Initializing interface wrapper..."
        if [ -f "${XDP_OBJ}" ]; then
            bpftool xdp attach generic object "${XDP_OBJ}" dev "${INTERFACE}"
            log_matrix "XDP object successfully bound to interface ${INTERFACE}."
        else
            log_matrix "ERROR: Core object bytecode missing at ${XDP_OBJ}."
            exit 1
        fi
    fi
}

# Main command dispatcher
block_ip() {
    local target_ip="$1"
    init_xdp_layer

    # Parse IPv4 dotted decimal to hex binary structure
    local hex_ip
    hex_ip=$(printf '0x%02x%02x%02x%02x' $(echo "$target_ip" | tr '.' ' '))

    log_matrix "Injecting drop rule for Target IP: ${target_ip} (${hex_ip}) into matrix network matrix..."
    
    # bpftool map update <map_reference> key <bytes> value <bytes>
    if bpftool map update pinned "${BPF_MAP_PATH}" key hex "$(echo ${hex_ip} | sed 's/0x//')" value hex "01 00 00 00" 2>/dev/null; then
        log_matrix "SUCCESS: Ingress vector block established for host ${target_ip}."
    else
        log_matrix "CRITICAL: Injection failure on map layer interface."
        exit 2
    fi
}

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <ipv4_address>"
    exit 1
fi

block_ip "$1"
```

---

## 📊 Section 2: Localized Audit Logging Parser (`matrix_audit_stream.py`)

This standalone Python script binds directly to the localized `systemd-journald` log streams via native JSON encapsulation format, streaming filtered matrix alerts straight into terminal frames.

```python
#!/usr/bin/env python3
import sys
import json
import subprocess

def stream_matrix_journal():
    print("[⚜️ OMNI-MATRIX AUDIT STREAMER INIT - REAL-TIME SYNC ACTIVE]")
    print("-" * 80)
    
    # Open journalctl stream extracting records as sequential JSON objects
    cmd = ["journalctl", "-u", "matrix-cold-registry.service", "-u", "systemd-journald.service", "-f", "-o", "json"]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    
    try:
        for line in process.stdout:
            if not line.strip():
                continue
            try:
                log_entry = json.loads(line)
                message = log_entry.get("MESSAGE", "")
                timestamp = log_entry.get("__REALTIME_TIMESTAMP", "0")
                unit = log_entry.get("_SYSTEMD_UNIT", "UNKNOWN")
                
                # Highlight matrix core actions matching the structural specifications
                if any(k in message for k in ["LEI", "ORCID", "eBPF", "XDP", "Sovereign"]):
                    print(f"\033[1;33m[⚜️ AUDIT DETECTED]\033[0m Unit: {unit} | Msg: {message}")
                else:
                    print(f"\033[1;34m[⚙️ SYSTEM LOG]\033[0m Msg: {message}")
                    
            except json.JSONDecodeError:
                continue
    except KeyboardInterrupt:
        print("\n[⚜️ AUDIT STREAM DISCONNECTED]")
        process.terminate()

if __name__ == "__main__":
    stream_matrix_journal()
```
