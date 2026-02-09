import os
import yaml
from git import Repo

class GitConnector:
    def __init__(self, config_path="config/framework.yaml"):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.git_config = config.get('git', {})
        
        self.repo_path = os.getcwd()
        self.remote_url = self.git_config.get('remote_url')
        self.branch = self.git_config.get('branch', 'main')
        
        try:
            self.repo = Repo(self.repo_path)
        except Exception:
            print("Not a git repository. Initializing...")
            self.repo = Repo.init(self.repo_path)

    def commit_and_push(self, message, files=None):
        try:
            if files:
                self.repo.index.add(files)
            else:
                self.repo.git.add(A=True)
            
            self.repo.index.commit(message)
            
            if self.remote_url:
                if 'origin' not in self.repo.remotes:
                    self.repo.create_remote('origin', self.remote_url)
                
                origin = self.repo.remote(name='origin')
                origin.push(self.branch)
                print(f"Changes pushed to {self.branch}")
            else:
                print("Remote URL not configured. Committed locally.")
        except Exception as e:
            print(f"Git operation failed: {e}")
