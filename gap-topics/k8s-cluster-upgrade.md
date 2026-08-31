# Gap Topic: Kubernetes Cluster Upgrade

## Order (THE key rule)
**Control plane FIRST, then worker nodes.** Version skew policy: workers can be BEHIND the control
plane (2-3 minor versions), NEVER ahead. Worker ahead of control plane → fails to register /
unpredictable (newer kubelet uses features/APIs the older control plane doesn't understand).
Can only go ONE minor version at a time (1.28→1.29→1.30, no skipping).

## Steps (managed — EKS/GKE)
1. **Check deprecated APIs** — biggest gotcha (below). Scan with kubent/pluto/kubectl-deprecations.
2. **Test in non-prod cluster first** (control-plane upgrades hard to roll back).
3. **Upgrade control plane** — managed (cloud handles master nodes); trigger via eksctl/console/TF.
4. **Upgrade add-ons** — CoreDNS, kube-proxy, CNI (VPC CNI) to compatible versions.
5. **Roll worker nodes** — few at a time (see below).
6. **Verify** — pods rescheduled, workloads healthy, add-ons working.

## Steps (self-managed — kubeadm)
`kubeadm upgrade plan` → `kubeadm upgrade apply` (control plane) → upgrade kubelet/kubectl on
control plane → drain + `kubeadm upgrade node` + kubelet on each worker → uncordon.

## Cordon / Drain / Uncordon
- **cordon** = mark node UNSCHEDULABLE (no NEW pods; existing pods stay). Just a flag.
- **drain** = EVICT all pods off (gracefully, respects PDB) → reschedule elsewhere. Auto-cordons first.
- **uncordon** = schedulable again after upgrade.
Node upgrade flow: cordon → drain → upgrade → uncordon.

## Rolling nodes (5-node example)
NEVER drain all at once (= outage, nowhere for pods to go). Do FEW at a time: drain node1 → pods
reschedule onto 2-5 → upgrade → uncordon → repeat. Need SPARE CAPACITY for drained pods → no
downtime. PodDisruptionBudget prevents over-eviction of one app's replicas.

## Node groups (blue-green upgrade — preferred)
Node group = managed pool of identical nodes (same type/version/AMI; EKS-managed node group / ASG).
Blue-green: (1) node group A on old version running workloads, (2) create node group B on NEW
version, (3) cordon+drain A → pods move to B, (4) delete A. Benefits: EASY ROLLBACK (A exists till
deleted), spin up whole correct-versioned pool at once, no mutating running nodes.
vs IN-PLACE = upgrade existing nodes one-by-one (cordon/drain/upgrade/uncordon each).
Analogy: in-place = renovate room by room while living in it; blue-green = build new house, move, demolish old.

## Challenges
1. **Deprecated/removed APIs** (#1) — K8s removes old API versions (Ingress extensions/v1beta1 →
   networking.k8s.io/v1). Old manifests break. Scan BEFORE with kubent/pluto (run from current,
   `--target-version 1.30` → checks your resources against removed-API DB, flags what'll break).
2. **Workload disruption on drain** — mitigate with PodDisruptionBudgets.
3. **Add-on compatibility** — CNI/CoreDNS/ingress must match new version.
4. **Stateful workloads** — StatefulSets/DBs need care on drain (PVC reattach).
5. **One minor at a time** — multi-version = sequential upgrades.
6. **Rollback hard** — control plane upgrades often not reversible → test non-prod first.
