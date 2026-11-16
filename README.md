# 2DV705 Assignment 2: Cloud Infrastructure on AWS

**Course:** 2DV705 - Virtualization, Cloud, and Storage  
**Institution:** Linnaeus University  
**Student:** Santiago (`sp223pv@student.lnu.se`)  
**AWS Region:** `eu-north-1` (Stockholm)

---

## 📌 Project Overview

This repository contains the complete Infrastructure as Code (IaC) implementation for **Assignment 2: Cloud Infrastructure on AWS**.

The infrastructure deploys a scalable, secure 3-tier web architecture for the `lnu-notes` application using **Terraform**, **AWS EC2**, **VPC**, **S3**, and **Systems Manager (SSM) Parameter Store**.

```
[ Internet ]
     │ HTTP:80
     ▼
[ Internet Gateway (IGW) ]
     │
┌────▼──────────────────────────────────────────────────────────────────┐
│ AWS VPC (10.0.0.0/16) - eu-north-1                                    │
│                                                                       │
│  ┌─────────────────────────────┐    ┌──────────────────────────────┐  │
│  │ Public Subnet (10.0.1.0/24) │    │ Private Subnet (10.0.2.0/24) │  │
│  │                             │    │                              │  │
│  │  [NAT Gateway] ─────────────┼────┼────────┐ (Outbound Updates)  │  │
│  │                             │    │        ▼                     │  │
│  │  [Web Server EC2] ──────────┼────┼──► [MariaDB EC2]             │  │
│  │  • Gunicorn / Nginx         │    │    • Port 3306 (Private)     │  │
│  │  • IAM Role (S3 & SSM)      │    │    • No Public IP / IGW     │  │
│  └──────────────┬──────────────┘    └──────────────────────────────┘  │
└─────────────────┼─────────────────────────────────────────────────────┘
                  │ IAM Role / SigV4
                  ▼
         [ Amazon S3 Bucket ]
         (Notes & Attachments)
```

---

## 🚀 Key Implementations & Tasks (1–16)

1. **Custom VPC & Subnets:**
   - Isolated CIDR `10.0.0.0/16`.
   - Public subnet (`10.0.1.0/24`) with Internet Gateway (IGW) for user-facing traffic.
   - Private subnet (`10.0.2.0/24`) with isolated route table routing `0.0.0.0/0` through a NAT Gateway for outbound patch management.
2. **Security & Least Privilege:**
   - **Database Isolation (Task 10):** Security group restricts port 3306 ingress strictly to the Web EC2 security group. Verified with external connection timeout (`nc -zvw 3 <db_ip> 3306`).
   - **S3 Bucket Policy (Task 12):** Explicit resource policy denies direct object access from outside the Web EC2 IAM instance profile (HTTP 403 AccessDenied for administrator credentials).
3. **Zero Plaintext Credentials in Terraform State (Task 16):**
   - Implemented via AWS Systems Manager (SSM) Parameter Store (`SecureString` parameter `/2dv705/db_password`).
   - Eliminated `random_password` from Terraform state, reducing plaintext password occurrences to `0` in `terraform.tfstate`.
   - EC2 instances retrieve the database password at boot time via AWS CLI and IMDSv2 IAM role credentials.
4. **Drift Detection & Automatic Reconciliation (Task 13):**
   - Caught and reconciled drift via `terraform plan` and `terraform apply`.
5. **Reproducible Rebuild (Task 14):**
   - Clean teardown (`terraform destroy`) and redeployment (`terraform apply`) verified from code alone.

---

## 📁 Repository Structure

```
.
├── README.md                       # Project documentation & reproduction guide
├── .gitignore                      # Security & artifact exclusions
└── lnu-notes/                      # Application code and Terraform infrastructure
    ├── app.py                      # Flask 3-tier application
    ├── schema.sql                  # Database schema
    ├── requirements.txt            # Python dependencies
    ├── deploy/                     # Cloud-init scripts and systemd configs
    │   ├── cloud-config-db.yaml
    │   ├── cloud-config-web.yaml
    │   ├── db-userdata.sh
    │   ├── iam-policy-s3.json
    │   ├── iam-policy-ssm.json
    │   ├── lnu-notes.service
    │   └── web-userdata.sh
    └── terraform/                  # Terraform IaC definitions
        ├── main.tf                 # VPC, Subnets, EC2, S3, Security Groups
        ├── task16-ssm.tf           # SSM Parameter Store integration
        ├── variables.tf            # Configurable input variables
        ├── outputs.tf              # Web IP, DB IP, S3 Bucket outputs
        ├── cloud-config-web.yaml.tftpl
        └── cloud-config-db.yaml.tftpl
```

---

## 🛠️ How to Deploy

### Prerequisites
- [Terraform](https://www.terraform.io/) `>= 1.5.0`
- [AWS CLI](https://aws.amazon.com/cli/) configured with valid administrator credentials
- An EC2 Key Pair created in `eu-north-1` (default: `2dv705`)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AngelsJ1/AWS.git
   cd AWS/lnu-notes/terraform
   ```

2. **Configure Variables:**
   Copy the example variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
   Edit `terraform.tfvars` with your settings:
   ```hcl
   region        = "eu-north-1"
   key_name      = "2dv705"
   my_ip         = "YOUR_PUBLIC_IP/32"
   bucket_prefix = "2dv705"
   ```

3. **Deploy Infrastructure:**
   ```bash
   terraform init
   terraform apply -auto-approve
   ```

4. **Verify Application:**
   Once cloud-init finishes (~2–3 minutes):
   ```bash
   WEB_IP=$(terraform output -raw web_public_ip)
   curl -s http://${WEB_IP}/healthz | jq .
   ```
   Expected output:
   ```json
   {
     "app": "ok",
     "database": "ok",
     "s3": "ok"
   }
   ```

5. **Teardown:**
   ```bash
   terraform destroy -auto-approve
   ```

---

## 🔒 Security Notice

Sensitive files (`terraform.tfvars`, `*.tfstate`, `*.pem`, `.env`) are strictly ignored via `.gitignore` and are never committed to version control.
