# Gap Topic: Helm (Kubernetes package manager)

## What it is / problem it solves
Helm = **package manager for Kubernetes** ("apt/yum for K8s"). Deploying an app means many YAML
files (Deployment, Service, ConfigMap, Secret, Ingress, PVC...). Managing those across
environments by hand is painful. Helm packages them into one reusable, parameterized unit = a **chart**.

## Core concepts
**Chart** — a package of pre-configured K8s resources:
```
mychart/
├── Chart.yaml        # metadata (name, version)
├── values.yaml       # DEFAULT config values
├── templates/        # templated K8s manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── charts/           # dependencies (sub-charts)
```

**Templates + Values (the key idea)** — templatize values instead of hardcoding:
```yaml
# templates/deployment.yaml
spec:
  replicas: {{ .Values.replicaCount }}
  containers:
    - image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```
```yaml
# values.yaml
replicaCount: 3
image: { repository: myapp, tag: "1.2.0" }
```
Same chart deploys differently per environment — just pass different values. DRY, like Terraform modules.

**Release** — an instance of a chart deployed to the cluster. Install same chart 3x = 3 releases.
Helm tracks each release's revision history.

**Override values per environment:**
```bash
helm install myapp ./mychart -f values-prod.yaml    # prod values file
helm install myapp ./mychart --set replicaCount=5   # override single value
```

## Commands
```bash
helm install myapp ./mychart      # deploy → creates a release
helm upgrade myapp ./mychart      # update existing release
helm rollback myapp 1             # roll back to revision 1 (tracks history!)
helm uninstall myapp              # remove release
helm list                         # list releases
helm template ./mychart           # render templates locally (debug)
```
`helm rollback` works because Helm keeps a revision history of releases → instant rollback of a bad deploy.

## Interview one-liner
"Helm is K8s' package manager. Instead of dozens of raw YAMLs, you package them into a chart with
templated manifests pulling from values.yaml — so the same chart deploys across environments with
different values (dev 1 replica, prod 5). Each deploy is a release, and Helm tracks history so you
can roll back easily. Like Terraform modules but for K8s manifests."

## Honest experience framing
"I've used Helm to deploy apps and tools — e.g. installed kube-prometheus-stack and ArgoCD via
charts. I understand chart structure — templates, values, releases — and how it parameterizes
deployments across environments. Comfortable using/customizing charts; authoring charts is
something I've done at a basic level and can grow into."
