import requests
import datetime

GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'  # 用GitHub Actions secret注入
SEARCH_KEYWORDS = ['AI', 'artificial intelligence', 'LLM', 'chatgpt', 'diffusion', 'text2image']
PER_PAGE = 20
DAYS = 1  # 统计最近1天

def fetch_latest_repos():
    today = datetime.datetime.utcnow()
    since = (today - datetime.timedelta(days=DAYS)).strftime('%Y-%m-%dT%H:%M:%SZ')
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    repos = []
    for keyword in SEARCH_KEYWORDS:
        url = f"https://api.github.com/search/repositories?q={keyword}+created:>{since}&sort=stars&order=desc&per_page={PER_PAGE}"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json().get('items', [])
            for repo in data:
                repos.append({
                    'name': repo['name'],
                    'desc': repo['description'],
                    'stars': repo['stargazers_count'],
                    'created_at': repo['created_at'][:10],
                    'url': repo['html_url']
                })
    # 去重
    unique = {f"{r['name']}_{r['url']}": r for r in repos}.values()
    return sorted(unique, key=lambda x: x['stars'], reverse=True)

def save_markdown(repos, filename='latest-ai-tools.md'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('# 每日GitHub最新AI工具榜单（自动更新）\n\n')
        f.write('| 项目名 | 简介 | Stars | 创建时间 | 链接 |\n')
        f.write('|--------|------|-------|----------|------|\n')
        for r in repos:
            desc = r['desc'].replace('\n', ' ').replace('|', '\\|') if r['desc'] else ''
            f.write(f"| {r['name']} | {desc} | {r['stars']} | {r['created_at']} | [GitHub]({r['url']}) |\n")

if __name__ == "__main__":
    repos = fetch_latest_repos()
    save_markdown(repos)
