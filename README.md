# WattToolkitAnalysis

## **项目简介**  

本项目是对开源软件 **[Watt Toolkit](https://github.com/BeyondDimension/SteamTools)** 的全面分析，主要目的是探索开源软件的开发规律和代码质量，并通过静态和动态分析工具挖掘潜在问题，为开源社区贡献改进建议

## **功能特点**  

- **仓库历史分析**：  
  - 提取提交记录，统计活跃度、版本演化规律、贡献者分布等  
- **社区互动研究**：  
  - 分析 Issue 和 Pull Request 的数量、处理效率及常见类型  
- **代码静态分析**：  
  - 评估代码复杂度、规范性，并定位“热点模块”  
- **动态测试与模糊测试**：  
  - 使用模糊测试工具尝试发现隐藏的潜在问题  
- **数据可视化**：  
  - 将分析结果以图表形式直观展示  

## **技术栈与工具**  

- **编程语言**：Python  
- **使用工具**：  
  - 数据分析：`pandas`, `matplotlib`  
  - 静态分析：`libcst`, `ast`, `pylint`  
  - Git 仓库数据获取：`PyGitHub`, `GitPython`  
  - 模糊测试：`AFL`, `fuzzing`  

## **文件结构**  

```plaintext
WattToolkitAnalysis/
├── data/                   # 分析过程中的数据文件
├── src/                    # 代码文件目录
│   ├── commit_analysis.py  # 提交历史分析脚本
│   ├── issue_pr_analysis.py# Issue 和 PR 分析脚本
│   ├── static_analysis.py  # 代码静态分析脚本
│   ├── fuzz_test.py        # 模糊测试实现脚本
│   └── visualization.py    # 数据可视化脚本
├── results/                # 分析结果（图表和报告）
├── README.md               # 项目说明文档
└── requirements.txt        # 依赖库清单
```

---

## **快速开始**  

### **1. 克隆项目**

```bash
git clone https://github.com/username/WattToolkit-Analysis.git
cd WattToolkit-Analysis
```

### **2. 安装依赖**

```bash
pip install -r requirements.txt
```

### **3. 运行分析脚本**

#### 运行提交历史分析：

```bash
python src/commit_analysis.py
```

#### 运行 Issue 和 Pull Request 分析：

```bash
python src/issue_pr_analysis.py
```

#### 运行代码静态分析：

```bash
python src/static_analysis.py
```

#### 运行模糊测试：

```bash
python src/fuzz_test.py
```

## **成果展示**  

分析结果保存在 `results/` 文件夹中，包括：  

- 仓库历史演化的趋势图  
- Issue 和 Pull Request 的处理效率统计  
- 代码复杂度与模块热力图  
