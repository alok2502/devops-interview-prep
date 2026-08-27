# Question Set 05 — K8s Scenarios + Automation (troubleshooting-heavy)

Format: Q → key answer points.

---

## 1. HPA not scaling (pod-level autoscaling not happening)
Diagnose: (1) `kubectl describe hpa` FIRST — shows current vs target metrics + errors, points at
cause. (2) metrics-server running? `kubectl top pods` (HPA needs it for CPU/mem). (3) resource
REQUESTS defined? HPA computes utilization as % of requests — no requests = no denominator = no
scaling. (4) maxReplicas cap hit? (5) can new pods schedule or is cluster at capacity? (describe
pod events). Order: HPA status → metrics → requests → cap → scheduling.

## 2. HPA was working, suddenly broke
Incident mindset — ask "WHAT CHANGED?": (1) `describe hpa` (current error). (2) recent deploy?
`rollout history` — removed/zeroed requests, changed HPA min/max/target. (3) metrics-server pod
still healthy? (was fine, now crashed/evicted). (4) hit maxReplicas as load grew (capped, looks
broken). (5) recent cluster upgrade broke metrics API. "Suddenly" → recent change or newly-hit limit.

## 3. Ingress configured but app not accessible
Trace request path IN ORDER (outside-in): (1) DNS — domain resolves to ingress LB IP? (nslookup;
external/Route53, not CoreDNS). (2) LB reachable — external IP + SG/firewall allows 80/443? (3)
Ingress CONTROLLER pod healthy? (no controller = ingress does nothing). (4) `describe ingress` —
host/path rules right, point to right svc+port? (5) Service exists, right port? (6) `kubectl get
endpoints` — has healthy pod IPs? EMPTY = #1 cause (selector mismatch / unready pods). (7) backend
pods Running + ready? Hop-by-hop isolates the break.

## 4. Kubernetes service discovery
Two layers: (1) Service + labels/selectors → endpoints (tracks current pod IPs, auto-updates as
pods die/restart, stable ClusterIP over ephemeral pods — solves changing-IP problem). (2) CoreDNS
(cluster DNS) → each Service gets DNS name `service.namespace.svc.cluster.local` → resolves to
ClusterIP. Pods reach services BY NAME (never hardcode pod IPs) → DNS → ClusterIP → service
load-balances to healthy endpoints.

## 5. Ensure 5 teams don't exceed a resource amount
Namespace PER team → ResourceQuota per namespace (caps team's TOTAL cpu/mem + object counts) +
LimitRange (default + min/max per individual pod/container). They complement: LimitRange ensures
every pod HAS requests/limits → ResourceQuota can then enforce the namespace total.
(See gap-topics/resourcequota-limitrange.md)

## 6. Leap second in Linux
(See gap-topics/leap-second.md) Occasional +1 sec to UTC for Earth's irregular rotation → minute
briefly has 61 sec. Breaks software assuming 60-sec minutes. Fix: leap smearing (spread over
hours; AWS/Google NTP).

## 7 & 8. Automation you've done (K8s + time-saver) — BOTH halves
K8s automation: CI/CD (GitHub Actions build/scan/push) + GitOps/ArgoCD (push to Git → auto-sync to
cluster, self-heal, no manual kubectl) + Helm. Time-saver showcase: AI monitoring agent (Python +
MCP, LLM extracts params → fills pre-tested queries, NOT AI-heavy = reliable, 100+ users incl
leadership, 30min→2min). Answer BOTH halves — don't skip the K8s one.

## 9. securityContext trap — runAsNonRoot:true + runAsUser:0
CONTRADICTION. runAsUser:0 = root; runAsNonRoot:true = must NOT be root. Result: pod SCHEDULES but
container FAILS to start (kubelet detects UID 0 violates runAsNonRoot → CreateContainerConfigError,
"container has runAsNonRoot and image will run as root"). Key nuance: scheduled ≠ running.
runAsNonRoot VALIDATES (rejects root), doesn't SET a UID; runAsUser SETS the UID.
