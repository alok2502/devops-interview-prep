# Gap Topic: Centralized Logging (log analysis across many apps)

## The problem
With N apps/servers, you can't SSH into each and grep. You need to ship all logs to ONE
searchable place.

## The 3-stage pipeline
1. **Collect** — a lightweight log shipper runs everywhere and forwards logs.
   Tools: **Fluent Bit**, Fluentd, Logstash, Filebeat, Vector.
   In Kubernetes: runs as a **DaemonSet** (one per node) tailing every pod's logs.
2. **Store + index** — logs go into an **indexed log store** (the "central location"):
   - **Elasticsearch** (full-text search)
   - **Loki** (Grafana's, lighter/cheaper, label-based)
   - Cloud: AWS **CloudWatch Logs** / OpenSearch
3. **Visualize + query** — **Kibana** (with Elasticsearch) or **Grafana** (with Loki),
   CloudWatch Logs Insights.

## Named stacks (interviewers ask by name)
- **EFK** = Elasticsearch + Fluent Bit + Kibana
- **ELK** = Elasticsearch + Logstash + Kibana
- **Loki stack** = Fluent Bit/Promtail → Loki → Grafana

## CRITICAL distinction (the thing people get wrong)
The "central location" is the **indexed log store (Elasticsearch/Loki)** — NOT S3 or EFS.
- S3/EFS = dumb storage (bytes/files) → no indexing, no search → useless for *analysis*.
- Elasticsearch/Loki = search-engine database for logs → parses + indexes so you can query
  "all ERROR logs from service X in last hour."
- S3's only role = cheap **archival** of old logs.

## Connects to
The "logs" pillar of observability (metrics=Prometheus, logs=this, traces=Jaeger).
Collector = DaemonSet.

## One-liner
"Ship all logs via Fluent Bit (DaemonSet) to an indexed store like Elasticsearch or Loki,
query via Kibana/Grafana — one searchable place instead of logging into each host."
