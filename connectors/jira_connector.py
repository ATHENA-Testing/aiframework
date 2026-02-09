import os
import yaml
from jira import JIRA
from requests_oauthlib import OAuth1

class JiraConnector:
    def __init__(self, config_path="config/framework.yaml"):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.jira_config = config.get('jira', {})
        
        self.server = self.jira_config.get('server')
        self.auth_method = self.jira_config.get('auth_method', 'api_token')
        self.client = self._authenticate()

    def _authenticate(self):
        if not self.server:
            print("JIRA Server URL not configured.")
            return None

        try:
            if self.auth_method == 'api_token':
                email = self.jira_config.get('email')
                api_token = self.jira_config.get('api_token')
                return JIRA(server=self.server, basic_auth=(email, api_token))
            
            elif self.auth_method == 'sso_oauth':
                # Simplified OAuth1 placeholder for SSO/OAuth
                # In real scenarios, this requires private keys and consumer keys
                consumer_key = self.jira_config.get('consumer_key')
                access_token = self.jira_config.get('access_token')
                access_token_secret = self.jira_config.get('access_token_secret')
                key_cert = self.jira_config.get('key_cert')
                
                oauth_dict = {
                    'access_token': access_token,
                    'access_token_secret': access_token_secret,
                    'consumer_key': consumer_key,
                    'key_cert': key_cert
                }
                return JIRA(server=self.server, oauth=oauth_dict)
            
            else:
                print(f"Unsupported auth method: {self.auth_method}")
                return None
        except Exception as e:
            print(f"Failed to connect to JIRA: {e}")
            return None

    def get_issue_details(self, issue_key):
        if not self.client: return None
        issue = self.client.issue(issue_key)
        return {
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'status': issue.fields.status.name
        }

    def update_test_result(self, issue_key, comment, status=None):
        if not self.client: return
        self.client.add_comment(issue_key, comment)
        if status:
            # Transition logic would go here
            pass
