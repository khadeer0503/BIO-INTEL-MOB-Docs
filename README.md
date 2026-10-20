# BIO-INTEL-MOB documentation

This repository contains the BIO-INTEL-MOB VR documentation, hosted with Mintlify.

## Prerequisites

- Node.js >= 20.17.0 (supported LTS preferred)

- Git

- Mintlify CLI: `npm install -g mint@latest`

## Preview

From the repository root:

```powershell
mint dev
```

Open <http://localhost:3000>.

## Validate

```powershell
mint validate
mint broken-links
```

## Updating documentation

1. Add or edit an `.mdx` file.
2. Register its path (without `.mdx`) in `docs.json` under the appropriate section.
3. Preview with `mint dev`, validate, commit and push.
4. Connect the repository using Mintlify's Git settings for automatic deployment.

## API accuracy policy

The API reference covers all eight BIO-INTEL-MOB pilots, with a shared server selector and dedicated sections per pilot. `openapi/pilots.json` defines the pilot names and URLs. `openapi/wordpress.yaml` defines the shared dataset and REST discovery contract; files in `openapi/pilots/` are generated from it.

Route registrations, response shapes, and documentation-origin CORS behavior were checked on 20 October 2026. The metadata-only snapshot is `api-reference/pilot-api-verification.json`. It records observed behavior, not undocumented backend validation rules. Add parameters, writable endpoints, authentication mechanisms, and fields only when the implementation supports them.

After changing the pilot registry or shared contract:

```powershell
npm ci
npm run api:generate
npm run api:check
mint validate
mint broken-links
```

To refresh the read-only deployment audit:

```powershell
python scripts/audit-pilot-apis.py --output api-reference/pilot-api-verification.json
```

The API playground uses interactive mode, as configured in `docs.json`. Each pilot section sends requests to that pilot's server. The shared section provides a server selector and preserves the original dataset reference URL.

## Publishing and security

Keep internal credentials, cookies, API keys, service endpoints not intended for public release, and personal data out of docs and examples. Documentation visibility is separate from GitHub repository visibility. Review Mintlify site access controls before publishing.

## Repository migration

The testing repository is `khadeer0503/BIO-INTEL-MOB-Docs`. To move it to `ctlup`, use GitHub's repository transfer workflow, subject to organization permissions, or push a complete clone to a new organization repository. After the move, update Mintlify's connected repository setting and GitHub App access.
