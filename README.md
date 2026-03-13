# extract-tryhackme-ssrf-relay

A Python-based **SSRF relay engine** leveraging socket threading and gopher payload encoding, built specifically for the **Extract TryHackMe challenge**.  
This tool demonstrates how to exploit SSRF vulnerabilities by relaying traffic through a custom socket listener and gopher-encoded payloads.

---

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/extract-tryhackme-ssrf-relay.git
   cd extract-tryhackme-ssrf-relay
   ```
2. Update the 'gateway_host' and 'target_port' values inside the APPLICATION_MAP section of the script:
   ```bash
   "bind_addr": "127.0.0.1",
   "bind_port": 8888,
   "gateway_host": "MACHINE_IP",
   "target_ip": "127.0.0.1",
   "target_port": TARGATED_PORT
   ```
3. Run the script:
   ```bash
   python3 relay.py
   ```

---

## License

This project is licensed under the MIT License – see the LICENSE file for details.

---

## Disclaimer

This project is intended only for educational and ethical penetration testing purposes.
Do not use this tool on systems without explicit authorization.
