# Gap Topic: AWS Multi-Account & Identity (no access keys)

## The building blocks
- **AWS Organizations** — groups multiple accounts under one org. Handles account structure,
  consolidated billing, org-wide guardrails via **SCPs** (Service Control Policies).
- **IAM Identity Center** (formerly AWS SSO) — the single sign-on front door. Connects to a
  corporate directory (Okta, Azure AD, or built-in). One login → list of accounts+roles you
  can assume.
- **STS (Security Token Service)** — issues **temporary credentials** when you assume a role.

## Multi-account secure access (no long-lived keys)
1. Organizations groups the accounts (+ SCP guardrails).
2. Identity Center gives one SSO login tied to corporate identity.
3. User assumes a role into a target account → STS temporary creds (auto-expire, scoped).
4. No stored access keys anywhere.
Classic underlying pattern: cross-account role assumption — central identity account, each
other account has a role that trusts it, you `sts:AssumeRole` for temp creds.

## Ways to log in to AWS (organize by WHO)
- Human: root (rare, MFA-locked), IAM user+password, federated/SSO (Identity Center / SAML / OIDC).
- Programmatic/CLI: IAM access keys (discouraged), assume role → STS temp creds (preferred).
- Service/workload: EC2 instance role, IRSA (EKS pods), Lambda execution role.

## Through-line
Temporary, role-based, auto-rotating credentials > long-lived stored keys. Same principle as
the EC2 instance role from Day 3, scaled to many accounts.
