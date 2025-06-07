#!/usr/bin/env python3
"""
GitHub組織の統計情報を収集するスクリプト
"""

import requests
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any

class GitHubStatsCollector:
    def __init__(self, org_name: str, token: str = None):
        self.org_name = org_name
        self.token = token
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'token {token}'
        
    def get_public_repos(self) -> List[Dict[str, Any]]:
        """組織の全パブリックリポジトリを取得"""
        url = f"https://api.github.com/orgs/{self.org_name}/repos"
        params = {
            'type': 'public',
            'per_page': 100
        }
        
        repos = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"エラー: {response.status_code} - {response.text}")
                break
                
            page_repos = response.json()
            if not page_repos:
                break
                
            repos.extend(page_repos)
            page += 1
            
        return repos
    
    def get_repo_stats(self, repo_name: str) -> Dict[str, Any]:
        """個別リポジトリの統計情報を取得"""
        stats = {
            'name': repo_name,
            'commits': 0,
            'prs': 0,
            'contributors': 0,
            'error': None
        }
        
        try:
            commits_url = f"https://api.github.com/repos/{self.org_name}/{repo_name}/commits"
            commits_response = requests.get(commits_url, headers=self.headers, params={'per_page': 1})
            
            if commits_response.status_code == 200:
                link_header = commits_response.headers.get('Link', '')
                if 'last' in link_header:
                    last_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if last_match:
                        stats['commits'] = int(last_match.group(1))
                    else:
                        stats['commits'] = 1
                else:
                    commits_data = commits_response.json()
                    stats['commits'] = len(commits_data) if commits_data else 0
            
            prs_url = f"https://api.github.com/repos/{self.org_name}/{repo_name}/pulls"
            prs_response = requests.get(prs_url, headers=self.headers, params={'state': 'all', 'per_page': 1})
            
            pr_count = 0
            if prs_response.status_code == 200:
                link_header = prs_response.headers.get('Link', '')
                if 'last' in link_header:
                    last_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if last_match:
                        pr_count = int(last_match.group(1))
                else:
                    prs_data = prs_response.json()
                    pr_count = len(prs_data) if prs_data else 0
            
            issues_url = f"https://api.github.com/repos/{self.org_name}/{repo_name}/issues"
            issues_response = requests.get(issues_url, headers=self.headers, params={'state': 'all', 'per_page': 1})
            
            issue_count = 0
            if issues_response.status_code == 200:
                issues_data = issues_response.json()
                if issues_data:
                    issue_count = max(issue['number'] for issue in issues_data)
            
            stats['prs'] = max(pr_count, issue_count)
            
            contributors_url = f"https://api.github.com/repos/{self.org_name}/{repo_name}/contributors"
            contributors_response = requests.get(contributors_url, headers=self.headers, params={'per_page': 1})
            
            if contributors_response.status_code == 200:
                link_header = contributors_response.headers.get('Link', '')
                if 'last' in link_header:
                    last_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if last_match:
                        stats['contributors'] = int(last_match.group(1))
                else:
                    contributors_data = contributors_response.json()
                    stats['contributors'] = len(contributors_data) if contributors_data else 0
                
        except Exception as e:
            stats['error'] = str(e)
            
        return stats
    
    def collect_all_stats(self) -> Dict[str, Any]:
        """全リポジトリの統計情報を収集"""
        print(f"組織 {self.org_name} の統計情報を収集中...")
        
        repos = self.get_public_repos()
        print(f"パブリックリポジトリ数: {len(repos)}")
        
        all_stats = {
            'organization': self.org_name,
            'collected_at': datetime.now().isoformat(),
            'total_repos': len(repos),
            'repositories': []
        }
        
        for repo in repos:
            repo_name = repo['name']
            print(f"処理中: {repo_name}")
            
            repo_stats = self.get_repo_stats(repo_name)
            repo_stats['description'] = repo.get('description', '')
            repo_stats['created_at'] = repo.get('created_at', '')
            repo_stats['updated_at'] = repo.get('updated_at', '')
            
            all_stats['repositories'].append(repo_stats)
        
        return all_stats

def main():
    token = os.getenv('GITHUB_TOKEN')
    
    collector = GitHubStatsCollector('team-mirai-volunteer', token)
    stats = collector.collect_all_stats()
    
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n統計情報を stats.json に保存しました")
    print(f"総リポジトリ数: {stats['total_repos']}")
    
    total_commits = sum(repo['commits'] for repo in stats['repositories'])
    total_prs = sum(repo['prs'] for repo in stats['repositories'])
    total_contributors = sum(repo['contributors'] for repo in stats['repositories'])
    
    print(f"総コミット数: {total_commits}")
    print(f"総PR数: {total_prs}")
    print(f"総貢献者数: {total_contributors}")

if __name__ == "__main__":
    main()
