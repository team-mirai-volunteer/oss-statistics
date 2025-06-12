#!/usr/bin/env python3
"""
GitHub組織の統計情報を収集するスクリプト（gh CLI使用版）
"""

import subprocess
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class GitHubStatsCollectorGH:
    def __init__(self, org_name: str):
        self.org_name = org_name
        
    def run_gh_command(self, cmd: List[str]) -> str:
        """gh CLIコマンドを実行して結果を取得"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"コマンドエラー: {' '.join(cmd)} - {e.stderr}")
            return ""
    
    def get_public_repos(self) -> List[Dict[str, Any]]:
        """組織の全パブリックリポジトリを取得"""
        cmd = ['gh', 'repo', 'list', self.org_name, '--json', 'name,createdAt,updatedAt,description', '--limit', '1000']
        output = self.run_gh_command(cmd)
        if output:
            return json.loads(output)
        return []
    
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
            commits_cmd = ['gh', 'api', f'repos/{self.org_name}/{repo_name}/commits', '--paginate']
            commits_raw = self.run_gh_command(commits_cmd)
            if commits_raw:
                try:
                    commits_data = json.loads(commits_raw)
                    stats['commits'] = len(commits_data)
                except json.JSONDecodeError:
                    pass
            
            prs_cmd = ['gh', 'api', f'repos/{self.org_name}/{repo_name}/pulls?state=all', '--paginate']
            prs_raw = self.run_gh_command(prs_cmd)
            if prs_raw:
                try:
                    prs_data = json.loads(prs_raw)
                    stats['prs'] = len(prs_data)
                except json.JSONDecodeError:
                    pass
            
            contributors_cmd = ['gh', 'api', f'repos/{self.org_name}/{repo_name}/contributors', '--paginate']
            contributors_raw = self.run_gh_command(contributors_cmd)
            if contributors_raw:
                try:
                    contributors_data = json.loads(contributors_raw)
                    stats['contributors'] = len(contributors_data)
                except json.JSONDecodeError:
                    pass
                
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
            repo_stats['created_at'] = repo.get('createdAt', '')
            repo_stats['updated_at'] = repo.get('updatedAt', '')
            
            all_stats['repositories'].append(repo_stats)
        
        return all_stats

def main():
    collector = GitHubStatsCollectorGH('team-mirai-volunteer')
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
