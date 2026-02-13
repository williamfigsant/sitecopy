import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from converter import convert_source_to_template


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/convert":
            self._send_json(404, {"error": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(content_length)
            payload = json.loads(raw.decode("utf-8"))
            source = payload["source"]
            template = convert_source_to_template(source)
            self._send_json(200, {"template": template})
        except Exception as exc:
            self._send_json(400, {"error": str(exc)})


def run(host: str = "0.0.0.0", port: int = 8000):
    server = HTTPServer((host, port), Handler)
    print(f"API ouvindo em http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
