# Gap Topic: Ansible (Configuration Management)

## What it is
Agentless configuration management + automation tool. Declares the desired STATE of servers
(packages installed, configs in place, services running) and makes them match — on 1 or 1000
servers, consistently.

## Ansible vs Terraform (THE key question)
- **Terraform** = IaC / **provisioning** — CREATES infra (EC2, VPC, LB). "Give me 5 servers."
- **Ansible** = **configuration management** — CONFIGURES existing servers. "Install Docker +
  nginx on those 5, copy configs, start services."
- **Complementary:** Terraform provisions → Ansible configures. (TF creates EC2 → Ansible installs software.)

## Two big properties (interviewers love these)
1. **Agentless** — NO agent needed on target machines (unlike Chef/Puppet). Connects over
   **SSH** (needs SSH + Python on target). List targets' IPs in the inventory.
2. **Idempotent** — run a playbook repeatedly → same result; only changes what's out of desired
   state. (nginx already installed → "install nginx" task does nothing.) Safe to re-run.

## Four core concepts
1. **Inventory** — file listing the servers Ansible manages, grouped ([webservers], [databases]).
2. **Playbook** — YAML file of tasks describing desired state (install nginx, start service).
   Declarative + ordered.
3. **Modules** — pre-built units of work (apt/yum=packages, service=services, copy/template=files,
   user=accounts). Hundreds available.
4. **Roles** — reusable, shareable bundles of playbooks (like Terraform modules).

## Flow
Write playbook + inventory → `ansible-playbook -i inventory playbook.yml` → Ansible SSHes to
each target, runs tasks (via Python on target), reports changed vs ok. Push-based, agentless.

## Example playbook
```yaml
- name: Configure web servers
  hosts: webservers
  become: yes
  tasks:
    - name: Install nginx
      apt: { name: nginx, state: present }
    - name: Start nginx
      service: { name: nginx, state: started, enabled: yes }
```

## Honest interview framing (haven't used in prod)
"Haven't used it extensively in production, but I understand it well: agentless config
management over SSH — nothing to install on targets. Define servers in an inventory, write
YAML playbooks describing desired state using modules, idempotent so safe to re-run. Terraform
provisions the infra, Ansible configures it — complementary."
