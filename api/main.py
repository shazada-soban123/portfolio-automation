#!/usr/bin/env python3
"""
Portfolio Automation - Main Runner
Complete workflow: Google Sheet Data → Portfolio Website → GitHub → Email
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from website_generator.generate import generate_portfolio
from api.github_integration import GitHubIntegration
from emails.notification import EmailNotifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', 'shazada-soban123')
ADMIN_EMAIL = 'sobanluminai@gmail.com'
CALENDLY_LINK = 'https://cal.com/shazada-soban/quick-chat?overlayCalendar=true'


class PortfolioAutomation:
    def __init__(self):
        self.github = GitHubIntegration(GITHUB_TOKEN, GITHUB_USERNAME)
        self.emailer = EmailNotifier()

    def run_full_workflow(self, data):
        """
        Execute complete automation workflow:
        1. Generate portfolio website
        2. Deploy to GitHub
        3. Send notification emails
        """
        logger.info(f"Starting workflow for: {data.get('full_name', 'Unknown')}")

        results = {
            'full_name': data.get('full_name'),
            'email': data.get('email'),
            'steps': {}
        }

        # Step 1: Generate Portfolio Website
        logger.info("Step 1: Generating portfolio website...")
        portfolio_result = generate_portfolio(data)

        if not portfolio_result['success']:
            results['steps']['generation'] = {'success': False, 'error': portfolio_result.get('error')}
            return results

        results['steps']['generation'] = {'success': True, 'path': portfolio_result['path']}
        website_path = portfolio_result['path']
        slug = portfolio_result['slug']

        logger.info(f"Portfolio generated at: {website_path}")

        # Step 2: Deploy to GitHub
        logger.info("Step 2: Deploying to GitHub...")
        deploy_result = self.github.deploy_portfolio(data, website_path)

        if not deploy_result['success']:
            results['steps']['deployment'] = {'success': False, 'error': deploy_result.get('error')}
            return results

        results['steps']['deployment'] = deploy_result
        website_url = deploy_result.get('website_url', deploy_result.get('repo_url'))
        results['website_url'] = website_url

        logger.info(f"Deployed to: {website_url}")

        # Step 3: Send Notification Emails
        logger.info("Step 3: Sending notification emails...")
        data['website_url'] = website_url
        email_results = self.emailer.send_portfolio_notification(data, website_url)

        results['steps']['emails'] = email_results
        results['success'] = True

        logger.info("Workflow completed successfully!")
        return results


def process_webhook(data):
    """Process incoming webhook data"""
    automation = PortfolioAutomation()
    return automation.run_full_workflow(data)


def main():
    """Main entry point for command-line usage"""
    if len(sys.argv) > 1:
        # Read data from file
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        # Read from stdin
        data = json.load(sys.stdin)

    results = process_webhook(data)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
