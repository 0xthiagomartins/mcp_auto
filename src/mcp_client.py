from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class MCPVehicleClient:
    def __init__(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self._process = subprocess.Popen(
            [sys.executable, "-m", "src.mcp_server"],
            cwd=root,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._seq = 0
        self._request("initialize", {})

    def close(self) -> None:
        if self._process.poll() is None:
            self._process.terminate()

    def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        self._seq += 1
        payload = {"jsonrpc": "2.0", "id": self._seq, "method": method, "params": params}

        assert self._process.stdin is not None
        assert self._process.stdout is not None

        self._process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self._process.stdin.flush()

        line = self._process.stdout.readline()
        if not line:
            stderr = self._process.stderr.read() if self._process.stderr else ""
            raise RuntimeError(f"MCP server sem resposta. STDERR: {stderr}")

        response = json.loads(line)
        if "error" in response:
            raise RuntimeError(response["error"]["message"])
        return response["result"]

    def search_vehicles(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        result = self._request("vehicles.search", filters)
        return result["vehicles"]
