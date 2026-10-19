# Documentation synchronization

Pushes to `main` in `khadeer0503/BIO-INTEL-MOB-Docs` trigger a one-way push of
`main` and its Git history to `https://github.com/ctlup/BIO-INTEL-MOB-Docs.git`.
The copied workflow skips execution in the organization repository.

## Setup

1. Commit `.github/workflows/sync-to-organization.yml` and push it to the personal
   repository's `main` branch. Keep `.github/` out of `.gitignore` so GitHub can
   discover the workflow.
2. In the personal documentation repository, open **Settings > Secrets and
   variables > Actions** and add the repository secret `ORG_SYNC_TOKEN`.
   A repository secret configured in the Unity repository is not shared with
   this repository. Enter the token directly in GitHub, never in a source file.
3. The token must have access to `ctlup/BIO-INTEL-MOB-Docs` and permission to push
   contents and workflow files. For a fine-grained token, select resource owner
   `ctlup`, this destination repository, and **Contents: Read and write** plus
   **Workflows: Read and write**. Complete organization approval if required.
4. Ensure Actions is enabled in the source repository and destination branch
   rules permit the token owner to push `main`.
5. Open **Actions > Sync documentation to organization** to inspect the push run
   or use **Run workflow** on `main` to retry. A successful sync leaves both
   repositories' `main` branches at the same commit SHA.

## Troubleshooting

- No workflow listed: confirm the YAML is committed under `.github/workflows/`
  on the source repository's `main`, rather than only present on disk.
- Missing token: add `ORG_SYNC_TOKEN` to the personal documentation repository.
- Permission denied or repository not found: verify destination access, token
  permissions, organization approval, and branch rules.
- Non-fast-forward rejection: the destination has commits absent from the source.
  This workflow uses a regular push; reconcile the histories before retrying.
  Unlike the Unity workflow, it does not replace destination-only commits with a
  force push.

Synchronization copies Git history, not repository settings, secrets, or issues.
Verify a real Actions run before treating synchronization as operational.
