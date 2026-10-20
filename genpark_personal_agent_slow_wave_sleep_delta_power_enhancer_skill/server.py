# -*- coding: utf-8 -*-
"""MCP Server for Slow-Wave Sleep Delta Power & Glymphatic Clearance Enhancer Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import SlowWaveSleepDeltaPowerEnhancer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "audit_deep_sleep_delta_power",
        "description": "Analyze wearable slow-wave sleep duration and nocturnal delta power percentage against clinical glymphatic waste clearance benchmarks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "total_sleep_time_minutes": {
                    "type": "integer"
                },
                "slow_wave_sleep_minutes": {
                    "type": "integer"
                },
                "awakenings_count": {
                    "type": "integer"
                },
                "average_resting_hr_bpm": {
                    "type": "integer"
                }
            },
            "required": [
                "total_sleep_time_minutes",
                "slow_wave_sleep_minutes",
                "awakenings_count"
            ]
        }
    },
    {
        "name": "generate_thermal_and_acoustic_sws_protocol",
        "description": "Generate dynamic smart bedroom thermostat cooling curve (66\u00b0F to 64\u00b0F) and 1/f pink noise auditory stimulation cadence.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_deep_sleep_boost_pct": {
                    "type": "number"
                },
                "bedtime_hour_24h": {
                    "type": "integer"
                }
            },
            "required": [
                "bedtime_hour_24h"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-slow-wave-sleep-delta-power-enhancer-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(SlowWaveSleepDeltaPowerEnhancer, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-personal-agent-slow-wave-sleep-delta-power-enhancer-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-slow-wave-sleep-delta-power-enhancer-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
