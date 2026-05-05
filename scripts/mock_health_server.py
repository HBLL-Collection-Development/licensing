import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class Handler(BaseHTTPRequestHandler):
    def _send(self, code=200, body=None):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if body is None:
            body = {'status': 'ok'}
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        if self.path in ['/', '/queue', '/llm/health']:
            if self.path == '/':
                self._send(200, {'message': 'Library Licensing Assistant API', 'status': 'ok'})
            elif self.path == '/queue':
                self._send(200, {'queue_status': 'ok', 'pending': False})
            else:
                self._send(200, {'llm': 'ok'})
        else:
            self._send(404, {'error': 'not found'})

    def log_message(self, format, *args):
        return

def run(port=8000):
    server = HTTPServer(('127.0.0.1', port), Handler)
    print(f"Mock health server listening on http://127.0.0.1:{port}")
    server.serve_forever()

if __name__ == '__main__':
    run(8000)
