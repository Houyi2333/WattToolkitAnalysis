import requests
import os
import json

# GitHub 配置信息
GITHUB_USER = "BeyondDimension"  # GitHub 用户名
GITHUB_REPO = "SteamTools"  # 仓库名
GITHUB_TOKEN = ""  # GitHub 个人访问令牌


# 获取 GitHub 上的 Issue 信息
def get_issues():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}  # 可选，如果你使用 OAuth Token
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issues = response.json()

        issues_data = []
        for issue in issues:
            print(f"Issue #{issue['number']}: {issue['title']}")
            print(f"  状态: {issue['state']}")
            print(f"  标签: {', '.join([label['name'] for label in issue['labels']])}")
            print(f"  创建者: {issue['user']['login']}")
            print(f"  创建时间: {issue['created_at']}")
            print(f"  描述: {issue['body']}")
            print("-" * 60)

            issues_data.append(
                {
                    "id": issue["id"],
                    "title": issue["title"],
                    "state": issue["state"],
                    "created_at": issue["created_at"],
                    "updated_at": issue["updated_at"],
                    "user": issue["user"]["login"],
                    "comments": issue["comments"],
                    "url": issue["html_url"],
                }
            )

    else:
        print(f"无法获取 Issue 信息: {response.status_code}")

    os.makedirs("./data", exist_ok=True)
    with open("./data/issue_info.json", "w", encoding="utf-8") as f:
        json.dump(issues_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    get_issues()
