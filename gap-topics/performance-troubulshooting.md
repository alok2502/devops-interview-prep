# Gap Topic: Performance Troubleshooting (work OUTSIDE IN)

"App is slow" in a K8s/cloud context — diagnose in layers, don't jump straight to SSH+top.

## 1. Monitoring first (localize)
Grafana/Prometheus dashboards: WHICH service is slow? What KIND — CPU, memory, latency, error
rate? This tells you where to look before touching anything.

## 2. K8s layer
- **CPU throttling** — container hitting its CPU limit gets THROTTLED (slowed, not killed).
  Common cause of "slow." Check throttling metrics vs limits.
- **Memory pressure** — near memory limit → GC pressure / risk of OOMKill.
- **HPA** — is it scaling under load? If under-provisioned and not scaling, that's the issue.

## 3. Dependency layer
"App is slow" is often "something it CALLS is slow" — slow DB query (missing index, N+1),
downstream API, connection pool exhaustion. Check the dependencies.

## 4. Host / process layer (Linux)
- `top` / `htop` — CPU-hungry processes
- `uptime` — load average vs number of cores (load > cores = saturation)
- `df -h` (overall disk) / `du -sh` (folder-wise) — disk full/pressure
- `renice` — lower a non-critical process's priority; `kill -9` — kill a runaway

## 5. Fix per root cause
Raise resource limits, scale out (HPA/more nodes), fix the slow query, handle the process.

## Key reminder
When the question is in a CLOUD/K8s context, bring in cloud tools (monitoring, throttling, HPA,
dependencies) — not just Linux tools. Have both layers. Don't open with "I haven't faced this" —
own the approach confidently.
