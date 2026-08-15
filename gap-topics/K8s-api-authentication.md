# Gap Topic: Kubernetes API Authentication (endpoint auth)

## Every API request → 3 stages IN ORDER
```
Request → [AuthN: who?] → [AuthZ: what?] → [Admission: should this?] → etcd
             fail=401         fail=403          fail=rejected
```

## Stage 1 — Authentication (AuthN): "WHO are you?"
Verifies identity only. Methods:
- **Client certificates** (mutual TLS — users/admins, often in kubeconfig)
- **Bearer tokens** — incl. **ServiceAccount tokens** → how **PODS** authenticate (token
  mounted into the pod)
- **OIDC** — external identity providers (Google, Azure AD, Okta) for human users
- Webhook / auth proxy (custom)
Note: K8s has NO built-in human "user" objects — humans via certs/OIDC. ServiceAccounts ARE
K8s objects — identity for pods/workloads.
Fail → **401 Unauthorized**.

## Stage 2 — Authorization (AuthZ): "WHAT can you do?"
**RBAC**: Roles/ClusterRoles (permissions) + RoleBindings/ClusterRoleBindings (grant to
identity). Checks verb + resource + namespace.
Fail → **403 Forbidden**.

## Stage 3 — Admission Control: "SHOULD this be allowed / modified?"
- **Mutating** controllers — modify request (inject sidecar, set defaults)
- **Validating** controllers — accept/reject (enforce "all pods must have limits")
Then persisted to etcd.

## KEY correction (common mistake)
**RBAC = AUTHORIZATION (stage 2), NOT authentication.** AuthN (who) comes first via
certs/tokens/ServiceAccounts/OIDC. Pods authenticate via **ServiceAccount tokens**.

## One-liner
"3 stages: AuthN (identity — certs/tokens/SA/OIDC, 401 if fail) → AuthZ (RBAC — what you can
do, 403 if fail) → Admission controllers (validate/mutate) → etcd."
