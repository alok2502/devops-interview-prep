# Gap Topic: ResourceQuota & LimitRange (multi-team resource governance)

Problem: multiple teams share a cluster — how do you stop one team from hogging all resources?
Answer: namespace per team + ResourceQuota + LimitRange.

## Setup: namespace per team
Give each team their own namespace → isolation + a boundary to apply quotas/limits to.

## ResourceQuota — caps a namespace's TOTAL usage
Limits the aggregate resources ALL pods in a namespace can consume:
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"              # can also cap object counts
```
So team-a's pods together can't exceed these totals. Blocks new pods that would breach the cap.
IMPORTANT: when a ResourceQuota for cpu/memory exists, every pod MUST specify requests/limits, or
it's rejected → that's where LimitRange helps.

## LimitRange — bounds INDIVIDUAL pods/containers
Sets default + min/max requests/limits per pod/container in a namespace:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: team-a-limits
  namespace: team-a
spec:
  limits:
    - type: Container
      default:               # applied if pod doesn't specify limits
        cpu: 500m
        memory: 512Mi
      defaultRequest:        # applied if pod doesn't specify requests
        cpu: 250m
        memory: 256Mi
      max:                   # no container can exceed
        cpu: "2"
        memory: 2Gi
      min:
        cpu: 100m
        memory: 128Mi
```

## How they work together (the key point)
- **LimitRange** ensures every pod HAS requests/limits (applies defaults + enforces min/max per pod).
- **ResourceQuota** enforces the namespace TOTAL.
- LimitRange makes ResourceQuota workable: since quota requires pods to declare requests/limits,
  LimitRange auto-provides defaults so pods aren't rejected.

## One-liner
"Namespace per team, then a ResourceQuota per namespace to cap each team's total CPU/memory and
object counts, plus a LimitRange to set default and min/max per pod. They complement each other —
LimitRange ensures every pod has limits, which ResourceQuota needs to enforce the namespace total."
