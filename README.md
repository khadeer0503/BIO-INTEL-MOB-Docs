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
mint openapi-check openapi/wordpress.yaml
```

## Updating documentation

1. Add or edit an `.mdx` file.
2. Register its path (without `.mdx`) in `docs.json` under the appropriate section.
3. Preview with `mint dev`, validate, commit and push.
4. Connect the repository using Mintlify's Git settings for automatic deployment.

## API accuracy policy

The initial `openapi/wordpress.yaml` is a draft contract for the user-provided Rome GET endpoint. Verify its schema against the WordPress plugin route registrations and actual response payloads before treating it as authoritative. Add query parameters, writable endpoints, authentication mechanisms, and JSON fields only when the implementation supports them. The API playground uses interactive mode, as configured in `docs.json`.

## Publishing and security

Keep internal credentials, cookies, API keys, service endpoints not intended for public release, and personal data out of docs and examples. Documentation visibility is separate from GitHub repository visibility. Review Mintlify site access controls before publishing.

## Repository migration

The testing repository is `khadeer0503/BIO-INTEL-MOB-Docs`. To move it to `ctlup`, use GitHub's repository transfer workflow, subject to organization permissions, or push a complete clone to a new organization repository. After the move, update Mintlify's connected repository setting and GitHub App access.
