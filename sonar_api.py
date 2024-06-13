import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

# SonarCloud API details
api_token = '8cdf3a2e370ee5866bd052a73a0117835a0bbff7'
organization = 'mansihsangwan-1'
project_key = 'mansihsangwan_UserAPIs'

# Define the API URLs
measures_url = f'https://sonarcloud.io/api/measures/component?component={project_key}&metricKeys=bugs,vulnerabilities,code_smells'
issues_url = f'https://sonarcloud.io/api/issues/search?componentKeys={project_key}'

# Fetch measures data
measures_response = requests.get(measures_url, auth=(api_token, ''))
measures_data = measures_response.json() if measures_response.status_code == 200 else {}

# Fetch issues data
issues_response = requests.get(issues_url, auth=(api_token, ''))
issues_data = issues_response.json() if issues_response.status_code == 200 else {}

# Prepare PDF document
report_title = f'SonarCloud Report for {project_key}'
doc = SimpleDocTemplate("sonarcloud_report.pdf", pagesize=A4)
styles = getSampleStyleSheet()
content = [Paragraph(report_title, styles['Title'])]

# Add measures to the report
if measures_data:
    measures = measures_data.get('component', {}).get('measures', [])
    for measure in measures:
        metric = measure['metric']
        value = measure['value']
        content.append(Paragraph(f'{metric.capitalize()}: {value}', styles['Normal']))

# Add issues to the report
if issues_data:
    total_issues = issues_data.get('total', 0)
    content.append(Paragraph(f'Total Issues: {total_issues}', styles['Normal']))
    for issue in issues_data.get('issues', []):
        issue_type = issue.get('type')
        issue_message = issue.get('message')
        content.append(Paragraph(f'{issue_type.capitalize()}: {issue_message}', styles['Normal']))

# Build PDF
doc.build(content)

print("PDF report generated successfully: sonarcloud_report.pdf")


