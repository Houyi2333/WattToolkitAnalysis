import json
from datetime import datetime


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

    # 遍历每个issue
    for issue in issues:
        if issue["state"] == "closed" and issue["closed_at"]:
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
    print(f"问题解决率: {resolution_rate:.2f}%")
    print(f"平均解决时间: {avg_resolution_time_hours:.2f} 小时")


# 主函数
if __name__ == "__main__":
    file_path = "./data/issue_info.json"
    analyze_issue_resolution(file_path)
