import json

# 读取 issue 数据
with open("./data/issue_info.json", "r", encoding="utf-8") as f:
    issues = json.load(f)

# 总 issue 数量
total_issues = len(issues)

# issue 状态统计
open_issues = [issue for issue in issues if issue["state"] == "open"]
closed_issues = [issue for issue in issues if issue["state"] == "closed"]

# issue 创建时间和更新时间
created_dates = [issue["created_at"] for issue in issues]
updated_dates = [issue["updated_at"] for issue in issues]

# 用户提交情况统计
user_issues = {}
for issue in issues:
    user = issue["user"]
    if user not in user_issues:
        user_issues[user] = 0
    user_issues[user] += 1

# issue 评论数统计
comments_count = [issue["comments"] for issue in issues]

# 打印分析结果
print(f"总 issue 数量: {total_issues}")
print(f"Open issues: {len(open_issues)}")
print(f"Closed issues: {len(closed_issues)}")
print(f"最早的 issue 创建时间: {min(created_dates)}")
print(f"最新的 issue 创建时间: {max(created_dates)}")
print(f"最早的 issue 更新时间: {min(updated_dates)}")
print(f"最新的 issue 更新时间: {max(updated_dates)}")
print("用户提交情况:")
for user, count in user_issues.items():
    print(f"  用户 {user}: 提交了 {count} 个 issue")
print(
    f"平均评论数: {sum(comments_count) / len(comments_count) if comments_count else 0:.2f}"
)
