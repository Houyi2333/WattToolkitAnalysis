import os
import re


# 将输出写入文件的函数
def write_to_file(message, file_path="output.txt"):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(message + "\n")


# 递归扫描文件夹中的所有 .cs 文件
def scan_all_cs_files(directory, output_file="output.txt"):
    # 确保文件在开始时是空的
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("扫描结果:\n\n")

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".cs"):
                file_path = os.path.join(root, file)
                check_platform_specific_paths(file_path, output_file)
                check_platform_specific_libraries(file_path, output_file)
                check_os_system_calls(file_path, output_file)
                check_preprocessor_directives(file_path, output_file)


# 检查操作系统特定的路径分隔符
def check_platform_specific_paths(code_path, output_file):
    try:
        with open(code_path, "r", encoding="utf-8", errors="ignore") as file:
            code = file.read()
    except UnicodeDecodeError:
        write_to_file(f"无法解码文件（可能是编码问题）：{code_path}", output_file)
        return

    # 检查硬编码的Windows路径分隔符
    windows_paths = re.findall(r"[A-Za-z]:\\(?:[\w]+\\)*[\w]+\.\w+", code)
    if windows_paths:
        write_to_file(f"发现 Windows 特定路径：{code_path}", output_file)
        for path in windows_paths:
            write_to_file(path, output_file)

    # 检查硬编码的Unix路径分隔符
    unix_paths = re.findall(r"/[^/]+(?:/[^/]+)+", code)
    if unix_paths:
        write_to_file(f"发现 Unix 特定路径：{code_path}", output_file)
        for path in unix_paths:
            write_to_file(path, output_file)


# 检查操作系统相关函数调用
def check_os_system_calls(code_path, output_file):
    try:
        with open(code_path, "r", encoding="utf-8", errors="ignore") as file:
            code = file.read()
    except UnicodeDecodeError:
        write_to_file(f"无法解码文件（可能是编码问题）：{code_path}", output_file)
        return

    # 查找操作系统相关的函数调用
    system_calls = re.findall(r"os\.(system|name|environ|chmod|stat|remove)", code)
    if system_calls:
        write_to_file(f"发现与操作系统相关的函数调用：{code_path}", output_file)
        for call in system_calls:
            write_to_file(call, output_file)


# 检查平台特定的库引用
def check_platform_specific_libraries(code_path, output_file):
    try:
        with open(code_path, "r", encoding="utf-8", errors="ignore") as file:
            code = file.read()
    except UnicodeDecodeError:
        write_to_file(f"无法解码文件（可能是编码问题）：{code_path}", output_file)
        return

    # 检查 Windows 特有的库引用
    windows_libraries = re.findall(r"using\s+System\.Windows", code)
    if windows_libraries:
        write_to_file(f"发现 Windows 特有的库：{code_path}", output_file)

    # 检查 Mono 库引用
    mono_libraries = re.findall(r"using\s+Mono\.", code)
    if mono_libraries:
        write_to_file(f"发现 Mono 特有的库：{code_path}", output_file)


# 检查条件编译指令
def check_preprocessor_directives(code_path, output_file):
    try:
        with open(code_path, "r", encoding="utf-8", errors="ignore") as file:
            code = file.read()
    except UnicodeDecodeError:
        write_to_file(f"无法解码文件（可能是编码问题）：{code_path}", output_file)
        return

    # 查找条件编译指令
    preprocessor_directives = re.findall(r"#if\s+([A-Za-z]+)", code)
    if preprocessor_directives:
        write_to_file(f"发现条件编译指令：{code_path}", output_file)
        for directive in preprocessor_directives:
            write_to_file(directive, output_file)


# 运行扫描
directory_path = "../SteamTools"  # 你的项目根目录路径
output_file = "./results/output.txt"  # 输出文件名
scan_all_cs_files(directory_path, output_file)
