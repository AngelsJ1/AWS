import os
import docx
from docx.shared import Inches, Pt, RGBColor

template_path = "/home/santiagop/AWS/Assignment Report Template.docx"
output_docx = "/home/santiagop/AWS/2DV705_A2_Santiago.docx"

doc = docx.Document(template_path)

def set_cell_text(cell, text, bold_prefix=None, italic=False, color_rgb=(20, 20, 20), font_size=9.5):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.bold = True
        run_b.font.size = Pt(font_size)
        run_b.font.color.rgb = RGBColor(*color_rgb)
    run = p.add_run(text)
    run.italic = italic
    run.font.size = Pt(font_size)
    run.font.color.rgb = RGBColor(*color_rgb)

def add_image_to_cell(cell, image_path, width_inches=5.8):
    if os.path.exists(image_path):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run()
        run.add_picture(image_path, width=Inches(width_inches))

# Table 0: Metadata
doc.tables[0].rows[0].cells[1].text = "Santiago"
doc.tables[0].rows[1].cells[1].text = "sp223pv@student.lnu.se"
doc.tables[0].rows[2].cells[1].text = "eu-north-1 (Stockholm) — EU data sovereignty (GDPR) and lowest network latency to Sweden."
doc.tables[0].rows[3].cells[1].text = "https://github.com/naser-sadeghi/lnu-notes.git"
doc.tables[0].rows[4].cells[1].text = "$10.00 zero-spend alarm, threshold 100%, set 2026-11-05 (credits unticked under advanced scope)."
doc.tables[0].rows[5].cells[1].text = "2026-11-16"

# Table 2: Part 1 Tasks
set_cell_text(doc.tables[2].rows[0].cells[2], "Enabled hardware authenticator MFA on the root account, archived credentials securely, and executed all subsequent work exclusively via the IAM administrator user.")
set_cell_text(doc.tables[2].rows[1].cells[2], "Plan: 23 to add, 0 to change, 0 to destroy. It proves deterministic infrastructure as code, validating provider syntax, calculated attributes, and dependency ordering before allocating real cloud resources.")
set_cell_text(doc.tables[2].rows[2].cells[2], "Laptop NIC → local gateway → ISP → AWS regional edge → Internet Gateway (1:1 NAT) → VPC route table → Nitro/Hyperplane virtual SDN fabric → Web Security Group → Web instance ENI.")

# Table 3: Evidence Part 1 (Plan summary line + Route Table entry)
set_cell_text(doc.tables[3].rows[0].cells[0], "Plan: 23 to add, 0 to change, 0 to destroy.\nRoute: 0.0.0.0/0 via Internet Gateway (igw-0b15e2f415cd6b66e) attached to VPC vpc-088ae055b348cf829.")
add_image_to_cell(doc.tables[3].rows[0].cells[0], "/home/santiagop/AWS/evidence/architecture_diagram.png", width_inches=5.8)

# Table 5: Part 2 Tasks
set_cell_text(doc.tables[5].rows[0].cells[2], "Terraform fills db_host (10.0.2.171). It could not be typed beforehand because AWS DHCP allocates private IPs dynamically from the subnet CIDR during EC2 instantiation.")
set_cell_text(doc.tables[5].rows[1].cells[2], "Create instance is Provisioning (Terraform). Install MySQL is Configuration Management (cloud-init executing at first boot).")
set_cell_text(doc.tables[5].rows[2].cells[2], "Bucket: 2dv705-352445792625-notes\n1. S3 Block Public Access (all four settings true in code).\n2. Default Server-Side Encryption (AES256).\n3. S3 Bucket Versioning enabled.")
set_cell_text(doc.tables[5].rows[3].cells[2], "cloud-config-web.yaml is idempotent. If an instance reboots during installation, cloud-init safely re-evaluates module states without crashing on existing directories or duplicating configuration lines.")

# Table 7: Part 3 Tasks
set_cell_text(doc.tables[7].rows[0].cells[2], "ingress {\n  from_port = 3306\n  to_port = 3306\n  protocol = \"tcp\"\n  security_groups = [aws_security_group.web.id]\n}\nA security group source represents an architectural role identity; it survives web instance recreation and IP changes without modifying firewall rules.")
set_cell_text(doc.tables[7].rows[1].cells[2], "No SSH to DB. The database stores state and requires no interactive shell; closing port 22 eliminates the remote network attack surface. It costs direct interactive DBA debugging, requiring SSM Session Manager instead.")

# Table 8: Evidence Part 3 / Task 10
set_cell_text(doc.tables[8].rows[0].cells[0], "Task 10 Evidence: Application reads/writes notes and images successfully (/healthz OK), while laptop direct TCP connection to private port 3306 times out.")
add_image_to_cell(doc.tables[8].rows[0].cells[0], "/home/santiagop/AWS/evidence/task10_evidence.png", width_inches=5.8)

# Table 10: Part 4 Tasks
set_cell_text(doc.tables[10].rows[0].cells[2], "Yes. Versioning protects uploaded image attachments against accidental deletion and ransomware. Storage overhead is negligible for small note images, though lifecycle expiration rules should be added in production.")
set_cell_text(doc.tables[10].rows[1].cells[2], "Allows s3:ListBucket, s3:GetObject, s3:PutObject, s3:DeleteObject on 2dv705-352445792625-notes/*, strictly conditioned on TLS enforcement (aws:SecureTransport: true).")
set_cell_text(doc.tables[10].rows[2].cells[2], "The plan detected drift and proposed re-enabling Block Public Access (~ update in-place). Reverting by hand conceals drift, bypasses git review, and destroys the code as the single source of truth.")

# Table 11: Evidence Part 4
set_cell_text(doc.tables[11].rows[0].cells[0], "Part 4 Evidence: Terraform plan detecting manual Block Public Access drift, and administrator laptop CLI denied PutObject due to explicit resource-based policy deny.")
add_image_to_cell(doc.tables[11].rows[0].cells[0], "/home/santiagop/AWS/evidence/part4_drift_evidence.png", width_inches=5.8)

# Table 13: Part 5 Tasks (14, 15, 16)
set_cell_text(doc.tables[13].rows[0].cells[2], "Yes. Full infrastructure destroyed and rebuilt from repository alone; /healthz returned ok with no manual intervention.")
set_cell_text(doc.tables[13].rows[1].cells[2], "Changed instance_type in terraform.tfvars. Plan indicated an in-place update (~), which stops the instance, resizes the virtual hardware, and restarts it with minimal downtime.")
set_cell_text(doc.tables[13].rows[2].cells[2], "Before: 3 | After: 0\nMoved to SSM Parameter Store. Any process on the EC2 instances with instance profile access can still query SSM via IMDS.")

# Table 15: Task 17
set_cell_text(doc.tables[15].rows[0].cells[2], "git clone <REPO> && cd lnu-notes/terraform\naws ssm put-parameter --name /2dv705/db_password --type SecureString --value '<PW>'\ncp terraform.tfvars.example terraform.tfvars # set admin_cidr and repo_url\nterraform init && terraform apply")

# Table 16: Evidence Part 5
set_cell_text(doc.tables[16].rows[0].cells[0], "Part 5 Evidence: Database password purged from terraform.tfstate (grep count 0), and clean rebuild completed via Terraform.")
add_image_to_cell(doc.tables[16].rows[0].cells[0], "/home/santiagop/AWS/evidence/part5_rebuild_evidence.png", width_inches=5.8)

# Table 18: Assessment Outcome C.2 (5 steps)
set_cell_text(doc.tables[18].rows[0].cells[2], "Uploaded note images stored in S3 must remain confidential and accessible solely to authorized web application sessions, preventing direct public internet access or unauthorized cross-account reads.")
set_cell_text(doc.tables[18].rows[1].cells[2], "Customer Responsibility. AWS secures physical storage and multi-tenant isolation; bucket access control, encryption configuration, and IAM role scoping are configured solely by the customer.")
set_cell_text(doc.tables[18].rows[2].cells[2], "Enacted aws_s3_bucket_public_access_block, default AES-256 server-side encryption, an IAM instance profile conditioned on TLS (aws:SecureTransport: true), and an explicit bucket Deny policy for non-web principals.")
set_cell_text(doc.tables[18].rows[3].cells[2], "Execute unauthenticated HTTP GET requests and authenticated administrative CLI uploads; confirm both fail with 403 Access Denied. Verify /healthz confirms web application role authorization.")
set_cell_text(doc.tables[18].rows[4].cells[2], "An attacker who achieves Remote Code Execution (RCE) on the web EC2 instance can query the Instance Metadata Service (IMDSv2) to extract temporary role credentials and read/write bucket objects until expiry.")

# Table 20: Teardown
set_cell_text(doc.tables[20].rows[0].cells[2], "Yes (all 23 resources destroyed cleanly)")
set_cell_text(doc.tables[20].rows[1].cells[2], "[] (0 running/pending instances)")
set_cell_text(doc.tables[20].rows[2].cells[2], "(empty list, 2dv705 bucket deleted)")
set_cell_text(doc.tables[20].rows[3].cells[2], "[] (0 unattached volumes)")
set_cell_text(doc.tables[20].rows[4].cells[2], "Yes (0 non-default VPCs remaining)")
set_cell_text(doc.tables[20].rows[5].cells[2], "$0.48 (fully covered by initial $100 AWS credits)")

# Table 22: Declaration
set_cell_text(doc.tables[22].rows[0].cells[2], "I built, deployed, and verified this infrastructure myself. Where I used documentation, course slides, and AI assistant tools (Antigravity), it was used to diagnose Arch Linux dynamic library errors, clarify Terraform syntax, and format the report. All code changes were reviewed and applied by me.")

# Table 24: Appendix
appendix_text = (
    "INCIDENT 1 — Arch Linux Dynamic Library Mismatch (libcurl / ngtcp2)\n"
    "• Error: yay and pacman failed with 'symbol lookup error: /usr/lib/libcurl.so.4: undefined symbol: ngtcp2_conn_get_tls_early_data_rejected2'\n"
    "• Diagnosis: A partial upgrade occurred where curl was upgraded to 8.23.0-1 (requiring libngtcp2 >= 1.25.0) while libngtcp2 was at 1.22.0. Because pacman links against libcurl.so.4, package management was broken.\n"
    "• Resolution: Used tar (which has no curl dependency) to extract the cached curl-8.19.0-1 package from /var/cache/pacman/pkg/ directly over /, reviving pacman. Then executed sudo pacman -Syu to synchronize all packages together.\n"
    "• Takeaway: Arch Linux requires synchronous system upgrades; partial upgrades break dynamic linker dependencies.\n\n"
    "INCIDENT 2 — Initial Connection Refused on /healthz\n"
    "• Error: curl http://<ip>/healthz returned connection refused directly after terraform apply.\n"
    "• Diagnosis: EC2 reported 'running' at the hypervisor level before cloud-init completed installing Python venv and MariaDB.\n"
    "• Resolution: Tailed /var/log/cloud-init-output.log via SSH; services started and health check returned OK within 3 minutes."
)
set_cell_text(doc.tables[24].rows[0].cells[0], appendix_text, font_size=8.5)

doc.save(output_docx)
print(f"Generated {output_docx}")
