# Question Set 04 — Mixed screening round (Linux, Python, Networking, Docker, K8s, AWS)

Format: Q → key answer points.

---

## NETWORKING

### IPv4 vs IPv6
IPv4 = 32-bit, 4 octets, DECIMAL dotted (192.168.1.1), each 0-255. IPv6 = 128-bit, 8 groups,
HEX colon-separated. WHY IPv6: IPv4 exhaustion (~4.3B addresses ran out). Coped via NAT +
private ranges (10.x, 172.16-31.x, 192.168.x = VPC ranges). IPv4 starts at 0.0.0.0.

### OSI model (APSTNDP top→bottom)
App (HTTP/DNS/SSH), Presentation (TLS/encrypt/format), Session, Transport (TCP/UDP + PORTS),
Network (IP + routing), Data Link (MAC/switches), Physical (cables). DevOps focus: L7 App
(Ingress/ALB), L4 Transport (Service/NLB), L3 Network (VPC/IP). KEY: Service=L4, Ingress=L7 IS OSI.

### Route53 public vs private hosted zone
PUBLIC = internet-facing DNS (www.company.com → public IP/ALB, anyone resolves). PRIVATE =
resolves only within associated VPC(s) (internal names, db.internal → private IP, not
internet-exposed). Why private: don't expose internal service names. Like K8s CoreDNS but VPC-level.

---

## LINUX

### Find files > 1GB
`find / -type f -size +1G` (+ = more than, units c/k/M/G). Time filters: -mtime (days),
-mmin (minutes). Combine: `find / -type f -size +1G -mtime +30`. Readable: `-exec ls -lh {} \;`.
Real use: find disk space hogs.

### Find ERROR case-insensitive in file
`grep -i error file.txt`. Flags: -i (ignore case), -r (recursive), -n (line numbers), -c (count),
-v (invert/exclude), -w (whole word), -A/-B/-C N (context). Chain: `grep -i error app.log | grep -i db`.

### First-time login to Linux machine
SSH in: `ssh -i key.pem user@public-ip` (default user by OS: ubuntu/ec2-user/admin). THEN:
update/upgrade packages, harden (disable root login, key-only auth), create non-root user, setup.

### Can't access Linux machine (layered troubleshooting)
(1) Instance running? (console — stopped/terminated? health checks?). (2) Network: SG port 22
from my IP? NACL/routing/public IP? (3) Creds: right key/user? chmod 400 on .pem? (4) Box: SSH
service down / out of resources → EC2 serial console or SSM Session Manager (get in w/o SSH).
SG port 22 = #1 cause. chmod 400 = common gotcha.

---

## PYTHON

### 5/2 vs 5//2
5/2 = 2.5 (true division, float). 5//2 = 2 (floor division, int).

### a=[0] b={0} → a[0] and b[0]
a[0] = 0 (LIST, ordered, indexable). b[0] = TypeError! {0} is a SET (unordered, NOT
subscriptable, auto-removes dupes, fast membership). {0:"x"}=dict, {}=empty dict, set()=empty set.

### Set vs List
List [..] = ordered, indexable, duplicates OK. Set {..} = unordered, NOT indexable, unique only,
fast membership (x in s). Use list for sequence, set for uniqueness/membership.

### IPv4 validator (FLAG PATTERN — see python-scripts/valid_ipv4.py)
is_valid=True → check len==4 → loop: .isdigit() (reject non-numeric) AND 0-255 → flip False on
any fail → decide once. Best as function returning bool (return False = early exit).

### Failed jobs filter (see python-scripts/failed_jobs.py)
Loop list of dicts, if status=="FAILED" append job_id, return list → [102,103].
One-liner (comprehension): `[log["job_id"] for log in logs if log["status"]=="FAILED"]`
Structure: [COLLECT for ITEM in LIST if CONDITION]. Comprehensions = fluency signal.

---

## DOCKER

### CMD vs ENTRYPOINT
Both define what runs at start. CMD = default, fully REPLACED if you pass args to `docker run`.
ENTRYPOINT = fixed, always runs, args APPEND to it. Combo (best): ENTRYPOINT ["python"] +
CMD ["app.py"] → default `python app.py`; `docker run img other.py` → `python other.py`
(CMD replaced, ENTRYPOINT stays). ENTRYPOINT = fixed part (binary), CMD = changeable part (script/flags).

---

## KUBERNETES

### K8s on a laptop without EKS/AKS?
Yes. EKS/AKS/GKE = MANAGED k8s (provider runs control plane). K8s is open-source, self-host
anywhere: VMware VMs + kubeadm, or kind (k8s-in-Docker), minikube, k3s for local. Managed ≠ only way.

### CI/CD
CI = automated checks on push (lint/test/scan) to catch bugs early. CD = continuous DELIVERY
(ready to ship, human approval gate) vs continuous DEPLOYMENT (fully auto).

### K8s architecture
CONTROL PLANE: API server (brain — all requests + all components watch it), etcd (key-value
store for cluster state, only API server writes), controller manager (runs controllers:
replicaset/deployment/node), scheduler (picks node for pods). DATA PLANE (workers): kubelet
(receives pod specs, ensures containers run via runtime, reports status), container runtime
(containerd/CRI-O — pulls images, runs containers), kube-proxy (Service networking/routing).
Runtime pluggable via CRI.

---

## Still to cover from this set (next time)
- Check firewall protection (Linux)
- Kustomize file creation (possible gap)
- Directory-monitor script (Python — watch dir, print new files every minute)
- SQL: customers with >3 orders in last 90 days (JOIN + GROUP BY + HAVING)
