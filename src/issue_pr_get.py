import requests
import json
import os

GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "BeyondDimension"
REPO_NAME = "SteamTools"
ACCESS_TOKEN = "114514"


def get_all_items(url, params=None):
    items = []
    page = 1
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}
    while True:
        if params is None:
            params = {}
        params.update({"page": page, "per_page": 100})
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data from GitHub API: {response.status_code}")
            break
        page_items = response.json()
        if not page_items:
            break
        items.extend(page_items)
        page += 1
    return items


def get_issues_and_prs(repo_owner, repo_name):
    issues_url = f"{GITHUB_API_URL}/repos/{repo_owner}/{repo_name}/issues"
    prs_url = f"{GITHUB_API_URL}/repos/{repo_owner}/{repo_name}/pulls"

    issues = get_all_items(issues_url, params={"state": "all", "filter": "all"})
    prs = get_all_items(prs_url, params={"state": "all"})

    # 过滤掉 pull requests
    issues = [issue for issue in issues if "pull_request" not in issue]

    return issues, prs


def analyze_issues(issues):
    open_issues = [issue for issue in issues if issue["state"] == "open"]
    closed_issues = [issue for issue in issues if issue["state"] == "closed"]

    print(f"Total issues: {len(issues)}")
    print(f"Open issues: {len(open_issues)}")
    print(f"Closed issues: {len(closed_issues)}")


def analyze_prs(prs):
    open_prs = [pr for pr in prs if pr["state"] == "open"]
    closed_prs = [pr for pr in prs if pr["state"] == "closed"]
    merged_prs = [pr for pr in prs if pr.get("merged_at") is not None]

    print(f"Total pull requests: {len(prs)}")
    print(f"Open pull requests: {len(open_prs)}")
    print(f"Closed pull requests: {len(closed_prs)}")
    print(f"Merged pull requests: {len(merged_prs)}")


def save_data_to_json(data, filename):
    os.makedirs("./data", exist_ok=True)
    with open(f"./data/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    issues, prs = get_issues_and_prs(REPO_OWNER, REPO_NAME)

    if issues is not None and prs is not None:
        analyze_issues(issues)
        analyze_prs(prs)

        save_data_to_json(issues, "issue_info.json")
        save_data_to_json(prs, "pr_info.json")
