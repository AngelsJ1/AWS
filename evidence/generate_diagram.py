import os
from PIL import Image, ImageDraw, ImageFont

# Set up dimensions
width = 1600
height = 1000
img = Image.new("RGB", (width, height), color="#0F172A") # Dark slate background
draw = ImageDraw.Draw(img)

# Load fonts
try:
    title_font = ImageFont.truetype("/usr/share/fonts/TTF/JetBrainsMonoNerdFontPropo-Bold.ttf", 32)
    header_font = ImageFont.truetype("/usr/share/fonts/TTF/JetBrainsMonoNerdFontPropo-Bold.ttf", 22)
    font = ImageFont.truetype("/usr/share/fonts/TTF/JetBrainsMonoNLNerdFontPropo-Regular.ttf", 16)
    font_bold = ImageFont.truetype("/usr/share/fonts/TTF/JetBrainsMonoNerdFontPropo-Bold.ttf", 16)
    small_font = ImageFont.truetype("/usr/share/fonts/TTF/JetBrainsMonoNLNerdFontPropo-Regular.ttf", 14)
except Exception:
    title_font = header_font = font = font_bold = small_font = ImageFont.load_default()

# Title banner
draw.text((50, 30), "2DV705 Assignment 2 — Cloud Infrastructure Architecture", font=title_font, fill="#38BDF8")
draw.text((50, 70), "AWS Region: eu-north-1 (Stockholm) | Account: 352445792625", font=small_font, fill="#94A3B8")

# Draw Public Internet section
draw.rounded_rectangle([40, 120, 280, 920], radius=12, outline="#475569", width=2, fill="#1E293B")
draw.text((60, 140), "PUBLIC INTERNET", font=header_font, fill="#F8FAFC")

# Laptop Box
draw.rounded_rectangle([60, 200, 260, 320], radius=8, outline="#38BDF8", width=2, fill="#0F172A")
draw.text((75, 215), "Student Laptop", font=font_bold, fill="#38BDF8")
draw.text((75, 245), "Arch Linux / Hyprland", font=small_font, fill="#E2E8F0")
draw.text((75, 270), "IP: 94.191.136.213", font=small_font, fill="#94A3B8")
draw.text((75, 292), "SSH & Admin testing", font=small_font, fill="#64748B")

# Web User Box
draw.rounded_rectangle([60, 360, 260, 460], radius=8, outline="#10B981", width=2, fill="#0F172A")
draw.text((75, 375), "Web Client / Browser", font=font_bold, fill="#10B981")
draw.text((75, 405), "HTTP Port 80 Access", font=small_font, fill="#E2E8F0")
draw.text((75, 430), "Source: 0.0.0.0/0", font=small_font, fill="#94A3B8")

# Draw AWS VPC container
draw.rounded_rectangle([320, 120, 1140, 920], radius=16, outline="#6366F1", width=3, fill="#1E1E38")
draw.text((350, 140), "AWS VPC: 10.0.0.0/16 (2dv705)", font=header_font, fill="#A5B4FC")

# Internet Gateway
draw.rounded_rectangle([350, 190, 520, 260], radius=8, outline="#F59E0B", width=2, fill="#292524")
draw.text((365, 205), "Internet Gateway", font=font_bold, fill="#F59E0B")
draw.text((365, 230), "1:1 NAT (igw-xxxx)", font=small_font, fill="#D6D3D1")

# Route Table Public
draw.rounded_rectangle([350, 280, 520, 350], radius=8, outline="#64748B", width=1, fill="#1E293B")
draw.text((365, 295), "Public Route Table", font=font_bold, fill="#94A3B8")
draw.text((365, 320), "0.0.0.0/0 -> igw", font=small_font, fill="#CBD5E1")

# Public Subnet
draw.rounded_rectangle([550, 190, 810, 890], radius=12, outline="#10B981", width=2, fill="#132E27")
draw.text((570, 210), "PUBLIC SUBNET", font=header_font, fill="#34D399")
draw.text((570, 240), "10.0.1.0/24 (eu-north-1a)", font=small_font, fill="#6EE7B7")

# Web Instance Box
draw.rounded_rectangle([570, 280, 790, 560], radius=8, outline="#34D399", width=2, fill="#064E3B")
draw.text((585, 295), "EC2: Web Instance", font=font_bold, fill="#A7F3D0")
draw.text((585, 325), "Type: t3.micro (Ubuntu 24.04)", font=small_font, fill="#E2E8F0")
draw.text((585, 350), "Public IP: Dynamic", font=small_font, fill="#E2E8F0")
draw.text((585, 375), "Private IP: 10.0.1.x", font=small_font, fill="#E2E8F0")
draw.text((585, 405), "--- Security Group: web ---", font=small_font, fill="#FDE047")
draw.text((585, 430), "Inbound :80 (0.0.0.0/0)", font=small_font, fill="#FEF08A")
draw.text((585, 455), "Inbound :22 (Admin IP /32)", font=small_font, fill="#FEF08A")
draw.text((585, 485), "--- User Data / App ---", font=small_font, fill="#A7F3D0")
draw.text((585, 510), "Gunicorn / Flask (lnu-notes)", font=small_font, fill="#E2E8F0")
draw.text((585, 532), "IAM Profile: 2dv705-web", font=small_font, fill="#67E8F9")

# NAT Gateway Box
draw.rounded_rectangle([570, 600, 790, 720], radius=8, outline="#F59E0B", width=2, fill="#451A03")
draw.text((585, 615), "NAT Gateway + EIP", font=font_bold, fill="#FBBF24")
draw.text((585, 645), "Handles DB outbound (apt)", font=small_font, fill="#FEF3C7")
draw.text((585, 670), "No inbound connections", font=small_font, fill="#FCD34D")
draw.text((585, 695), "aws_eip.nat (vpc)", font=small_font, fill="#94A3B8")

# Private Subnet
draw.rounded_rectangle([840, 190, 1110, 890], radius=12, outline="#EF4444", width=2, fill="#35141D")
draw.text((860, 210), "PRIVATE SUBNET", font=header_font, fill="#F87171")
draw.text((860, 240), "10.0.2.0/24 (No Public Route)", font=small_font, fill="#FCA5A5")

# DB Instance Box
draw.rounded_rectangle([860, 280, 1090, 560], radius=8, outline="#F87171", width=2, fill="#7F1D1D")
draw.text((875, 295), "EC2: DB Instance", font=font_bold, fill="#FECACA")
draw.text((875, 325), "Type: t3.micro (Ubuntu 24.04)", font=small_font, fill="#E2E8F0")
draw.text((875, 350), "Public IP: NONE (No route)", font=small_font, fill="#FCA5A5")
draw.text((875, 375), "Private IP: 10.0.2.x", font=small_font, fill="#E2E8F0")
draw.text((875, 405), "--- Security Group: db ---", font=small_font, fill="#FDE047")
draw.text((875, 430), "Inbound :3306 (sg-web only)", font=small_font, fill="#FEF08A")
draw.text((875, 455), "Inbound :22 (NONE - Closed)", font=small_font, fill="#F87171")
draw.text((875, 485), "--- Database Service ---", font=small_font, fill="#FECACA")
draw.text((875, 510), "MariaDB 11 (lnunotes db)", font=small_font, fill="#E2E8F0")
draw.text((875, 532), "cloud-init initialized", font=small_font, fill="#94A3B8")

# Private Route Table Box
draw.rounded_rectangle([860, 600, 1090, 720], radius=8, outline="#64748B", width=1, fill="#1E293B")
draw.text((875, 615), "Private Route Table", font=font_bold, fill="#94A3B8")
draw.text((875, 645), "0.0.0.0/0 -> nat-xxxx", font=small_font, fill="#CBD5E1")
draw.text((875, 670), "Allows yum/apt updates out", font=small_font, fill="#94A3B8")
draw.text((875, 695), "Drops all inbound traffic", font=small_font, fill="#F87171")

# AWS Managed Services Box (Right side)
draw.rounded_rectangle([1170, 120, 1560, 920], radius=16, outline="#38BDF8", width=2, fill="#0F243A")
draw.text((1190, 140), "AWS MANAGED SERVICES", font=header_font, fill="#38BDF8")

# S3 Bucket Box
draw.rounded_rectangle([1190, 200, 1540, 440], radius=8, outline="#38BDF8", width=2, fill="#082F49")
draw.text((1205, 215), "S3: 2dv705-[ID]-notes", font=font_bold, fill="#7DD3FC")
draw.text((1205, 245), "Objects: /notes, /uploads", font=small_font, fill="#E2E8F0")
draw.text((1205, 275), "[x] Block Public Access (All)", font=small_font, fill="#34D399")
draw.text((1205, 305), "[x] Server-Side Encryption (AES256)", font=small_font, fill="#34D399")
draw.text((1205, 335), "[x] Versioning Enabled", font=small_font, fill="#34D399")
draw.text((1205, 365), "[x] Bucket Policy (Deny Non-Role)", font=small_font, fill="#F87171")
draw.text((1205, 395), "Accessible only via Presigned URLs", font=small_font, fill="#FDE047")
draw.text((1205, 417), "Enforces TLS (SecureTransport)", font=small_font, fill="#38BDF8")

# IAM Role Box
draw.rounded_rectangle([1190, 470, 1540, 680], radius=8, outline="#A855F7", width=2, fill="#3B0764")
draw.text((1205, 485), "IAM: Role 2dv705-web", font=font_bold, fill="#D8B4FE")
draw.text((1205, 515), "Attached to Web Instance Profile", font=small_font, fill="#E2E8F0")
draw.text((1205, 545), "Actions: s3:Get/Put/Delete/List", font=small_font, fill="#F5D0FE")
draw.text((1205, 575), "Resource: notes bucket ARN only", font=small_font, fill="#F5D0FE")
draw.text((1205, 605), "Condition: aws:SecureTransport", font=small_font, fill="#F5D0FE")
draw.text((1205, 635), "SSM Task 16: ssm:GetParameter", font=small_font, fill="#FDE047")
draw.text((1205, 657), "NO static keys on instance!", font=small_font, fill="#34D399")

# SSM Parameter Store Box
draw.rounded_rectangle([1190, 710, 1540, 890], radius=8, outline="#EC4899", width=2, fill="#4A044E")
draw.text((1205, 725), "SSM Parameter Store (Task 16)", font=font_bold, fill="#F472B6")
draw.text((1205, 755), "Name: /2dv705/db_password", font=small_font, fill="#FBCFE8")
draw.text((1205, 785), "Type: SecureString (KMS encrypted)", font=small_font, fill="#FBCFE8")
draw.text((1205, 815), "Fetched at boot by cloud-init", font=small_font, fill="#E2E8F0")
draw.text((1205, 845), "Purges password from tfstate!", font=small_font, fill="#34D399")
draw.text((1205, 867), "Zero plaintext secrets in git", font=small_font, fill="#38BDF8")

# Arrows and connection annotations
# Web client to IGW
draw.line([(260, 410), (350, 225)], fill="#10B981", width=3)
draw.polygon([(345, 220), (355, 225), (348, 233)], fill="#10B981")
draw.text((270, 310), "HTTP:80", font=font_bold, fill="#10B981")

# Laptop to Web instance SSH
draw.line([(260, 260), (570, 460)], fill="#38BDF8", width=3)
draw.text((310, 270), "SSH :22 (Admin IP only)", font=font_bold, fill="#38BDF8")

# Web Instance to DB Instance
draw.line([(790, 430), (860, 430)], fill="#FDE047", width=4)
draw.polygon([(852, 423), (860, 430), (852, 437)], fill="#FDE047")
draw.text((795, 405), "MySQL :3306", font=font_bold, fill="#FDE047")

# Laptop to DB block attempt
draw.line([(260, 310), (860, 460)], fill="#EF4444", width=3)
draw.text((450, 490), "BLOCKED: Direct Laptop -> DB :3306 (Timeout)", font=font_bold, fill="#EF4444")

# DB to NAT
draw.line([(975, 560), (975, 600)], fill="#F59E0B", width=2)
draw.line([(860, 660), (790, 660)], fill="#F59E0B", width=3)

# Web Instance to S3
draw.line([(790, 330), (1190, 280)], fill="#38BDF8", width=3)
draw.text((880, 260), "Presigned URLs / S3 API over TLS", font=font_bold, fill="#38BDF8")

# Save diagram
os.makedirs("/home/santiagop/AWS/evidence", exist_ok=True)
img.save("/home/santiagop/AWS/evidence/architecture_diagram.png", "PNG")
print("Architecture diagram generated at /home/santiagop/AWS/evidence/architecture_diagram.png")
