# Gap Topic: Kafka (concept + ops)

## What it is / problem it solves
Distributed event streaming platform. Instead of services A→B→C→D wiring directly (tangled,
blocking), A publishes events to Kafka and B/C/D read from Kafka — DECOUPLED, neither knows the
other. A durable, high-throughput message log systems write to and read from.

## Components
- **Producer** — writes/publishes events to Kafka.
- **Consumer** — reads/subscribes to events.
- **Topic** — named category/feed of messages (e.g. "orders").
- **Partition** — topic split into partitions for SCALE/parallelism; spread across brokers.
  Ordered WITHIN a partition, no global order across partitions.
- **Broker** — a Kafka server; cluster = multiple brokers.
- **Replication** — each partition has a LEADER (handles R/W) + FOLLOWER replicas on other
  brokers. Leader's broker dies → follower promoted → HA, no data loss.
- **Consumer Group** — consumers split partitions among themselves for parallel consumption
  (1 partition → 1 consumer per group; max useful consumers = partition count).
- **ZooKeeper (old) / KRaft (new)** — cluster metadata/coordination. KRaft = Kafka's built-in
  consensus, no separate ZooKeeper.

## vs traditional message queue
Queue DELETES message after read. Kafka RETAINS for a configured retention period (ordered log +
consumer offsets) → consumers can RE-READ / REPLAY events. "A log you can replay, not a queue that forgets."

## Use cases
Event-driven microservices, data pipelines, log/metrics aggregation, stream processing, decoupling.

---

## OPS / DevOps angle

### Deploy / run
- **Managed** (easiest, most common): AWS MSK, Confluent Cloud, Aiven. Provision (Terraform),
  configure topics/access, monitor.
- **Self-managed on K8s**: **Strimzi operator** — declare Kafka cluster as a custom resource,
  operator handles brokers/scaling/rolling updates.
- Kafka is STATEFUL → runs as a **StatefulSet + persistent volumes** (stable identity + own disk
  for the log). THE example of why StatefulSets exist (vs Deployment).

### Monitor (JMX → Prometheus → Grafana → Alertmanager)
1. **Consumer lag** (#1 metric) — how far consumers are behind latest (produced offset − consumed).
   Growing lag = consumers can't keep up = problem. Alert on this first.
2. **Broker disk usage** — log stored on disk; full disk = broker down.
3. **Under-replicated partitions** — replicas out of sync / broker down = fault-tolerance risk.
4. **Partition/leader balance** across brokers; throughput (msgs/bytes in/out).

### Scale
- Throughput → add **partitions** (can't easily remove; affects ordering/keying; plan upfront).
- Cluster → add **brokers** + rebalance partitions (not automatic; reassignment / Cruise Control / Strimzi).
- Consumption → add **consumers** to a group (max useful = partition count).

### Common issues
Growing consumer lag (slow/stuck consumers → scale them), broker disk full (retention/traffic
spike), under-replicated partitions, rebalancing storms (consumers join/leave → pauses consumption),
broker failure (leaders fail over to replicas).

## One-liner
"Kafka is a distributed event streaming platform that decouples services — producers publish to
topics, consumers read, neither knows the other. Topics split into partitions across brokers for
scale, replicated for fault tolerance. Unlike a queue it retains messages so consumers can replay.
Operationally: managed (MSK) or self-managed on K8s via Strimzi as a StatefulSet with PVCs; monitor
consumer lag, disk, and under-replicated partitions via Prometheus/JMX; scale by adding partitions,
brokers, or consumers."
