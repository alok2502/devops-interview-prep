# Gap Topic: SRE Cluster — Golden Signals, SLO Alerting, Error Budget, Burn Rate

Four connected concepts. Answer ~5 Altimetrik questions.

## 1. Four Golden Signals (LTES)
Google SRE's key metrics for any user-facing service (focus on these, not 100s of metrics):
- **Latency** — request time. Split SUCCESSFUL vs FAILED latency (a fast error still an error).
- **Traffic** — demand — requests/sec, throughput.
- **Errors** — rate of failed requests (500s, timeouts, wrong results).
- **Saturation** — how "full" resources are (CPU/mem/disk/queue depth) — closeness to capacity.
These become your SLIs. "I structure dashboards + alerts around the 4 golden signals."

## 2. SLI / SLO (connection)
- SLI = the measurement (e.g. % requests <300ms, % successful). Often a golden signal.
- SLO = the target (e.g. 99.9% success). Pick SLIs → set SLOs → alert on the SLO.

## 3. Error Budget
- **Formula: 100% − SLO.** The amount of failure ALLOWED.
- SLO 99.9% → 0.1% budget. Over 100M req/month = 100k allowed failures.
- **Decision it drives:** budget healthy → ship features / take risks; budget low → STOP shipping,
  focus stability/reliability. Objective, data-driven velocity-vs-reliability tradeoff.

## 4. SLO-Based Alerting + Burn Rate (the advanced part)
Problem with raw-threshold alerts ("CPU>80%!"): noisy, not tied to user impact.
SLO-based alerting instead alerts on **BURN RATE** = how fast you consume the error budget vs sustainable.
- Burn rate **1** = budget lasts EXACTLY the SLO window (e.g. 30 days). Sustainable. **IDEAL = 1 or below.**
- Burn rate **2** = burning 2x fast → budget gone in HALF the window (15 days).
- Burn rate **10** = month's budget gone in ~3 days. Serious.
- Consistently >1 → will breach SLO before window ends.

**Multi-window multi-burn-rate alerting (sophisticated):**
- Fast burn (e.g. 14x over 1hr) → PAGE immediately (budget destroyed fast, urgent).
- Slow burn (e.g. 1-2x over 6hr) → ticket/warning (gradual erosion).
Benefit: fewer false alarms (only alert on real budget consumption), urgency scaled to severity.

## Honest interview framing
"I structure monitoring on the 4 golden signals — latency, traffic, errors, saturation — with
dashboards + threshold alerts in Prometheus/Grafana. I understand SLO-based alerting: define
SLIs/SLOs, track error budget (100−SLO), alert on burn rate — how fast you consume the budget —
with multi-window alerts so fast burn pages and slow burn raises a ticket. I've done threshold
alerting hands-on; the full multi-burn-rate SLO alerting I understand and am keen to implement deeper."
