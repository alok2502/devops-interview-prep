# Gap Topic: On-Premises → Cloud Migration

## The 6 R's (map each app to one)
1. **Rehost** ("lift and shift") — move as-is to cloud VMs (VM→EC2). Fast/cheap, no cloud benefits.
2. **Replatform** ("lift and reshape") — minor optimizations (self-managed DB → RDS, containerize).
3. **Repurchase** — drop it, move to SaaS (self-hosted CRM → Salesforce).
4. **Refactor / Re-architect** — redesign cloud-native (monolith → microservices, serverless). Most benefit/effort.
5. **Retire** — decommission apps no longer needed.
6. **Retain** — keep on-prem for now (compliance / not worth it yet).

One-liner: "Assess each app and map it to one of the 6 R's by business value and effort."

## Phases
Assess (inventory + dependency mapping) → Plan (strategy per app, sequence least-critical
first) → Migrate (in waves, not big-bang) → Optimize (right-size, cost-optimize).

## Challenges (this is what the question asks)
1. Data volume/transfer time (TB/PB over network is slow)
2. Downtime / cutover (switch without taking business offline)
3. Hidden dependencies (App A secretly needs App B → breaks)
4. Data consistency during migration (source keeps changing while copying)
5. Networking (VPN, **Direct Connect**, IP/DNS changes)
6. Security & compliance (data residency, encryption, redo IAM)
7. Cost surprises (oversized lift-and-shift, egress costs)
8. Skills gap (team knows on-prem, not cloud)

## Big-data transfer
- **DataSync** — over the network (ongoing sync, good bandwidth, smaller/medium volumes)
- **Snowball** — physical encrypted ruggedized device shipped to you (TBs–low PBs).
  ~80TB/device (Edge). Why faster: network transfer is bandwidth-capped + scales with volume
  (500TB over 1Gbps ≈ 46 days); physical shipping is ~constant time regardless of size.
- **Snowmobile** — truck-sized container, up to ~100 PB (exabyte-scale).

## Database migration (common sub-question)
- **AWS DMS** (Database Migration Service): initial **full load** + **CDC** (Change Data
  Capture) to keep syncing ongoing changes → **minimal downtime**; source stays live.
- **Homogeneous** (same engine, Oracle→Oracle) = straightforward.
- **Heterogeneous** (Oracle→Aurora PostgreSQL) = use **SCT** (Schema Conversion Tool) FIRST
  to convert schema/procedures, THEN DMS for data.
- Targets: RDS (managed), Aurora (cloud-native), EC2-hosted (full control).

## Honest interview framing (if no real migration experience)
"I haven't personally led a migration, but I understand the approach — assess each app,
map to one of the 6 R's, migrate in waves. Main challenges: data volume, downtime/cutover,
hidden dependencies, consistency. For DBs, AWS DMS with CDC minimizes downtime, and SCT
handles engine changes." (Honest + demonstrates understanding > faking a story that collapses.)
