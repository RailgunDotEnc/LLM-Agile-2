# JiraAPI(email: Str, api_token: Str, jira_domain: Str) -> JiraAPI Instance 
# get_story(self, issue_key: Str) -> Output: [issue description]
# get_story_list(self, project_key: Str) -> Output: [(issue key, issue description), .... , (issue key, issue description)]

import requests
import json
import base64

class JiraAPI:
    def __init__(self, email, api_token, jira_domain):
        self.email = email
        self.api_token = api_token
        self.jira_domain = jira_domain

    def encode_credentials(self):
        credentials = f"{self.email}:{self.api_token}"
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    def get_story(self, issue_key):
        encoded_credentials = self.encode_credentials()
        jira_url = f"https://{self.jira_domain}/rest/api/3/issue/{issue_key}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }
        response = requests.get(jira_url, headers=headers)
        if response.status_code == 200:
            issue_details = response.json()
            issue_parsed = [issue_details.get("fields")["issuetype"]['description']] #Asked for description, commands, acceptance FIXME
            return issue_parsed
        else:
            return []

    def get_story_list(self, project_key):
        encoded_credentials = self.encode_credentials()
        jira_url = f"https://{self.jira_domain}/rest/api/3/search"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }
        jql = f"project = {project_key} ORDER BY created DESC"
        params = {'jql': jql, 'maxResults': 10}
        response = requests.get(jira_url, headers=headers, params=params)
        if response.status_code == 200:
            issues = response.json().get('issues', [])
            issue_keys = [(issue.get('key'), issue.get('fields')['issuetype']['description']) for issue in issues]
            return issue_keys
        else:
            print(f"Failed to retrieve issues. Response: {response.status_code}, {response.text}")
            return []

if __name__ == '__main__':
    email = ""
    api_token = ""
    jira_domain = ""
    jira_api = JiraAPI(email, api_token, jira_domain)

    # Test get_story function
    print("FP-1 " + str(jira_api.get_story("FP-1")))

    # Test get_story_list function
    print("Story List " + str(jira_api.get_story_list("FP")))
