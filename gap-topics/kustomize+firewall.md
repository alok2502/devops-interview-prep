# Gap Topics: Kustomize + Linux Firewall

## KUSTOMIZE

Template-FREE Kubernetes customization (Helm's alternative approach).

### Base + Overlays
```
myapp/
├── base/
│   ├── kustomization.yaml   # lists the base resources
│   ├── deployment.yaml      # plain YAML (replicas: 1)
│   └── service.yaml
└── overlays/
    ├── dev/kustomization.yaml    # references base + small patches
    └── prod/kustomization.yaml   # references base + patches (replicas: 5, namespace, image tag)
```

- **Base** = standard plain YAML + a `kustomization.yaml` listing the resources.
- **Overlay** = per-environment folder that references the base and applies PATCHES.
- Kustomize merges base + overlay patches → final YAML. No templates, no variables — pure YAML.

### Usage
```bash
kubectl apply -k overlays/prod/    # -k = kustomize, BUILT INTO kubectl (no install)
kubectl kustomize overlays/prod/   # render/preview the final YAML
```

### Kustomize vs Helm (the interview question)
| | Kustomize | Helm |
|---|---|---|
| Approach | Patches / overlays on plain YAML | Templates with {{ .Values }} |
| Templating | NO (pure YAML) | YES (Go templates + values.yaml) |
| Packaging | Not a package manager | Package manager (charts, repos, sharing) |
| In kubectl | YES (`kubectl -k`) | No (separate tool) |
| Rollback | No release tracking | Tracks releases, `helm rollback` |

One-liner: "Both do per-env config. Helm = templates + values, full package manager with
releases/rollback. Kustomize = template-free, plain-YAML base + patches per env, built into
kubectl. Kustomize simpler for straightforward customization; Helm more powerful for packaging.
Teams often use both — Kustomize for env overlays, Helm for third-party charts."

---

## LINUX FIREWALL — checking status

Three tools (depends on distro):
- **ufw** (Ubuntu/Debian): `sudo ufw status` (+ `verbose`) — active? + rules.
- **firewalld** (RHEL/CentOS/Fedora): `sudo firewall-cmd --state`, `--list-all`,
  `systemctl status firewalld`.
- **iptables** (low-level, underlies the others): `sudo iptables -L` (`-n -v` numeric/verbose).
  ufw & firewalld are friendly FRONT-ENDS to iptables. Newer systems = nftables/nft.

Interview answer: "Depends on distro — `ufw status` on Ubuntu, `firewall-cmd --state` on RHEL,
`iptables -L` at the low level. ufw/firewalld are front-ends to iptables. Also check
`systemctl status` on the firewall service."

Tie-in: firewall is a common "can't connect to port X" cause → check LOCAL firewall + AWS
Security Group (two layers).
