"""
GitHub Integration Module
Handles repository creation and deployment
"""

import os
import subprocess
import requests
from pathlib import Path

class GitHubIntegration:
    def __init__(self, token, username):
        self.token = token
        self.username = username
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'

    def create_repository(self, repo_name, description="Portfolio Website"):
        """Create a new GitHub repository"""
        url = f'{self.base_url}/user/repos'
        data = {
            'name': repo_name,
            'description': description,
            'private': False,
            'auto_init': True,
            'has_wiki': False,
            'has_issues': True,
            'has_projects': False
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 201:
            return {'success': True, 'repo_url': response.json()['html_url']}
        elif response.status_code == 422:
            # Repository might already exist
            return {'success': True, 'repo_url': f'https://github.com/{self.username}/{repo_name}'}
        else:
            return {'success': False, 'error': response.text}

    def push_to_repository(self, local_path, repo_name):
        """Push local files to GitHub repository"""
        repo_url = f'https://{self.token}@github.com/{self.username}/{repo_name}.git'
        temp_dir = f'/tmp/{repo_name}'

        try:
            # Clone the repository
            subprocess.run(['rm', '-rf', temp_dir], check=True)
            result = subprocess.run(
                ['git', 'clone', repo_url, temp_dir],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                return {'success': False, 'error': f"Clone failed: {result.stderr}"}

            # Copy files to temp directory
            for item in Path(local_path).iterdir():
                if item.is_file():
                    subprocess.run(['cp', str(item), temp_dir])
                elif item.is_dir() and item.name != '.git':
                    subprocess.run(['cp', '-r', str(item), temp_dir])

            # Configure git
            subprocess.run(['git', 'config', 'user.email', 'automation@portfolio.dev'], cwd=temp_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Portfolio Automation'], cwd=temp_dir, check=True)

            # Add all files
            subprocess.run(['git', '-C', temp_dir, 'add', '.'], check=True)

            # Commit
            commit_result = subprocess.run(
                ['git', '-C', temp_dir, 'commit', '-m', 'Add portfolio website'],
                capture_output=True,
                text=True
            )

            if commit_result.returncode != 0:
                # Check if there's anything to commit
                if 'nothing to commit' in commit_result.stderr:
                    pass  # That's okay
                else:
                    return {'success': False, 'error': f"Commit failed: {commit_result.stderr}"}

            # Push
            push_result = subprocess.run(
                ['git', '-C', temp_dir, 'push', 'origin', 'main'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if push_result.returncode != 0:
                # Try pushing to master if main doesn't exist
                push_result = subprocess.run(
                    ['git', '-C', temp_dir, 'push', 'origin', 'master'],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

            # Clean up
            subprocess.run(['rm', '-rf', temp_dir], check=True)

            if push_result.returncode == 0:
                website_url = f'https://{self.username}.github.io/{repo_name}/'
                return {
                    'success': True,
                    'repo_url': f'https://github.com/{self.username}/{repo_name}',
                    'website_url': website_url
                }
            else:
                return {'success': False, 'error': f"Push failed: {push_result.stderr}"}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def deploy_portfolio(self, portfolio_data, website_path):
        """Complete deployment workflow"""
        # Create repository name
        email_slug = portfolio_data['email'].split('@')[0].replace('.', '-').lower()
        repo_name = f'portfolio-{email_slug}'

        # Create repository
        create_result = self.create_repository(
            repo_name,
            f"Portfolio website for {portfolio_data['full_name']}"
        )

        if not create_result['success']:
            return create_result

        # Push files
        push_result = self.push_to_repository(website_path, repo_name)

        return push_result


def main(data):
    """Main function for processing GitHub deployment"""
    token = os.environ.get('GITHUB_TOKEN', '')
    username = os.environ.get('GITHUB_USERNAME', 'shazada-soban123')

    github = GitHubIntegration(token, username)
    result = github.deploy_portfolio(data, data.get('website_path', ''))

    return result


if __name__ == '__main__':
    import json
    import sys

    data = json.loads(sys.stdin.read())
    result = main(data)
    print(json.dumps(result))
