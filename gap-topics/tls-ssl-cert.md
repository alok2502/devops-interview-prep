# Gap Topic: TLS/SSL & Certificate Management (K8s)

## How TLS/SSL works (fundamentals)
Two jobs: **ENCRYPT** traffic (privacy) + **AUTHENTICATE** the server (identity). It's the "S" in HTTPS.
- Server has a **private key** (secret) + **public certificate** (shared).
- Certificate is signed by a **Certificate Authority (CA)** — trusted third party (Let's Encrypt,
  DigiCert). The CA signature is what makes clients trust it.
- **Handshake:** client connects → server sends cert → client verifies (trusted CA? valid? right
  domain?) → they agree a session key via asymmetric crypto → traffic encrypted with fast
  symmetric session key.
- Key insight: asymmetric keys establish trust + exchange session key ONCE; then symmetric key
  encrypts actual data (faster). Trust rests on CAs.

## TLS in Kubernetes
1. Store cert + key as a **TLS Secret** (`kubernetes.io/tls`):
   `kubectl create secret tls my-tls --cert=cert.pem --key=key.pem`
2. Reference it in the **Ingress `tls` section** (secretName + hosts).
3. **Ingress controller TERMINATES TLS** — handles HTTPS/decryption at the edge, forwards to
   services internally (usually plain HTTP inside cluster).

## Automation: cert-manager
Managing certs by hand is painful (Let's Encrypt certs expire ~90 days). **cert-manager**:
- Installed in cluster, integrates with a CA like **Let's Encrypt** (free, automated).
- Define an **Issuer/ClusterIssuer** (which CA) → cert-manager auto requests, issues, stores (as
  TLS Secret), and RENEWS before expiry. No manual cert rotation.

## Interview answer
"Store the cert+key as a TLS Secret, reference it in the Ingress tls section so the Ingress
controller terminates TLS. For managing certs at scale, cert-manager automates issuing and
renewing from a CA like Let's Encrypt — stored as Secrets, renewed before expiry, no manual work."
