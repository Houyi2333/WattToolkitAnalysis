import subprocess
import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  # 导入 TTFont 以加载自定义字体

def run_csharp_analyzer(analyzer_path, target_file):
    """
    运行 C# 分析器并返回输出和错误信息。

    :param analyzer_path: C# 分析器的路径
    :param target_file: 要分析的 C# 文件路径
    :return: 分析输出和错误
    """
    command = ["dotnet", analyzer_path, target_file]
    print(f"Running command: {' '.join(command)}")  # 打印运行的命令
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",  # 明确指定编码为 utf-8
        errors="replace"   # 遇到无法解码的字符时替换为占位符
    )
    print(f"Command completed with return code: {result.returncode}")  # 打印返回码
    print(f"Command output: {result.stdout}")  # 打印标准输出
    print(f"Command error: {result.stderr}")   # 打印标准错误

    # 处理错误信息
    if result.returncode != 0:
        print("Analysis failed with the following errors:")
        for line in result.stderr.splitlines():
            print(line)
        return None, result.stderr
    else:
        return result.stdout, result.stderr

def generate_pdf_report(report_data, output_path, font_path):
    """
    生成 PDF 报告。

    :param report_data: 要写入 PDF 的报告数据
    :param output_path: 输出 PDF 的路径
    :param font_path: 支持中文的字体文件路径（如 msyh.ttc）
    """
    # 注册中文字体
    pdfmetrics.registerFont(TTFont("MSYH", font_path))

    # 创建 PDF 画布
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # 设置字体为支持中文的字体
    c.setFont("MSYH", 12)

    # 添加标题
    c.drawString(30, height - 30, "静态分析报告")
    c.line(30, height - 32, 580, height - 32)
    y = height - 50

    # 写入报告内容
    for line in report_data:
        c.drawString(30, y, line)
        y -= 15
        if y < 50:  # 如果内容超出页面，创建新页面
            c.showPage()
            c.setFont("MSYH", 12)
            y = height - 50

    # 保存 PDF
    c.save()

def analyze_module(analyzer_path, module_path, output_folder, font_path):
    """
    分析一个模块中的所有 C# 文件。

    :param analyzer_path: C# 分析器的路径
    :param module_path: 模块的路径
    :param output_folder: 输出文件夹路径
    :param font_path: 支持中文的字体文件路径（如 msyh.ttc）
    :return: 模块的分析结果
    """
    module_name = os.path.basename(module_path)
    module_output_folder = os.path.join(output_folder, module_name)
    os.makedirs(module_output_folder, exist_ok=True)

    report_data = []

    # 获取模块中的所有 .cs 文件
    cs_files = glob.glob(os.path.join(module_path, "**", "*.cs"), recursive=True)

    for cs_file in cs_files:
        print(f"Analyzing {cs_file}...")
        output, error = run_csharp_analyzer(analyzer_path, cs_file)

        result_file = os.path.join(module_output_folder, f"{os.path.basename(cs_file)}.result")

        # 使用 utf-8 编码写入文件，并处理可能的编码错误
        with open(result_file, "w", encoding="utf-8", errors="replace") as f:
            if error:
                f.write(f"Error: {error}\n")
                report_data.append(f"Error in {os.path.basename(cs_file)}: {error.strip()}")
            elif output is None:
                f.write("Error: No output from C# analyzer.\n")
                report_data.append(f"Error in {os.path.basename(cs_file)}: No output from C# analyzer.")
            else:
                f.write(output)
                report_data.append(f"Results for {os.path.basename(cs_file)}:\n{output.strip()}")

        print(f"Results saved to {result_file}")

    # 生成模块的 PDF 报告，直接保存在 ./results/{模块名}.pdf
    pdf_path = os.path.join(output_folder, f"{module_name}.pdf")  # 修改路径
    generate_pdf_report(report_data, pdf_path, font_path)
    print(f"PDF report generated at {pdf_path}")

def main():
    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 相对路径设置
    analyzer_path = os.path.join(script_dir, "static_analysis_cs", "bin", "Debug", "net8.0", "static_analysis_cs.dll")
    repo_path = os.path.join(script_dir, "..", "repo", "SteamTools", "src")
    output_folder = os.path.join(script_dir, "..", "results", "static_analysis")
    font_path = os.path.join(script_dir, "..", "src", "msyh.ttc")  # 字体文件路径

    os.makedirs(output_folder, exist_ok=True)

    # 获取所有模块
    modules = [os.path.join(repo_path, module) for module in os.listdir(repo_path) if os.path.isdir(os.path.join(repo_path, module))]

    for module in modules:
        print(f"Analyzing module: {os.path.basename(module)}")
        analyze_module(analyzer_path, module, output_folder, font_path)

if __name__ == "__main__":
    main()
