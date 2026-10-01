"""
MarketPulse Sunucu
==================
Kullanim:
  python sunucu.py
  Tarayicide: http://localhost:8000/borsa-analiz.html
"""

import http.server, json, os
from urllib.parse import urlparse, parse_qs

KLASOR = os.path.dirname(os.path.abspath(__file__))

class MarketPulseHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=KLASOR, **kwargs)

    def log_message(self, format, *args):
        pass  # Gereksiz log mesajlarini kapat

    def do_POST(self):
        path = urlparse(self.path).path

        # Portföy kaydet
        if path == '/api/portfolyo-kaydet':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                with open(os.path.join(KLASOR, 'portfolyo.json'), 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self._json_ok({'durum': 'ok'})
            except Exception as e:
                self._json_err(str(e))

        # İşlem günlüğü kaydet
        elif path == '/api/islemler-kaydet':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                with open(os.path.join(KLASOR, 'islemler.json'), 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self._json_ok({'durum': 'ok'})
            except Exception as e:
                self._json_err(str(e))
        else:
            self.send_error(404)

    def _json_ok(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def _json_err(self, msg):
        body = json.dumps({'durum': 'hata', 'mesaj': msg}).encode()
        self.send_response(500)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    import socketserver
    PORT = 8000
    print("MarketPulse Sunucu baslatildi")
    print(f"Adres: http://localhost:{PORT}/borsa-analiz.html")
    print("Durdurmak icin: Ctrl+C\n")
    with socketserver.TCPServer(("", PORT), MarketPulseHandler) as httpd:
        httpd.serve_forever()
