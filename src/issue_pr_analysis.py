import json
from datetime import datetime
from collections import Counter


# 读取JSON数据
def load_issues(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# 计算解决时间（秒）
def calculate_resolution_time(created_at, closed_at):
    created_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    closed_time = datetime.fromisoformat(closed_at.replace("Z", "+00:00"))
    return (closed_time - created_time).total_seconds()


# 分析问题解决情况
def analyze_issue_resolution(file_path):
    issues = load_issues(file_path)

    # 已解决和未解决的问题计数
    resolved_count = 0
    open_count = 0
    total_resolution_time = 0
    resolved_issues = 0

    authors_close = [
        issue["user"]["login"] for issue in issues if issue["state"] == "closed"
    ]
    authors = [issue["user"]["login"] for issue in issues]
    author_close_counts = Counter(authors_close)
    author_counts = Counter(authors)
    # 遍历每个issue
    for issue in issues:
        # Track the author
        # 分析已解决和未解决的问题
        if issue["state"] == "closed" and issue.get("closed_at"):
            resolved_count += 1
            resolution_time = calculate_resolution_time(
                issue["created_at"], issue["closed_at"]
            )
            total_resolution_time += resolution_time
            resolved_issues += 1
        elif issue["state"] == "open":
            open_count += 1

    # 计算解决率
    total_issues = resolved_count + open_count
    resolution_rate = (resolved_count / total_issues) * 100 if total_issues > 0 else 0

    # 计算平均解决时间
    avg_resolution_time = (
        total_resolution_time / resolved_issues if resolved_issues > 0 else 0
    )
    avg_resolution_time_hours = avg_resolution_time / 3600  # 转换为小时

    # 打印解决率和平均解决时间
    print(f"解决率: {resolution_rate:.2f}%")
    print(f"平均解决时间: {avg_resolution_time_hours:.2f} 小时")

    # 问题解决率大于等于75%视为提出高质量问题作者
    high_efficiency_author = 0

    # 打印作者解决情况
    print("\n作者问题解决率:")
    for author, count in author_counts.items():
        author_close_count = author_close_counts.get(author, 0)

        author_resolution_rate = (
            (author_close_count / count) * 100 if author_close_count > 0 else 0
        )
        if author_resolution_rate > 75:
            high_efficiency_author += 1

        print(f"{author}: 问题解决率:{author_resolution_rate:.2f}%")

    high_efficiency_author_rate = high_efficiency_author / len(author)
    print(f"高质量作者比例:{high_efficiency_author_rate:.2f}%")


# 示例：调用函数并分析数据
file_path = "./data/issue_info.json"
analyze_issue_resolution(file_path)
