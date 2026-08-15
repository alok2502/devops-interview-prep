# Gap Topic: EKS ↔ IAM Access — the 3 mechanisms (KEEP SEPARATE)

The hardest part of EKS access: three different IAM↔EKS bridges, for three different purposes.
People constantly muddle them. Keep them straight:

| Mechanism | Purpose | Connects |
|---|---|---|
| **aws-auth / Access Entries** | Cluster access for **humans** | IAM identity → K8s user/group |
| **K8s RBAC** (Role + Binding) | Permissions **inside** cluster | K8s user/group → what they can do |
| **IRSA** (SA annotation + OIDC) | **Pod** → AWS API access | ServiceAccount → IAM role |

---

## 1. aws-auth ConfigMap (IAM identity → cluster access)
- ConfigMap in `kube-system`. Maps IAM user/role **ARN** → a K8s username + group.
  - `mapUsers` for IAM users, `mapRoles` for IAM roles.
- The classic way to let an IAM identity access the cluster (run kubectl).
- Error-prone (a typo can lock everyone out) → newer **EKS Access Entries** = native EKS API,
  no ConfigMap editing.

## 2. K8s RBAC (K8s user/group → permissions)
- Role (namespaced) / ClusterRole (cluster-wide) = the permissions (verbs + resources).
- RoleBinding / ClusterRoleBinding = grant to a subject (the K8s user/group from aws-auth).

## Setting up RBAC in EKS = #1 + #2 together
IAM authenticates → aws-auth maps ARN → K8s group → RoleBinding grants that group its perms.

## 3. IRSA — IAM Roles for Service Accounts (pod → AWS API)
COMPLETELY SEPARATE from RBAC. Lets a POD call AWS APIs (S3, Secrets Manager) without keys.
1. Enable **OIDC provider** on the cluster (the trust mechanism).
2. Create IAM role: policy (e.g. secretsmanager:GetSecretValue) + trust policy for cluster
   OIDC + the specific ServiceAccount.
3. **Annotate the ServiceAccount**: `eks.amazonaws.com/role-arn: <role-arn>`.
4. Pods using that SA get temporary STS creds via OIDC → call AWS APIs, no stored keys.

### Getting a Secrets Manager secret INTO the pod (separate from IRSA access):
- App reads directly via **AWS SDK** (using IRSA creds)
- **External Secrets Operator (ESO)** — syncs the secret into a native K8s Secret
- **Secrets Store CSI driver** — mounts the secret as a file in the pod

## The trap to avoid
"Set up RBAC" → do NOT reach for IRSA. IRSA is pod→AWS, not user→cluster-permissions.
