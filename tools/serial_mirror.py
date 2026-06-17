#!/usr/bin/env python3
import argparse
import http.server
import json
import os
import queue
import socketserver
import threading
import time
from pathlib import Path

import serial


ROOT = Path(__file__).resolve().parents[1]
CLIENTS = []
CLIENTS_LOCK = threading.Lock()
LATEST = {
    "state": "waiting",
    "score": 0,
    "best": 0,
    "level": 0,
    "alt": "",
    "message": "等待 M5Stick 串口数据",
}


def broadcast(payload):
    with CLIENTS_LOCK:
        clients = list(CLIENTS)
    for client in clients:
        try:
            client.put_nowait(payload)
        except queue.Full:
            pass


def serial_worker(port, baud):
    global LATEST
    while True:
        try:
            with serial.Serial(port, baud, timeout=1) as ser:
                LATEST = {
                    "state": "connected",
                    "score": 0,
                    "best": 0,
                    "level": 0,
                    "alt": "",
                    "message": f"已连接 {port}",
                }
                broadcast(LATEST)
                while True:
                    raw = ser.readline().decode("utf-8", errors="ignore").strip()
                    if not raw.startswith("DJ:"):
                        continue
                    try:
                        LATEST = json.loads(raw[3:])
                        broadcast(LATEST)
                    except json.JSONDecodeError:
                        continue
        except serial.SerialException as exc:
            LATEST = {
                "state": "error",
                "score": 0,
                "best": 0,
                "level": 0,
                "alt": "",
                "message": str(exc),
            }
            broadcast(LATEST)
            time.sleep(1.5)


class MirrorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        print(fmt % args)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            client = queue.Queue(maxsize=24)
            with CLIENTS_LOCK:
                CLIENTS.append(client)
            try:
                self._send_event(LATEST)
                while True:
                    try:
                        payload = client.get(timeout=15)
                        self._send_event(payload)
                    except queue.Empty:
                        self.wfile.write(b": ping\n\n")
                        self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                with CLIENTS_LOCK:
                    if client in CLIENTS:
                        CLIENTS.remove(client)
            return

        return super().do_GET()

    def _send_event(self, payload):
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.wfile.write(b"data: " + data + b"\n\n")
        self.wfile.flush()


def main():
    parser = argparse.ArgumentParser(description="Devil Jump serial mirror bridge")
    parser.add_argument("--serial", default=os.environ.get("M5_PORT", "/dev/cu.usbserial-6952522CF5"))
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--http", type=int, default=8766)
    args = parser.parse_args()

    thread = threading.Thread(target=serial_worker, args=(args.serial, args.baud), daemon=True)
    thread.start()

    with socketserver.ThreadingTCPServer((args.host, args.http), MirrorHandler) as server:
        server.daemon_threads = True
        print(f"Mirror: http://{args.host}:{args.http}/mirror/")
        print(f"Serial: {args.serial} @ {args.baud}")
        server.serve_forever()


if __name__ == "__main__":
    main()
