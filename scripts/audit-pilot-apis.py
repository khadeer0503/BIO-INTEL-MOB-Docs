"""Inspect public pilot REST metadata and dataset shapes without storing proposal data."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
PILOTS = json.loads((ROOT / "openapi/pilots.json").read_text(encoding="utf-8"))
ORIGIN = "https://ct-lup.mintlify.site"


def fetch(url, method="GET"):
    request_headers = {
        "Accept": "application/json", "User-Agent": "BIO-INTEL-MOB-docs-audit/1.0",
        "Origin": ORIGIN,
    }
    if method == "OPTIONS":
        request_headers["Access-Control-Request-Method"] = "GET"
    request = Request(url, method=method, headers=request_headers)
    try:
        with urlopen(request, timeout=20) as response:
            headers = {key: response.headers.get(key) for key in (
                "Access-Control-Allow-Origin", "Access-Control-Allow-Methods", "Access-Control-Allow-Credentials"
            )}
            return response.status, json.load(response) if method == "GET" else None, None, headers
    except HTTPError as error:
        return error.code, None, f"HTTP {error.code}", {}
    except (URLError, TimeoutError, ValueError, OSError) as error:
        return None, None, str(error), {}


def shape(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return {key: shape(item) for key, item in value.items()}
    if isinstance(value, list):
        unique = {json.dumps(shape(item), sort_keys=True) for item in value}
        return {"type": "array", "count": len(value), "itemShapes": [json.loads(item) for item in sorted(unique)]}
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    return "string"


def audit(pilot):
    name, server = pilot["name"], pilot["server"]
    index_status, index, index_error, _ = fetch(server + "/")
    namespace_status, namespace, namespace_error, _ = fetch(server + "/api")
    dataset_status, dataset, dataset_error, headers = fetch(server + "/api/datasets")
    options_status, _, options_error, options_headers = fetch(server + "/api/datasets", "OPTIONS")
    routes = {}
    if isinstance(index, dict):
        for route, metadata in index.get("routes", {}).items():
            if route == "/api" or route.startswith("/api/"):
                routes[route] = {key: metadata[key] for key in ("namespace", "methods", "endpoints", "schema") if key in metadata}
    valid_envelope = isinstance(dataset, dict) and all(
        key in dataset and isinstance(dataset[key], expected)
        for key, expected in (("id", int), ("city", str), ("generatedAt", str), ("proposals", list))
    )
    return {
        "pilot": name,
        "server": server,
        "discovery": {"status": index_status, "error": index_error, "namespaces": index.get("namespaces", []) if isinstance(index, dict) else [], "routes": routes},
        "projectIndex": {"status": namespace_status, "error": namespace_error, "namespace": namespace.get("namespace") if isinstance(namespace, dict) else None, "routes": list(namespace.get("routes", {})) if isinstance(namespace, dict) else []},
        "datasets": {"status": dataset_status, "error": dataset_error, "validEnvelope": valid_envelope, "city": dataset.get("city") if isinstance(dataset, dict) else None, "shape": shape(dataset) if dataset is not None else None, "cors": headers},
        "preflight": {"origin": ORIGIN, "status": options_status, "error": options_error, "cors": options_headers},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a metadata-only JSON audit report.")
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=8) as executor:
        pilots = list(executor.map(audit, PILOTS))
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "pilots": pilots}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for pilot in pilots:
        print(json.dumps({"pilot": pilot["pilot"], "discovery": pilot["discovery"]["status"], "projectIndex": pilot["projectIndex"]["status"], "datasets": pilot["datasets"]["status"], "city": pilot["datasets"]["city"], "routes": list(pilot["discovery"]["routes"]), "cors": pilot["datasets"]["cors"], "preflight": pilot["preflight"]}, ensure_ascii=False))
    return 0 if all(
        all(p[key]["status"] == 200 for key in ("discovery", "projectIndex", "datasets"))
        and p["preflight"]["status"] in (200, 204)
        and "GET" in p["discovery"]["routes"].get("/api/datasets", {}).get("methods", [])
        and p["projectIndex"]["namespace"] == "api"
        and p["datasets"]["validEnvelope"]
        and p["datasets"]["cors"].get("Access-Control-Allow-Origin") in (ORIGIN, "*")
        and p["preflight"]["cors"].get("Access-Control-Allow-Origin") in (ORIGIN, "*")
        and "GET" in p["preflight"]["cors"].get("Access-Control-Allow-Methods", "").replace(" ", "").split(",")
        for p in pilots
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
