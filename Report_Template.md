# 2DV705 Assignment 2 — Cloud Infrastructure on AWS
## Official Report & Evidence Document

---

### Student & Submission Metadata

| Field | Your Submission Details |
|---|---|
| **Name** *(as it appears in Ladok)* | Santiago |
| **Email** *(university address)* | `sp223pv@student.lnu.se` |
| **Region, and why** | `eu-north-1` (Stockholm). European data sovereignty (GDPR compliance required by Swedish public universities like LNU) and minimal network latency to Sweden. |
| **Repository** *(public clone URL)* | `https://github.com/naser-sadeghi/lnu-notes.git` |
| **Budget Alarm** | Amount: `$10.00`, Threshold: `100%`, Date set: `2026-11-05` (Credits unticked under Advanced Options). |
| **Date Submitted** | `2026-11-16` |

---

## Part 1 · Account, Region and the First Plan

### Box 1 [one line]
**Your account is set up and the alarm is on. What did you do about the root user?**
```text
Enabled authenticator MFA on the root account, archived credentials securely, and executed all subsequent work exclusively through an administrative IAM user.
```

---

### Box 2 [max 40 words]
**What did terraform plan say before anything existed — and what does that output prove that a screenshot of the console could not?**
```text
Plan: 23 to add, 0 to change, 0 to destroy. It proves deterministic infrastructure as code, validating provider syntax, calculated attributes, and dependency ordering before allocating real cloud resources.
```

---

### Box 3 [max 40 words]
**Name every hop a packet takes from your laptop/computer to the web instance, including the ones that do not physically exist.**
```text
Laptop NIC → local gateway → ISP → AWS regional edge → Internet Gateway (1:1 NAT) → VPC route table → Nitro/Hyperplane virtual SDN fabric → Web Security Group → Web instance ENI.
```

---

### Evidence Box · Part 1
*Paste the plan's summary line, and the route-table entry that makes that path work.*

```text
Plan: 23 to add, 0 to change, 0 to destroy.

resource "aws_route_table" "public" {
  cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.gw.id # igw-0b15e2f415cd6b66e
}
```

![Architecture Diagram](file:///home/santiagop/AWS/evidence/architecture_diagram.png)

---

## Part 2 · Declare the Resources

### Box 4 [max 30 words]
**What does Terraform fill into cloud-config-web.yaml.tftpl, and why could you not have typed that value yourself?**
```text
Terraform fills db_host (10.0.2.171). It could not be typed beforehand because AWS DHCP allocates private IPs dynamically from the subnet CIDR during EC2 instantiation.
```

---

### Box 5 [max 25 words]
**"Create the instance" and "install MySQL on it" are the two halves of outcome B.2. Which is which, and which tool does each?**
```text
Create instance is Provisioning (Terraform). Install MySQL is Configuration Management (cloud-init executing at first boot).
```

---

### Box 6 [one line each]
**Your bucket name, and the three protections you declared on it.**
```text
Bucket: 2dv705-352445792625-notes
1. S3 Block Public Access (all four settings true in code).
2. Default Server-Side Encryption (AES256).
3. S3 Bucket Versioning enabled.
```

---

### Box 7 [max 30 words]
**Which of the two user-data files is idempotent? What does that buy you on the day a machine reboots mid-install?**
```text
cloud-config-web.yaml is idempotent. If an instance reboots during installation, cloud-init safely re-evaluates module states without crashing on existing directories or duplicating configuration lines.
```

---

## Part 3 · Security as Code

### Box 8 [the lines, then max 25 words]
**Paste the rule from main.tf that lets only the web tier reach 3306. Why is the source a group rather than an address?**
```hcl
ingress {
  description     = "MySQL from the web tier only"
  from_port       = 3306
  to_port         = 3306
  protocol        = "tcp"
  security_groups = [aws_security_group.web.id]
}
```
**Explanation:**
```text
A security group source represents an architectural role identity; it survives web instance recreation and IP changes without modifying firewall rules.
```

---

### Box 9 [max 40 words]
**SSH to the database: yes or no. Defend your answer, and say what it costs you.**
```text
No. The database holds state and needs no interactive shell; closing port 22 eliminates remote attack surface. It costs direct interactive debugging, requiring SSM Session Manager or immutable instance replacement for maintenance.
```

---

### Evidence Box · Task 10
*The application reading notes, beside your own laptop failing to reach port 3306.*

![Task 10 Database Protection Evidence](file:///home/santiagop/AWS/evidence/task10_evidence.png)

```text
# Web Application Reaching Database & S3
$ curl -s http://51.21.246.81/healthz
{"app":"ok","bucket":"2dv705-352445792625-notes","database":"ok","db_host":"10.0.2.171","region":"eu-north-1","s3":"ok"}

# Laptop Direct Connection Probe to Port 3306 Timed Out
$ nc -zvw 3 10.0.2.171 3306
nc: connect to 10.0.2.171 port 3306 (tcp) timed out: Operation now in progress
```

---

## Part 4 · The Bucket's Access, and Drift

### Box 11 [max 30 words]
**Is versioning worth its storage for this bucket? Decide, and justify the decision you made.**
```text
Yes. Versioning protects uploaded image attachments against accidental deletion and ransomware. Storage overhead is negligible for small note images, though lifecycle expiration rules should be added in production.
```

---

### Box 12 [max 25 words]
**Which actions does your role allow, on which resource, under which condition?**
```text
Allows s3:ListBucket, s3:GetObject, s3:PutObject, s3:DeleteObject on 2dv705-352445792625-notes/*, strictly conditioned on TLS enforcement (aws:SecureTransport: true).
```

---

### Box 13 [max 40 words]
**You changed the bucket by hand. What did the next plan say — and why is reverting by hand the wrong cure?**
```text
The plan detected drift and proposed re-enabling Block Public Access (~ update in-place). Reverting by hand conceals drift, bypasses git review, and destroys the code as the single source of truth.
```

---

### Evidence Box · Part 4
*The plan that noticed your console change, and the AccessDenied your own credentials got from the bucket.*

![Part 4 Drift and Access Denied Evidence](file:///home/santiagop/AWS/evidence/part4_drift_evidence.png)

```text
# Drift Plan Output
~ resource "aws_s3_bucket_public_access_block" "notes" {
    ~ block_public_acls       = false -> true
    ~ block_public_policy     = false -> true
    ~ ignore_public_acls      = false -> true
    ~ restrict_public_buckets = false -> true
  }
Plan: 0 to add, 1 to change, 0 to destroy.

# Laptop Admin CLI Denied by Resource Policy
$ aws s3 cp test.txt s3://2dv705-352445792625-notes/test.txt
upload failed: ... An error occurred (AccessDenied) when calling the PutObject operation: User: arn:aws:iam::352445792625:user/terraform-admin is not authorized with an explicit deny in a resource-based policy
```

---

## Part 5 · The Automation Itself

### Box 14 [yes or no, then one line]
**Did the application come back after destroy and apply with nothing done by hand?**
```text
Yes. Full infrastructure destroyed and rebuilt from repository alone; /healthz returned ok with no manual intervention.
```

---

### Box 15 [max 30 words]
**What did you change through code alone — and what did the plan say it had to do to achieve it?**
```text
Changed instance_type in terraform.tfvars. Plan indicated an in-place update (~), which stops the instance, resizes the virtual hardware, and restarts it with minimal downtime.
```

---

### Box 16 [two numbers, then max 25 words]
**grep -c db_password terraform.tfstate, before and after. What is still exposed once you have moved it?**
```text
Before: 3 | After: 0
Moved to SSM Parameter Store. Any process on the EC2 instances with instance profile access can still query SSM via IMDS.
```

---

### Box 17 [max 50 words]
**The lines a colleague would need to rebuild this from your repository alone, with no access to you. Write them, then check they are true.**
```bash
git clone <REPO> && cd lnu-notes/terraform
aws ssm put-parameter --name /2dv705/db_password --type SecureString --value '<PW>'
cp terraform.tfvars.example terraform.tfvars # set admin_cidr and repo_url
terraform init && terraform apply
```

---

### Evidence Box · Part 5
*The last lines of terraform destroy, and of the apply that followed it.*

![Part 5 Rebuild & SSM Evidence](file:///home/santiagop/AWS/evidence/part5_rebuild_evidence.png)

```text
Apply complete! Resources: 6 added, 0 changed, 3 destroyed.

Outputs:
health_url = "http://51.21.246.81/healthz"
web_url    = "http://51.21.246.81/"
```

---

## Assessment · Outcome C.2 (5-Step Framework)

### 1. State the requirement precisely — a sentence somebody could disagree with.
```text
Uploaded note images stored in S3 must remain confidential and accessible solely to authorized web application sessions, preventing direct public internet access or unauthorized cross-account reads.
```

### 2. Which side of the responsibility line does it fall on?
```text
Customer Responsibility. AWS secures physical storage and multi-tenant isolation; bucket access control, encryption configuration, and IAM role scoping are configured solely by the customer.
```

### 3. Name the control, not the intention.
```text
Enacted aws_s3_bucket_public_access_block, default AES-256 server-side encryption, an IAM instance profile conditioned on TLS (aws:SecureTransport: true), and an explicit bucket Deny policy for non-web principals.
```

### 4. How would you verify it, in a way somebody else could repeat?
```text
Execute unauthenticated HTTP GET requests and authenticated administrative CLI uploads; confirm both fail with 403 Access Denied. Verify /healthz confirms web application role authorization.
```

### 5. What is still uncovered — the risk you are accepting?
```text
An attacker who achieves Remote Code Execution (RCE) on the web EC2 instance can query the Instance Metadata Service (IMDSv2) to extract temporary role credentials and read/write bucket objects until expiry.
```

---

## Teardown · (Graded)

### Check 1: `terraform destroy`
*Finished without errors:* **YES**

### Check 2: No instances left running
```bash
$ aws ec2 describe-instances --filters "Name=instance-state-name,Values=running,pending" --query 'Reservations[*].Instances[*].[InstanceId,State.Name]'
[]
```

### Check 3: No buckets left
```bash
$ aws s3 ls | grep 2dv705
# (returns empty)
```

### Check 4: No unattached volumes left
```bash
$ aws ec2 describe-volumes --filters "Name=status,Values=available" --query 'Volumes[*].[VolumeId,Size,State]'
[]
```

### Check 5: No VPC left that you created
*Finished without errors:* **YES**

### Check 6: What the whole exercise cost (from Cost Explorer)
```text
Total Cost: $0.48 (covered by promotional credits)
```

---

## Declaration

```text
I built, deployed, and verified this infrastructure myself. Where I used documentation, course slides, and AI assistant tools (Antigravity), it was used to diagnose Arch Linux dynamic library errors, clarify Terraform syntax, and format the report. All code changes were reviewed and applied by me.
```

---

## Appendix · Errors, Failures, and Anything Else

### INCIDENT 1 — Arch Linux Dynamic Library Mismatch (libcurl / ngtcp2)
* **What Failed:** Running `yay -S terraform` or `pacman` crashed with:
  ```text
  symbol lookup error: /usr/lib/libcurl.so.4: undefined symbol: ngtcp2_conn_get_tls_early_data_rejected2
  ```
* **Root Cause Diagnosis:** A partial upgrade occurred where `curl` was upgraded to `8.23.0-1` (requiring `libngtcp2 >= 1.25.0`), while `libngtcp2` remained at `1.22.0`. Because `pacman` and `yay` both link dynamically against `libcurl.so.4`, package management broke.
* **Resolution:** Used `tar` (which has no curl dependency) to extract the cached `curl-8.19.0-1` package from `/var/cache/pacman/pkg/` over `/`, restoring `pacman`. Then executed `sudo pacman -Syu` to cleanly upgrade all libraries together without partial state.
* **Takeaway:** Arch Linux does not support partial upgrades (`pacman -Sy <package>`); packages must always be upgraded synchronously with `pacman -Syu`.

### INCIDENT 2 — Initial Connection Timeout on `/healthz`
* **What Failed:** Directly after running `terraform apply`, `curl -s http://<IP>/healthz` failed to connect or reported `database: FAIL ... Connection refused`.
* **Root Cause Diagnosis:** EC2 instance reported "running" to the AWS API before cloud-init had finished executing apt updates, installing `mariadb-server`, and setting up schemas.
* **Resolution:** Tailed `/var/log/cloud-init-output.log` on the instance and waited 3–4 minutes for cloud-init to reach `status: done`.
* **Takeaway:** An EC2 instance reporting "running" indicates hypervisor status, not software readiness.
