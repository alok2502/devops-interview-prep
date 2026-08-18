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

# Gap Topic: Ansible — How it Authenticates & Runs (SSH details)

## Authentication (how Ansible gets into targets)
Standard SSH — same as a human SSHing in:
1. **SSH key-based** (standard for automation) — public key in target's `~/.ssh/authorized_keys`,
   control node uses matching private key. No password prompts.
2. **User/password** — possible (`ansible_user`/`ansible_password`, or `--ask-pass`), but keys preferred.
```ini
[webservers]
10.0.1.5 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa
```

## Privilege escalation (running as root)
`become: yes` → runs task via **sudo** on the target. Ansible SSHes in as a normal user, escalates
to root for tasks that need it.

## How tasks actually run (why it's "agentless")
1. SSH into target.
2. Copy the relevant **Python module code** to a temp dir on the target.
3. Target's **Python interpreter** executes it (does the real work).
4. Returns result (changed/ok/failed), cleans up temp files.
Only requirement on target: **SSH + Python**. No permanent agent → "agentless."

## Getting SSH keys onto N machines (the bootstrap problem)
- `ssh-copy-id user@host` — few machines, manual (appends key to authorized_keys).
- **SCALE / cloud:** inject key at PROVISIONING time:
  - AWS EC2 **key pair** at launch (AWS auto-adds to authorized_keys)
  - Golden **AMI** with keys baked in
  - **cloud-init / user-data** startup script
- **Clean pattern:** Terraform provisions instances WITH the key → Ansible configures
  (provisioning + config hand off).
- Existing machines w/o keys: initial password-based Ansible run to distribute keys, then key-based.
- Enterprise: AWS SSM Session Manager (no keys, IAM-based).

## One-liner
"Ansible authenticates over SSH (key-based for automation), escalates via sudo with `become`,
copies its module code to the target, runs it with the target's Python, returns result, cleans up
— that's why it's agentless. At scale, the SSH key is injected at provisioning time (EC2 key pair,
AMI, or cloud-init) rather than copied to running machines."
