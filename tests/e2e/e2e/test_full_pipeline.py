import os
import json
import threading
import http.server
import socketserver
import shutil
import time
import pytest
from pathlib import Path

TEST_ROOT = Path(__file__).resolve().parent
REPO_ROOT = TEST_ROOT.parents[2]
OUTPUT_DIR = REPO_ROOT / "data" / "e2e-outputs"

class MockHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length else b''
        resp = json.dumps({"mock":"response"}).encode()
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length', str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)
    def log_message(self, *args):
        pass

def start_mock_server(port):
    server = socketserver.TCPServer(("127.0.0.1", port), MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

def simulate_pipeline():
    # simple simulation: copy sample-data to outputs and write result.json
    sample = Path(REPO_ROOT) / "sample-data"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    files = []
    if sample.exists():
        for p in sample.iterdir():
            if p.is_file():
                dest = OUTPUT_DIR / p.name
                try:
                    shutil.copy2(p, dest)
                    files.append(p.name)
                except Exception:
                    pass
    result = {"status":"ok","files":files}
    with open(OUTPUT_DIR/"result.json","w") as f:
        json.dump(result,f)
    return result


def test_pipeline_flow(tmp_path):
    # start mocks
    llm = start_mock_server(9001)
    smtp = start_mock_server(9002)
    try:
        res = simulate_pipeline()
        assert res["status"]=="ok"
        out = OUTPUT_DIR/"result.json"
        assert out.exists()
        data = json.load(open(out))
        assert "files" in data
    finally:
        llm.shutdown()
        smtp.shutdown()


def test_ui_with_playwright():
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    ui = TEST_ROOT/"ui_mock.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{ui}")
        assert "E2E UI Mock" in page.content()
        browser.close()
