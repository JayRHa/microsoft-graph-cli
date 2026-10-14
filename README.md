<!-- jr-brand:start -->
<p align="center">
  <a href="https://jannikreinhard.com/">
    <img src="https://raw.githubusercontent.com/JayRHa/.github/main/assets/readme/brand-header.png" alt="Jannik Reinhard — I help enterprises ship secure AI agents" width="100%">
  </a>
</p>
<p align="center">
  <a href="https://jannikreinhard.com/">Website</a> ·
  <a href="https://www.linkedin.com/in/jannik-r/">LinkedIn</a> ·
  <a href="https://x.com/jannik_reinhard">X</a> ·
  <a href="https://www.youtube.com/@jannikreinhard">YouTube</a>
</p>
<!-- jr-brand:end -->

# Microsoft Graph CLI

**Type:** Tool or application · **Status:** Community project

## Overview

Agent-friendly Microsoft Graph requests from the terminal with predictable JSON output.

Query. Inspect. Automate.


Microsoft Graph | Python CLI | JSON-first | Agent Ready

Microsoft Graph CLI is a small command line toolkit for working with Microsoft Graph in scripts, terminals and AI-agent workflows. It provides a curated endpoint catalog for common Microsoft 365, Entra ID and Intune reads, plus a generic `call` command for any Graph path.

The tool is intentionally simple: authentication can come from an existing access token or Azure client credentials, every command emits deterministic JSON, and `--dry-run` prints the exact request before touching a tenant.

## Quickstart

```bash
git clone https://github.com/JayRHa/microsoft-graph-cli.git
cd microsoft-graph-cli
python -m pip install -e .

export MSGRAPH_ACCESS_TOKEN="<access-token>"
msgraph endpoints
msgraph users --top 5 --select id,displayName,userPrincipalName
```

Use client credentials instead of a prebuilt token:

```bash
export AZURE_TENANT_ID="<tenant-id>"
export AZURE_CLIENT_ID="<app-registration-client-id>"
export AZURE_CLIENT_SECRET="<client-secret>"

msgraph managed-devices --top 10 --dry-run
```

## How It Works

```mermaid
flowchart LR
    Agent[Human or AI agent] --> CLI[msgraph CLI]
    CLI --> Auth[Token from env or client credentials]
    CLI --> Plan[Dry-run request plan]
    CLI --> Graph[Microsoft Graph]
    Graph --> JSON[Structured JSON output]
    JSON --> Agent
```

## Commands

| Command | Purpose |
| --- | --- |
| `msgraph endpoints` | List curated endpoint keys, paths and required Graph permission scopes. |
| `msgraph call` | Execute any Microsoft Graph request by endpoint key or raw path. |
| `msgraph users` | List users with common `$top`, `$select` and `$filter` controls. |
| `msgraph managed-devices` | List Intune managed devices through Microsoft Graph. |

## Examples

```bash
msgraph endpoints --category intune
msgraph call --endpoint user --path-param id=alex@example.com --dry-run
msgraph call --method GET --path /organization
msgraph call --endpoint sign-ins --query '$top=10' --query '$filter=createdDateTime ge 2026-05-01T00:00:00Z'
```

## Authentication

The CLI checks authentication in this order: `--access-token`, `MSGRAPH_ACCESS_TOKEN`, `AZURE_ACCESS_TOKEN`, then client credentials from `AZURE_TENANT_ID`, `AZURE_CLIENT_ID` and `AZURE_CLIENT_SECRET`.

## Output Contract

All successful commands write JSON to stdout. Errors are written to stderr with a non-zero exit code, which makes the CLI predictable for shell scripts, CI jobs and agent toolchains.

## License

MIT License. See [LICENSE](LICENSE).

<!-- jr-brand-footer:start -->
---

[Articles and guides](https://jannikreinhard.com/) · [Repository index](https://github.com/JayRHa/.github/blob/main/REPOSITORIES.md)
<!-- jr-brand-footer:end -->
