# Question Set 06 — Altimetrik (senior, deep) — PART 1

Harder/deeper set: Terraform, observability/SRE, resume-claim questions. (Multi-day set.)

---

## 1. Import a manually-created resource into Terraform
`terraform import` — brings resource into STATE, does NOT generate config. Workflow: (1) write
resource block in .tf, (2) `terraform import <type>.<name> <resource-id>`, (3) `terraform plan` →
fill config until no changes (else apply may destroy/modify). Modern (TF 1.5+): declarative
`import {}` block + `terraform plan -generate-config-out=file.tf` to scaffold config.

## 2. Exposure to Dev/QA/Prod environments
dev → cap/pt → uat → staging(prod replica) → prod. CI/CD promotes code up. Release branches for
accumulated changes. Test on prod-replica before go-live. Per-env config differs (dev small/cheap,
prod full-scale HA — separate values files / TF workspaces/vars). Prod access tighter — approval
gates, change management.

## 3. Software architecture components + flow
LB (distribute traffic, round-robin/path-based) → Web Server (nginx/Apache — STATIC content +
reverse proxy) → App Server (Tomcat/Node — dynamic BUSINESS LOGIC) → Database (persistent; SQL vs
NoSQL; read replicas). + Caching (Redis/CDN — reduce load/latency). Integrations = external
services app calls (payment, 3rd-party APIs, queues). Flow: LB→web→app→DB→back.

## 4. Alerts, logging, incident/problem resolution
ALERTS = Prometheus threshold alerts (CPU/mem/error-rate/latency) → Alertmanager (routing + group
+ dedup) → Teams/mail. LOGGING = Fluent Bit DaemonSet → Elasticsearch/Loki (store+index) →
Grafana/Kibana. INCIDENT = STAR (monitoring→rollout history→rollback to restore→reproduce→describe
→exit 1=app/config→RCA→readiness probe). ITIL distinction: INCIDENT (restore fast) vs PROBLEM
(RCA + prevent recurrence).

## 5. Production system sizing/provisioning/setup/maintenance/closure
SIZING (load testing → CPU/mem → node count for HA → ResourceQuota/LimitRange + requests/limits,
requests=HPA denominator). PROVISIONING (Terraform modules, ASG node scaling, S3+DynamoDB state).
SETUP (Ansible config, Helm per-env values, ArgoCD GitOps; +CI/CD build→scan→push). MAINTENANCE
(dashboards, Prometheus+Alertmanager alerts, cluster upgrades). CLOSURE (boto3 cleanup scripts for
stale VMs/EBS, manual checks, stop unneeded instances).

## Gap topics filled today
- K8s cluster upgrade → gap-topics/k8s-cluster-upgrade.md
- SRE golden signals / SLO alerting / error budget / burn rate →
  gap-topics/sre-golden-signals-slo-burn-rate.md

## Still to cover (next session — Altimetrik part 2)
- Infra admin: licensing, billing, cost reduction, security
- Helm deep-dive: walk through actual charts + what's in values.yaml
- GKE deployment troubleshooting (pod error/terminating — troubleshooting approach)
- Observability tools/frameworks used; creating dashboards + alerts (golden signals)
- Terraform: deploy cluster nodes; write VPC + subnet (public/private) live
- Resume claims: optimized K8s deployment configs; blameless postmortem framework; MTTR reduction automation
