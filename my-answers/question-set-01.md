# Question Set 01 — Service-company / mid-level (3 YOE) round

Drilled answers in my own words, polished. Format: Question → my answer → key follow-ups.

---

## 1. What's the difference between Docker and Kubernetes?

Docker is a containerization platform used to build container images and run containers
on a **single host**. Kubernetes is a container **orchestrator** that manages containers
across a **cluster of multiple nodes**. They're not competitors — they complement each
other: Docker packages and runs the container, Kubernetes runs it reliably at scale by
handling scheduling onto nodes, autoscaling, self-healing, service discovery, load
balancing, and rolling updates/rollbacks. Kubernetes uses a CRI-compatible container
runtime (containerd, CRI-O) to actually run the containers — it doesn't need Docker
specifically (dockershim was deprecated; images are OCI-standard).

**One-liner:** single-host (Docker) vs cluster-scale orchestration (K8s); complementary, not competing.

**Follow-up — Can you run K8s without Docker?**
Yes. K8s only needs a CRI-compatible runtime (containerd, CRI-O). Docker images are
OCI-standard, so any OCI runtime can run them.

---

## 2. How do you reduce downtime during deployments?

Pick a deployment strategy:
- **Rolling update** (default): gradually replaces old pods with new ones, only removing
  an old pod once the new one is ready and healthy — so capacity stays constant, zero downtime.
  Tune `maxUnavailable=0` and `maxSurge` to guarantee no capacity loss.
- **Readiness probes**: a new pod doesn't receive traffic until it passes readiness — a
  broken new version never gets added to the Service endpoints.
- **Canary**: shift traffic gradually (5% → 100%), watching metrics — limits blast radius.
- **Blue-green**: two identical environments (old=blue, new=green), switch traffic at once;
  instant rollback, but 2x resource cost.
- **Rollback**: if a deploy goes bad, `kubectl rollout undo` instantly reverts to the last
  working version — so a bad deploy doesn't cause extended downtime.

**When to use which:** rolling = default zero-downtime; canary = limit risk + watch metrics;
blue-green = instant switch/rollback, can afford 2x cost.

---

## 3. Readiness vs Liveness probe (+ what if confused)

- **Liveness** = "is the app alive?" Fails → **restart** the pod. (One-liner: "should I restart this?")
- **Readiness** = "is it ready to serve traffic?" Fails → **removed from Service endpoints**
  (no restart). (One-liner: "should I send it traffic?")

**If confused:**
- Liveness where you meant readiness → pod keeps **restarting** even when not truly dead →
  CrashLoopBackOff.
- Readiness where you meant liveness → a genuinely hung pod gets **pulled from traffic but
  never restarts** → sits dead, capacity silently lost, never self-heals.

---

## 4. What agents have you deployed? (ambiguous — clarify first)

"Agents" is ambiguous — clarify or acknowledge, then lead with the strongest.
Lead with the **AI monitoring agent** (see STAR story): Python + MCP protocol (pluggable to
any interface), used AI only for parameter extraction from natural language (NOT query
generation) to keep it fast/safe/accurate, fed into pre-built validated queries. Cut error
investigation from 30+ min to ~2 min, 100+ users incl. leadership.
Also genuine: Prometheus node-exporter (cluster metrics), self-hosted CI/CD runners.

---

## 5. 100 applications — how do you do log analysis?

Centralized logging pipeline (3 stages):
1. **Collect** — a log shipper (Fluent Bit / Fluentd) runs on every node as a **DaemonSet**,
   tails all pod logs, ships them out.
2. **Store + index** — logs land in an **indexed log store: Elasticsearch or Loki** (THIS is
   the "central location" — NOT S3/EFS, which have no search/indexing). S3 only for cheap archival.
3. **Visualize/query** — Kibana (with Elasticsearch) or Grafana (with Loki).

Named stacks: **EFK** = Elasticsearch + Fluent Bit + Kibana. **ELK** = Elasticsearch +
Logstash + Kibana. Cloud-native: CloudWatch Logs + Logs Insights.
Point: never SSH into 100 machines to grep — everything ships to one searchable place.

---

## 6. SRE vs DevOps

DevOps = a **culture/set of practices** improving dev-ops collaboration to deliver faster
via automation and CI/CD. SRE = an **engineering approach** to reliability/availability —
observability, incident management, SLOs, error budgets.
**Key framing:** "SRE is a specific *implementation* of DevOps" (class SRE implements
interface DevOps). Not competitors. Error budgets tie them together: within budget → ship
features; budget burned → focus on stability.
**Summary:** DevOps accelerates delivery; SRE ensures reliability.

---

## 7. On-prem → cloud migration + challenges

**6 R's** (pick one per app by business value/effort): Rehost (lift-and-shift), Replatform
(lift-and-reshape, e.g. DB→RDS), Repurchase (move to SaaS), Refactor (re-architect
cloud-native), Retire (decommission), Retain (keep on-prem).
**Phases:** Assess (inventory + dependency mapping) → Plan (strategy per app, sequence) →
Migrate (in waves, not big-bang) → Optimize (right-size, cost).
**Challenges:** data volume/transfer time, downtime/cutover, hidden dependencies, data
consistency during migration, networking (VPN/Direct Connect), security/compliance, cost surprises.
**500 TB transfer:** AWS **Snowball** (physical encrypted device shipped to you) — because
network transfer is bandwidth-capped and scales with volume (weeks/months for 500TB), while
physical shipping is ~constant time. DataSync for over-the-wire; Snowmobile (truck) for PB-scale.
**DB migration:** AWS **DMS** (full load + **CDC** for minimal downtime). Heterogeneous engine
(Oracle→Aurora PostgreSQL) needs **SCT** (Schema Conversion Tool) first, then DMS.

---

## 8. How does endpoint authentication work in Kubernetes?

Every API request goes through **3 stages in order**:
1. **AuthN (who are you?)** — client certificates, bearer/**ServiceAccount tokens** (pods),
   OIDC (external users). Fail → **401 Unauthorized**.
2. **AuthZ (what can you do?)** — **RBAC**: Roles/ClusterRoles define permissions,
   RoleBindings/ClusterRoleBindings grant them. Fail → **403 Forbidden**.
3. **Admission control** — final gate: **validating** (accept/reject, e.g. enforce resource
   limits) and **mutating** (modify, e.g. inject sidecar) controllers. Then persisted to etcd.

**KEY correction:** RBAC = **authorization**, NOT authentication. Pods authenticate via
**ServiceAccount tokens**.
