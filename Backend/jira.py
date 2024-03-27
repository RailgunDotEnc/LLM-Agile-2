import json
from api import get_encoded_credentials, make_get_request

# JIRA domain and credentials
jira_domain = "YOUR_DOMAIN.atlassian.net"
email = "YOUR_EMAIL"
api_token = "YOUR_API_TOKEN"

# Credentials
encoded_credentials = get_encoded_credentials(email, api_token)

# JIRA Search API URL
jira_url = f"https://{jira_domain}/rest/api/3/search"

# Headers for the request
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Basic {encoded_credentials}"
}

# The project key from which to retrieve issues
project_key = "FP"

# Constructing JQL query
jql = f"project = {project_key} ORDER BY created DESC"

# Parameters for the request, including the JQL query
params = {
    'jql': jql,
    'maxResults': 10
}

def get_jira_issues():
    # Sending GET request to the JIRA Search API
    response = make_get_request(jira_url, headers, params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parsing the response to get issues
        issues = response.json()['issues']
        print(f"Found {len(issues)} issues in project {project_key}:")
        
        for issue in issues:
            print(f"- {issue['key']}: {issue['fields']['summary']}")
    else:
        print("Failed to retrieve issues.")
        print(f"Response: {response.status_code}, {response.text}")

if __name__ == "__main__":
    get_jira_issues()