import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

SENSITIVE_HEADERS = {"authorization", "x-api-key", "api-key", "ocp-apim-subscription-key"}

@dataclass(frozen=True)
class RequestPlan:
    method: str
    url: str
    headers: dict[str, str]
    body: Any | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"method": self.method, "url": self.url, "headers": redact_headers(self.headers), "body": self.body}

def parse_key_value_pairs(values: list[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values or []:
        if "=" not in value:
            raise ValueError(f"Expected KEY=VALUE, got {value!r}")
        key, item_value = value.split("=", 1)
        if not key.strip():
            raise ValueError(f"Expected non-empty key in {value!r}")
        parsed[key.strip()] = item_value
    return parsed

def apply_path_params(path: str, values: dict[str, str]) -> str:
    result = path
    for key, value in values.items():
        result = result.replace("{" + key + "}", quote(value, safe=""))
    if "{" in result or "}" in result:
        raise ValueError(f"Missing path parameter for {path!r}")
    return result

def merge_query(url_or_path: str, values: dict[str, str]) -> str:
    if not values:
        return url_or_path
    parts = urlsplit(url_or_path)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update(values)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

def parse_json_body(body: str | None, body_file_content: str | None) -> Any | None:
    if body and body_file_content:
        raise ValueError("Use either --body or --body-file, not both.")
    source = body_file_content if body_file_content is not None else body
    if source is None:
        return None
    try:
        return json.loads(source)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Body must be valid JSON: {exc}") from exc

def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    return {key: ("<redacted>" if key.lower() in SENSITIVE_HEADERS else value) for key, value in headers.items()}

def endpoint_categories(endpoints: list[dict[str, str]]) -> list[str]:
    return sorted({item["category"] for item in endpoints})
