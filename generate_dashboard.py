
from github import Github
import os
from datetime import datetime

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = "PowertrainLab"
REPOS = [
    "Powertrain_Control_Simulation",
    "MBD_Powertrain_Torque_Control",
    "Engine_ECU_Calibration",
    "ISO_26262_Functional_Safety",
    "CAN_Bus_Data_Analysis",
    "Automotive_Sensor_Fusion"
]

g = Github(GITHUB_TOKEN)
org = g.get_organization(ORG_NAME)

dashboard_md = "# 📊 Powertrain Engineering Lab Dashboard\n\n"
dashboard_md += f"Last updated: `{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`\n\n"
dashboard_md += "| Repository | Open Issues | Closed Issues | Completion % | Last Log Update |\n"
dashboard_md += "|------------|-------------|---------------|---------------|-----------------|\n"

for repo_name in REPOS:
    repo = org.get_repo(repo_name)
    open_issues = repo.get_issues(state='open')
    closed_issues = repo.get_issues(state='closed')
    num_open = open_issues.totalCount
    num_closed = closed_issues.totalCount
    total = num_open + num_closed
    percent_complete = int((num_closed / total) * 100) if total > 0 else 0

    try:
        file_content = repo.get_contents("results/performance_log.txt").decoded_content.decode()
        last_log = file_content.strip().split('\n')[-1]
    except:
        last_log = "N/A"

    dashboard_md += f"| `{repo_name}` | {num_open} | {num_closed} | **{percent_complete}%** | `{last_log}` |\n"

with open("dashboard.md", "w") as f:
    f.write(dashboard_md)
print("✅ Generated dashboard.md")
