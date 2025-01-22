import subprocess
import os
import glob
from reportlab.lib.pagesizes import letter, landscape  # 导入 landscape 以设置PDF为横向
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
        errors="replace"  # 遇到无法解码的字符时替换为占位符
    )
    print(f"Command completed with return code: {result.returncode}")  # 打印返回码
    print(f"Command output: {result.stdout}")  # 打印标准输出
    print(f"Command error: {result.stderr}")  # 打印标准错误

    # 处理错误信息
    if result.returncode != 0:
        print("Analysis failed with the following errors:")
        for line in result.stderr.splitlines():
            print(line)
        return None, result.stderr
    else:
        return result.stdout, result.stderr


def generate_pdf_report(report_data, output_path, font_path, pdf_width=1000):
    """
    生成 PDF 报告。

    :param report_data: 要写入 PDF 的报告数据
    :param output_path: 输出 PDF 的路径
    :param font_path: 支持中文的字体文件路径（如 msyh.ttc）
    :param pdf_width: PDF 的宽度（自定义）
    """
    # 注册中文字体
    pdfmetrics.registerFont(TTFont("MSYH", font_path))

    # 创建 PDF 画布，设置为横向
    c = canvas.Canvas(output_path, pagesize=(pdf_width, landscape(letter)[1]))  # 使用自定义宽度
    width, height = pdf_width, landscape(letter)[1]

    # 设置字体为支持中文的字体
    c.setFont("MSYH", 12)

    # 添加标题
    c.drawString(30, height - 30, "静态分析报告")
    c.line(30, height - 32, width - 30, height - 32)
    y = height - 50

    # 写入报告内容
    for entry in report_data:
        c.drawString(30, y, entry)
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
    all_results = []  # 用于最终报告的集合

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
                all_results.append(f"Error in {os.path.basename(cs_file)}: {error.strip()}")
            elif output is None:
                f.write("Error: No output from C# analyzer.\n")
                report_data.append(f"Error in {os.path.basename(cs_file)}: No output from C# analyzer.")
                all_results.append(f"Error in {os.path.basename(cs_file)}: No output from C# analyzer.")
            else:
                f.write(output)
                # 将输出按行分割，并添加到报告数据中
                report_data.append(f"Results for {os.path.basename(cs_file)}:")
                all_results.append(f"Results for {os.path.basename(cs_file)}:")
                for line in output.strip().splitlines():
                    report_data.append(f"    {line.strip()}")  # 每条信息前加空格格式化
                    all_results.append(f"    {line.strip()}")  # 每条信息前加空格格式化

        print(f"Results saved to {result_file}")

    # 生成每个文件的单独 PDF 报告
    individual_pdf_path = os.path.join(output_folder, f"{module_name}_analysis_report.pdf")
    generate_pdf_report(report_data, individual_pdf_path, font_path)
    print(f"Individual PDF report generated at {individual_pdf_path}")

    return all_results


def analyze_single_cs_files(analyzer_path, root_path, output_folder, font_path):
    """
    分析直接存放在模块路径下的所有单独的 C# 文件。

    :param analyzer_path: C# 分析器的路径
    :param root_path: 包含 C# 文件的根路径
    :param output_folder: 输出文件夹路径
    :param font_path: 支持中文的字体文件路径（如 msyh.ttc）
    """
    report_data = []
    all_results = []  # 用于最终报告的集合

    cs_files = [f for f in os.listdir(root_path) if f.endswith('.cs') and os.path.isfile(os.path.join(root_path, f))]

    for cs_file in cs_files:
        file_path = os.path.join(root_path, cs_file)
        print(f"Analyzing single file: {file_path}...")
        output, error = run_csharp_analyzer(analyzer_path, file_path)

        result_file = os.path.join(output_folder, f"{os.path.basename(cs_file)}.result")

        # 使用 utf-8 编码写入文件，并处理可能的编码错误
        with open(result_file, "w", encoding="utf-8", errors="replace") as f:
            if error:
                f.write(f"Error: {error}\n")
                report_data.append(f"Error in {os.path.basename(cs_file)}: {error.strip()}")
                all_results.append(f"Error in {os.path.basename(cs_file)}: {error.strip()}")
            elif output is None:
                f.write("Error: No output from C# analyzer.\n")
                report_data.append(f"Error in {os.path.basename(cs_file)}: No output from C# analyzer.")
                all_results.append(f"Error in {os.path.basename(cs_file)}: No output from C# analyzer.")
            else:
                f.write(output)
                # 将输出按行分割，并添加到报告数据中
                report_data.append(f"Results for {os.path.basename(cs_file)}:")
                all_results.append(f"Results for {os.path.basename(cs_file)}:")
                for line in output.strip().splitlines():
                    report_data.append(f"    {line.strip()}")  # 每条信息前加空格格式化
                    all_results.append(f"    {line.strip()}")  # 每条信息前加空格格式化

        print(f"Results saved to {result_file}")

        # 生成每个单独文件的 PDF 报告
        individual_pdf_path = os.path.join(output_folder, f"{os.path.basename(cs_file)}_analysis_report.pdf")
        generate_pdf_report(report_data, individual_pdf_path, font_path)
        print(f"Individual PDF report generated at {individual_pdf_path}")

    return all_results


def generate_final_report(all_results, output_folder, font_path):
    """
    生成最终汇总报告 PDF。

    :param all_results: 所有分析结果
    :param output_folder: 输出文件夹路径
    :param font_path: 支持中文的字体文件路径
    """
    final_report_path = os.path.join(output_folder, "final_static_analysis_report.pdf")
    generate_pdf_report(all_results, final_report_path, font_path)
    print(f"Final report generated at {final_report_path}")


def main():
    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 相对路径设置
    analyzer_path = os.path.join(script_dir, "static_analysis_cs", "bin", "Debug", "net8.0", "static_analysis_cs.dll")
    repo_path = os.path.join(script_dir, "..", "repo", "SteamTools", "src")
    output_folder = os.path.join(script_dir, "..", "results", "static_analysis")
    font_path = os.path.join(script_dir, "..", "src", "msyh.ttc")  # 字体文件路径

    os.makedirs(output_folder, exist_ok=True)

    all_results = []  # 用于最终报告的集合

    # 获取所有模块
    modules = [os.path.join(repo_path, module) for module in os.listdir(repo_path) if
               os.path.isdir(os.path.join(repo_path, module))]

    for module in modules:
        print(f"Analyzing module: {os.path.basename(module)}")
        module_results = analyze_module(analyzer_path, module, output_folder, font_path)
        all_results.extend(module_results)

    # 处理直接存放在 src 目录下的 .cs 文件
    single_file_results = analyze_single_cs_files(analyzer_path, repo_path, output_folder, font_path)
    all_results.extend(single_file_results)

    # 生成最终汇总报告
    generate_final_report(all_results, output_folder, font_path)


if __name__ == "__main__":
    main()
