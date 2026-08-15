# Gap Topics: Terraform Multi-Region + S3/VPC + init

## Terraform multi-region = PROVIDER ALIASES
A provider block is single-region. To span regions in one config:
```hcl
provider "aws" {                 # default (no alias)
  region = "us-east-1"
}
provider "aws" {
  alias  = "europe"              # aliased
  region = "eu-west-1"
}
resource "aws_instance" "eu" {
  provider      = aws.europe     # <-- pick the region via provider arg
  ami           = "..."
  instance_type = "t3.micro"
}
```
- No `provider` arg on a resource → uses the **default** (unaliased) provider's region.
- AMIs are region-specific → look up per region with a `data "aws_ami"` source.
- Scale the same infra across regions via modules + passed providers.

## `terraform init` (4 things)
1. Download provider plugins → `.terraform/`
2. Initialize backend / state storage (migrate local→remote if configured, prompts)
3. Download modules
4. Create/update `.terraform.lock.hcl` (pin provider versions)

## Does S3 need a VPC?
No — S3 is a regional managed service OUTSIDE the VPC, accessed via API, controlled by
IAM/bucket policies. Hosted in one region, globally accessible with permissions.
**VPC Gateway Endpoint for S3** = optional; lets VPC resources reach S3 privately over AWS's
internal network (no internet/NAT) — more secure + saves cost.

## All-private app, user access
ALB in PUBLIC subnets (internet-facing) → routes to private frontend → BE → DB (all internal).
Only the LB is exposed. Route53 → ALB. Inbound = ALB; Outbound (private→internet) = NAT gateway.
