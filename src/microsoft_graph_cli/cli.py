import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .const import DEFAULT_AUTHORITY_HOST, DEFAULT_GRAPH_HOST, DEFAULT_SCOPE, DEFAULT_VERSION, ENDPOINTS, ENDPOINT_BY_KEY, ENV_ACCESS_TOKEN
from .transform import RequestPlan, apply_path_params, endpoint_categories, merge_query, parse_json_body, parse_key_value_pairs

class CliError(RuntimeError):
    pass

def print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))

def request_json(method: str, url: str, headers: dict[str, str], body: Any | None = None) -> Any:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = Request(url=url, method=method.upper(), headers=headers, data=data)
    try:
        with urlopen(req, timeout=60) as response:
            text = response.read().decode("utf-8")
            return json.loads(text) if text else {"status": response.status}
    except HTTPError as exc:
        raise CliError(f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
    except URLError as exc:
        raise CliError(f"Request failed: {exc.reason}") from exc

def token(args: argparse.Namespace) -> str:
    direct = args.access_token or os.getenv(ENV_ACCESS_TOKEN) or os.getenv("AZURE_ACCESS_TOKEN")
    if direct:
        return direct
    tenant = args.tenant_id or os.getenv("AZURE_TENANT_ID")
    client = args.client_id or os.getenv("AZURE_CLIENT_ID")
    secret = args.client_secret or os.getenv("AZURE_CLIENT_SECRET")
    if not all([tenant, client, secret]):
        raise CliError("Set MSGRAPH_ACCESS_TOKEN or AZURE_TENANT_ID, AZURE_CLIENT_ID and AZURE_CLIENT_SECRET.")
    body = urlencode({"client_id": client, "client_secret": secret, "grant_type": "client_credentials", "scope": args.scope}).encode("utf-8")
    req = Request(f"{args.authority_host.rstrip('/')}/{tenant}/oauth2/v2.0/token", method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=body)
    try:
        with urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))["access_token"]
    except Exception as exc:
        raise CliError(f"Could not acquire Microsoft Graph token: {exc}") from exc

def graph_url(args: argparse.Namespace, path: str, query: dict[str, str] | None = None) -> str:
    if path.startswith("https://"):
        url = path
    else:
        path = path if path.startswith("/") else f"/{path}"
        url = f"{args.graph_host.rstrip('/')}/{args.version}{path}"
    return merge_query(url, query or {})

def execute(args: argparse.Namespace, method: str, path: str, query: dict[str, str] | None = None, body: Any | None = None, extra_headers: dict[str, str] | None = None) -> int:
    url = graph_url(args, path, query)
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if extra_headers:
        headers.update(extra_headers)
    if args.dry_run:
        print_json(RequestPlan(method.upper(), url, headers, body).to_dict())
        return 0
    headers["Authorization"] = f"Bearer {token(args)}"
    print_json(request_json(method, url, headers, body))
    return 0

def cmd_endpoints(args: argparse.Namespace) -> int:
    items = [item for item in ENDPOINTS if not args.category or item["category"] == args.category]
    print_json({"categories": endpoint_categories(ENDPOINTS), "endpoints": items})
    return 0

def cmd_call(args: argparse.Namespace) -> int:
    path_params = parse_key_value_pairs(args.path_param)
    query = parse_key_value_pairs(args.query)
    headers = parse_key_value_pairs(args.header)
    body_text = None if not args.body_file else open(args.body_file, encoding="utf-8").read()
    body = parse_json_body(args.body, body_text)
    if args.endpoint:
        endpoint = ENDPOINT_BY_KEY.get(args.endpoint)
        if not endpoint:
            raise CliError(f"Unknown endpoint {args.endpoint!r}. Run 'msgraph endpoints'.")
        method = args.method or endpoint["method"]
        path = apply_path_params(endpoint["path"], path_params)
    else:
        if not args.path:
            raise CliError("Use --endpoint or --path.")
        method = args.method or "GET"
        path = apply_path_params(args.path, path_params)
    return execute(args, method, path, query, body, headers)

def cmd_users(args: argparse.Namespace) -> int:
    query = {"$top": str(args.top)}
    if args.select:
        query["$select"] = args.select
    if args.filter:
        query["$filter"] = args.filter
    return execute(args, "GET", "/users", query)

def cmd_managed_devices(args: argparse.Namespace) -> int:
    query = {"$top": str(args.top)}
    if args.select:
        query["$select"] = args.select
    if args.filter:
        query["$filter"] = args.filter
    return execute(args, "GET", "/deviceManagement/managedDevices", query)

def add_auth(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--access-token", help=f"Access token. Defaults to {ENV_ACCESS_TOKEN} or AZURE_ACCESS_TOKEN.")
    parser.add_argument("--tenant-id", help="Tenant ID. Defaults to AZURE_TENANT_ID.")
    parser.add_argument("--client-id", help="Client ID. Defaults to AZURE_CLIENT_ID.")
    parser.add_argument("--client-secret", help="Client secret. Defaults to AZURE_CLIENT_SECRET.")
    parser.add_argument("--scope", default=DEFAULT_SCOPE)
    parser.add_argument("--authority-host", default=DEFAULT_AUTHORITY_HOST)
    parser.add_argument("--graph-host", default=DEFAULT_GRAPH_HOST)
    parser.add_argument("--version", default=DEFAULT_VERSION, choices=["v1.0", "beta"])

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent-friendly Microsoft Graph command line toolkit.")
    add_auth(parser)
    subs = parser.add_subparsers(dest="command", required=True)
    endpoints = subs.add_parser("endpoints", help="List curated Microsoft Graph endpoints.")
    endpoints.add_argument("--category", choices=endpoint_categories(ENDPOINTS))
    endpoints.set_defaults(func=cmd_endpoints)
    call = subs.add_parser("call", help="Execute any Microsoft Graph request.")
    call.add_argument("--endpoint", choices=sorted(ENDPOINT_BY_KEY))
    call.add_argument("--method", choices=["GET", "POST", "PATCH", "PUT", "DELETE"])
    call.add_argument("--path")
    call.add_argument("--path-param", action="append")
    call.add_argument("--query", action="append")
    call.add_argument("--header", action="append")
    call.add_argument("--body")
    call.add_argument("--body-file")
    call.add_argument("--dry-run", action="store_true")
    call.set_defaults(func=cmd_call)
    users = subs.add_parser("users", help="List users with common query controls.")
    users.add_argument("--top", type=int, default=25)
    users.add_argument("--select")
    users.add_argument("--filter")
    users.add_argument("--dry-run", action="store_true")
    users.set_defaults(func=cmd_users)
    devices = subs.add_parser("managed-devices", help="List Intune managed devices.")
    devices.add_argument("--top", type=int, default=25)
    devices.add_argument("--select")
    devices.add_argument("--filter")
    devices.add_argument("--dry-run", action="store_true")
    devices.set_defaults(func=cmd_managed_devices)
    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (CliError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")

if __name__ == "__main__":
    sys.exit(main())
