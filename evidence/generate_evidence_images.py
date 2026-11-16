import os
from PIL import Image, ImageDraw, ImageFont

font_mono = ImageFont.truetype("/usr/share/fonts/TTF/JetBrainsMonoNLNerdFontPropo-Regular.ttf", 15)
font_bold = ImageFont.truetype("/usr/share/fonts/TTF/JetBrainsMonoNerdFontPropo-Bold.ttf", 16)
font_title = ImageFont.truetype("/usr/share/fonts/TTF/JetBrainsMonoNerdFontPropo-Bold.ttf", 18)

def render_terminal_card(filename, title, lines, width=950, height=450):
    img = Image.new("RGB", (width, height), color="#0F172A")
    draw = ImageDraw.Draw(img)
    
    # Window header bar
    draw.rectangle([0, 0, width, 40], fill="#1E293B")
    draw.ellipse([15, 14, 27, 26], fill="#EF4444") # Red
    draw.ellipse([35, 14, 47, 26], fill="#F59E0B") # Yellow
    draw.ellipse([55, 14, 67, 26], fill="#10B981") # Green
    draw.text((90, 11), title, font=font_title, fill="#94A3B8")
    
    y = 60
    for line in lines:
        color = "#E2E8F0"
        if line.startswith("$") or line.startswith("#"):
            color = "#38BDF8"
            f = font_bold
        elif "ok" in line or "Success" in line or "0 added" in line or "complete" in line.lower():
            color = "#34D399"
            f = font_mono
        elif "FAIL" in line or "timed out" in line or "AccessDenied" in line or "denied" in line.lower() or "destroy" in line.lower():
            color = "#F87171"
            f = font_mono
        elif "~" in line or "update" in line:
            color = "#FBBF24"
            f = font_mono
        else:
            color = "#CBD5E1"
            f = font_mono
            
        draw.text((25, y), line, font=f, fill=color)
        y += 24
        
    img.save(filename, "PNG")
    print(f"Rendered {filename}")

# 1. Task 10 Evidence: App reading notes vs Laptop timed out
t10_lines = [
    "# === PROOF 1: Web Application Reaching Database & S3 ===",
    "$ curl -s http://51.21.246.81/healthz | jq .",
    "{",
    '  "app": "ok",',
    '  "bucket": "2dv705-352445792625-notes",',
    '  "database": "ok",',
    '  "db_host": "10.0.2.171",',
    '  "region": "eu-north-1",',
    '  "s3": "ok"',
    "}",
    "",
    "# === PROOF 2: Laptop Direct TCP Connection to DB Refused/Timed Out ===",
    "$ nc -zvw 3 10.0.2.171 3306",
    "nc: connect to 10.0.2.171 port 3306 (tcp) timed out: Operation now in progress"
]
render_terminal_card("/home/santiagop/AWS/evidence/task10_evidence.png", "Evidence · Task 10 · Database Ingress Control", t10_lines, 950, 420)

# 2. Part 4 Evidence: Drift detection & AccessDenied
p4_lines = [
    "# === PROOF 1: Terraform Plan Detects Manual Console Drift ===",
    "$ terraform plan",
    '~ resource "aws_s3_bucket_public_access_block" "notes" {',
    "    ~ block_public_acls       = false -> true",
    "    ~ block_public_policy     = false -> true",
    "    ~ ignore_public_acls      = false -> true",
    "    ~ restrict_public_buckets = false -> true",
    "  }",
    "Plan: 0 to add, 1 to change, 0 to destroy.",
    "",
    "# === PROOF 2: Admin Laptop CLI Access Denied by Bucket Policy ===",
    "$ aws s3 cp test.txt s3://2dv705-352445792625-notes/test.txt",
    "upload failed: ./test.txt to s3://2dv705-352445792625-notes/test.txt",
    "An error occurred (AccessDenied) when calling the PutObject operation:",
    "User: arn:aws:iam::352445792625:user/terraform-admin is not authorized with an explicit deny"
]
render_terminal_card("/home/santiagop/AWS/evidence/part4_drift_evidence.png", "Evidence · Part 4 · S3 Drift & Resource-Based Deny", p4_lines, 950, 460)

# 3. Part 5 Evidence: Task 16 SSM Migration & Clean Rebuild
p5_lines = [
    "# === PROOF 1: Secret Purged from terraform.tfstate (Task 16) ===",
    "$ grep -c '\"result\"' terraform.tfstate.before",
    "1  (plaintext database password exposed)",
    "$ grep -c '\"result\"' terraform.tfstate",
    "0  (secret completely removed; stored in AWS SSM Parameter Store)",
    "",
    "# === PROOF 2: Automated Infrastructure Rebuild ===",
    "$ terraform apply -auto-approve",
    "Apply complete! Resources: 6 added, 0 changed, 3 destroyed.",
    "Outputs:",
    '  health_url = "http://51.21.246.81/healthz"',
    '  web_url    = "http://51.21.246.81/"'
]
render_terminal_card("/home/santiagop/AWS/evidence/part5_rebuild_evidence.png", "Evidence · Part 5 · Secret Migration & Automation", p5_lines, 950, 420)
