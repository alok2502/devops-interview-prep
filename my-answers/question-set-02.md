# Question Set 02 — AWS/EKS Identity & Access (senior/cloud-focused round, ~4-7 YOE level)

Theme: identity, access, and secrets in AWS/EKS. Temporary credentials as the through-line.

---

## 1. Bind an IAM user to an EKS role (IAM → K8s RBAC)

IAM and K8s RBAC are separate systems; EKS bridges them:
1. **IAM** authenticates the user (AWS-side, "who").
2. **`aws-auth` ConfigMap** (in `kube-system`) maps the IAM user/role **ARN** → a Kubernetes
   username + group.
3. **K8s RBAC** — a RoleBinding/ClusterRoleBinding grants that group permissions ("what").

Newer: **EKS Access Entries** — native EKS API to manage this without editing aws-auth
(less error-prone; a typo in aws-auth could lock everyone out).

---

## 2. 10 AWS accounts — secure login, no access keys

- **AWS Organizations** groups all accounts (+ org-wide guardrails via SCPs).
- **IAM Identity Center** (formerly AWS SSO) = single sign-on front door, connected to a
  corporate directory (Okta/Azure AD).
- Users log in once → **assume roles** into each account → get **temporary STS credentials**
  (auto-expiring, scoped). No long-lived keys.
- Underlying mechanism: cross-account role assumption via **STS**. Same principle as an EC2
  instance role — temporary/scoped/auto-rotating creds.

---

## 3. Ways to log in to AWS (organize by WHO)

- **Human:** root user + password (rare, locked down w/ MFA); IAM user + password;
  federated/SSO (IAM Identity Center or external IdP via SAML/OIDC).
- **Programmatic/CLI:** IAM access keys (discouraged now); assume IAM role → temporary STS
  credentials (preferred).
- **Service/workload:** IAM roles for services — EC2 instance role, IRSA for EKS pods,
  Lambda execution role.
- Through-line: temporary role-based creds > long-lived keys.

---

## 4. Does S3 require a VPC?

No. S3 is a **regional managed service that lives OUTSIDE the VPC**, accessed via its API,
controlled by IAM/bucket policies (not VPC networking). Bucket hosted in one region,
accessible globally with permissions.
**But:** a **VPC Gateway Endpoint for S3** lets VPC resources reach S3 **privately** over
AWS's internal network (no internet/NAT) — more secure, saves NAT/egress cost.

---

## 5. What happens when you run `terraform init`? (4 things)

1. Downloads **provider plugins** → `.terraform/`.
2. Initializes the **backend** (state storage); migrates local→remote if configured (prompts).
3. Downloads **modules** the config references.
4. Creates/updates **`.terraform.lock.hcl`** (pins provider versions for reproducibility).
Re-run when providers/modules/backend change.

---

## 6 & 7. Multi-region Terraform (provider aliases)

A provider block is single-region. For multiple regions use **provider aliases**:
- Define multiple `provider "aws"` blocks, each a different `region`; one default (no alias),
  others with `alias = "europe"` etc.
- On a resource, set `provider = aws.europe` to target that region.
- Resource with **no** `provider` argument → uses the **default** (unaliased) provider's region.
- AMIs are region-specific → look up per region with a data source.
- Scale via modules + passed providers.

**"Which region does an EC2 with no provider arg go to?"** → the default provider's region.

---

## 8. Frontend/backend/DB all in private subnets — how does a user access it?

- **ALB in the PUBLIC subnets** (internet-facing) accepts user traffic → routes to the
  **private** frontend → frontend→backend→DB all internal/private within the VPC.
- Only the load balancer is exposed; app tiers never directly reachable (security win).
- **Route 53** → points domain at the ALB.
- **Inbound = ALB; Outbound** (private instances → internet for updates/APIs) = **NAT gateway**.

---

## 9. EKS accessing AWS Secrets Manager → IRSA

**IRSA = IAM Roles for Service Accounts** (pod → AWS API access, no stored keys):
1. Enable **OIDC provider** on the cluster.
2. Create IAM role w/ Secrets Manager policy + trust policy for the cluster OIDC + SA.
3. **Annotate the ServiceAccount** with the role ARN (`eks.amazonaws.com/role-arn`).
4. Pods using that SA get **temporary STS creds** via OIDC → can read Secrets Manager.

Getting the secret INTO the pod (separate step): app reads via **SDK**, or **External
Secrets Operator** (syncs into a K8s Secret), or **Secrets Store CSI driver** (mounts as file).
IRSA = ACCESS; delivery = SDK/ESO/CSI. NOT aws-auth (that's cluster access).

---

## 10. Set up RBAC in EKS (2 layers)

1. **K8s RBAC:** Role/ClusterRole (what actions) + RoleBinding/ClusterRoleBinding (who — a
   K8s user/group).
2. **IAM bridge:** `aws-auth` ConfigMap (or Access Entries) maps IAM ARN → K8s user/group.
Flow: IAM authenticates → aws-auth maps ARN to group → RoleBinding grants that group perms.
**IRSA is NOT part of RBAC** — that's pod→AWS API access, a separate mechanism.

---

## The 3 EKS IAM mechanisms (KEEP SEPARATE — the key takeaway)
| Mechanism | Purpose |
|---|---|
| aws-auth / Access Entries | Human IAM identity → cluster access |
| K8s RBAC (Role + Binding) | K8s user/group → in-cluster permissions |
| IRSA (SA annotation + OIDC) | Pod → AWS API access |
