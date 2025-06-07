#!/usr/bin/env python3
"""
OSS統計ダッシュボード - Webアプリケーション
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

def load_stats():
    """統計データを読み込み"""
    try:
        with open('stats.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@app.route('/')
def dashboard():
    """メインダッシュボード"""
    stats = load_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/api/stats')
def api_stats():
    """統計データのAPI"""
    stats = load_stats()
    if stats:
        return jsonify(stats)
    else:
        return jsonify({'error': 'データが見つかりません'}), 404

@app.route('/api/refresh')
def refresh_stats():
    """統計データを再収集"""
    import subprocess
    try:
        result = subprocess.run(['python3', 'collect_stats.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'データを更新しました'})
        else:
            return jsonify({'success': False, 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
