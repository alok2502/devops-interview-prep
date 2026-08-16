# Question Set 03 — Mid-level DevOps round (~3-5 YOE)

Conceptual + experience-based. Mostly in-wheelhouse. Format: Q → polished answer → key points.

---

## 1. How do you ensure High Availability in Kubernetes?

Remove single points of failure at every layer:
- **App:** multiple replicas + **pod anti-affinity** (spread replicas across nodes/AZs —
  replicas alone DON'T guarantee spread) + **PodDisruptionBudget** (protect during drains/upgrades).
- **Nodes:** multiple worker nodes across **Availability Zones** (zone failure ≠ outage).
- **Control plane:** multiple master nodes behind a **load balancer**.
- **Scaling:** **HPA** (scale pods on load) + cluster-autoscaler (scale nodes).
- **Data:** replicated / multi-AZ (RDS multi-AZ, or StatefulSet with replication).

---

## 2. replicas:3 — doesn't K8s guarantee different nodes? (follow-up)

No. `replicas: 3` guarantees the **count**, not the **placement** — the scheduler CAN stack
all 3 on one node, so that node's failure kills the app. **Pod anti-affinity** (or newer
**topology spread constraints**) forces distribution across nodes/AZs. HA must be designed, not assumed.

---

## 3. SLO, SLI, SLA — and why important

- **SLI** = Service Level *Indicator* — the measurement (e.g. % successful requests, latency).
- **SLO** = Service Level *Objective* — the internal target (e.g. 99.9%).
- **SLA** = Service Level *Agreement* — customer contract with penalties. Kept **looser** than
  SLO for breathing room.
- **Error budget = 100% − SLO** (allowed unreliability). Budget remaining → ship features;
  budget low → focus on reliability.
- **Why important:** makes reliability measurable + gives an objective, data-driven way to
  balance shipping speed vs stability.

---

## 4. Describe a recent major incident (STAR)

Pulled into a call — a service was down, throwing errors. Checked monitoring for scope +
timing → correlated with a recent change → logged into cluster, pods in CrashLoopBackOff →
**rolled back first** (`kubectl rollout undo`) to restore service → confirmed service up →
reproduced in staging → `describe` showed **exit code 1** (app-level, not OOM) → `kubectl logs
--previous` → **bad config value** → RCA to dev team → **prevention: readiness probe** (bad new
pods fail readiness → never added to Service endpoints → rollout stalls → old version keeps serving).
Delivery: slow down, hit STAR beats, don't rush.

---

## 5. Deployment setup in your org

Push → **CI**: checkout → lint/test → build Docker image → **Trivy scan** (gate on fixable
CRITICALs, `ignore-unfixed`) → push to registry (secrets pulled at runtime, not hardcoded).
**CD**: **GitOps via ArgoCD** — controller in-cluster watches Git, reconciles, pull-based
(cluster creds never leave cluster). Enrich with: environments (dev→staging→prod), rolling
updates + rollback, prod approval gate.

---

## 6. Max time for a node to start serving after failure (timeline)

Not instant — a sequence:
1. kubelet heartbeats every **10s** (`node-status-update-frequency`).
2. After **~40s** missed heartbeats (`node-monitor-grace-period`) → node marked **NotReady**.
3. After **~5 min** (`pod-eviction-timeout`, 300s) → pods evicted + rescheduled to healthy nodes.
The 5-min delay is **intentional** — avoids mass reschedule on transient blips (stability vs
fast-failover tradeoff; tunable). Ties to default `unreachable:NoExecute for 300s` toleration.
This is WHY pod anti-affinity matters — node recovery isn't instant.

---

## 7. Resolving high-performance issues (work OUTSIDE IN)

1. **Monitoring first** — Grafana/Prometheus: which service? CPU / memory / latency / errors?
   Localize before SSHing in.
2. **K8s layer** — CPU **throttling** vs limits (throttling slows, doesn't kill — Day 16),
   memory pressure, is **HPA** scaling under load?
3. **Dependency** — slow DB query / downstream API ("app slow" is often "DB slow").
4. **Host** — `top`/`htop` (CPU), `uptime` (load avg vs #cores), `df -h`/`du -sh` (disk),
   `renice` (lower priority) / `kill -9` (kill runaway).
5. Fix per root cause: raise limits, scale out, fix query, handle process.
(Don't lead with "I haven't faced this" — own the approach.)

---

## 8. Observability vs Monitoring

- **Monitoring** = watching **known/predefined** metrics + alerts you set up in advance
  ("is CPU > 80%?"). Tells you SOMETHING is wrong. Answers questions you knew to ask.
- **Observability** = ability to understand **unknown/unexpected** problems — ask NEW questions
  of the system's outputs. Tells you WHAT/WHY.
- **3 pillars** enable it: metrics (something's wrong) + logs (what) + traces (where).
- One-liner: monitoring = "is what I'm watching OK?"; observability = "something weird I never
  anticipated — why?"

---

## Still to cover in set 03 (next session)
Linux mount command; RCA when app down in cloud; master vs worker node down; VPC for HA;
scripting experience (→ AI agent); Terraform code experience; Docker experience (→ capstone);
**Terraform workspaces** (gap to fill).
