# Gap Topic: Node Failure → Pod Rescheduling Timeline

When a node fails, pods do NOT move instantly. Sequence of timeouts:

1. **Heartbeat interval** — kubelet reports status every **10s** (`node-status-update-frequency`).
2. **NotReady** — after **~40s** of missed heartbeats (`node-monitor-grace-period`), the node
   controller marks the node **NotReady**.
3. **Pod eviction** — after **~5 min** (`pod-eviction-timeout`, default 300s) of NotReady, pods
   are evicted and rescheduled onto healthy nodes.
4. **Reschedule** — scheduler places pods on healthy nodes → image pull + startup.

## Why the 5-minute delay?
Intentional — prevents mass rescheduling on a **transient blip** (brief network glitch). It's a
tradeoff: fast failover vs stability. Tunable (`pod-eviction-timeout`) if you need faster
failover, but risks churn on flaky networks.

## Connection
- The default pod toleration `node.kubernetes.io/unreachable:NoExecute for 300s` IS this 5-min grace.
- This is WHY pod anti-affinity + multiple replicas matter: node recovery isn't instant, so if
  all replicas sat on the dead node you're down ~5 min. Spread → survivors serve immediately.

## Interview answer
"It's a sequence, not instant: kubelet heartbeats every 10s; after ~40s of missed heartbeats
the node is NotReady; after a ~5-min eviction timeout pods reschedule to healthy nodes. The
5-min delay is deliberate — it avoids unnecessary rescheduling on transient blips. You can tune
it down for faster failover if needed."
