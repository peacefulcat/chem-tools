# StoichKit ⚗️

> 化学计量工具箱 — 分子量计算 + 化学方程式配平

**第1-2周·热身项目** ｜ 每周化学+编程小项目系列

---

## 项目简介

一个用 Python 实现的命令行化学工具，功能覆盖本科化学课程中最常见的两个化学计量场景：

1. **分子量计算器** — 输入分子式，输出精确分子量
2. **化学方程式配平助手** — 输入反应物和生成物，输出配平系数

---

## 功能规划

### ✅ Week 1：分子量计算器

- [x] 内置元素周期表（原子序数 → 元素符号 → 原子量）
- [x] 支持带括号的分子式，如 `Fe2(SO4)3`
- [x] 支持水合物，如 `CuSO4·5H2O`
- [x] 支持同位素标记（可选扩展）
- [x] 结果精确到小数点后 4 位

**示例：**
```
$ python stoichkit.py mass H2SO4
分子量 H2SO4 = 98.0785 g/mol

$ python stoichkit.py mass Fe2(SO4)3
分子量 Fe2(SO4)3 = 399.8778 g/mol

$ python stoichkit.py mass CuSO4·5H2O
分子量 CuSO4·5H2O = 249.6850 g/mol
```

### ✅ Week 2：化学方程式配平助手

- [x] 输入反应物和生成物，自动配平
- [x] 基于线性代数（高斯消元法）求解系数
- [x] 支持非整数系数 → 归一化为最小整数比
- [x] 检测无法配平的反应
- [x] 检测产物中的状态符号（s, l, g, aq）并保留

**示例：**
```
$ python stoichkit.py balance "Fe + O2 → Fe2O3"
4 Fe + 3 O2 → 2 Fe2O3

$ python stoichkit.py balance "C2H6 + O2 → CO2 + H2O"
2 C2H6 + 7 O2 → 4 CO2 + 6 H2O

$ python stoichkit.py balance "KMnO4 + HCl → KCl + MnCl2 + Cl2 + H2O"
2 KMnO4 + 16 HCl → 2 KCl + 2 MnCl2 + 5 Cl2 + 8 H2O
```

---

## 项目结构

```
StoichKit/
├── README.md           # 本文件
├── stoichkit.py        # 主程序入口（CLI）
├── elements.py         # 元素周期表数据
├── parser.py           # 分子式解析器（支持括号嵌套）
├── mass_calc.py        # 分子量计算
├── balancer.py         # 方程配平（线性代数求解）
└── tests/              # 单元测试
    ├── test_parser.py
    ├── test_mass.py
    └── test_balancer.py
```

---

## 运行环境

- **语言：** Python 3.10+
- **依赖：** 标准库仅需 `sys`, `re`, `collections`, `itertools`，无需第三方包
- **运行方式：**
  ```bash
  # 分子量计算
  python stoichkit.py mass H2SO4

  # 方程式配平
  python stoichkit.py balance "Fe + O2 → Fe2O3"

  # 交互模式
  python stoichkit.py interactive
  ```

---

## 学习目标

| 编程技能 | 化学知识 |
|---------|---------|
| 字典与数据组织 | 元素周期表结构 |
| 递归解析（括号嵌套） | 分子式表示法 |
| 正则表达式 | 化学计量数 |
| 线性代数（高斯消元） | 物料守恒定律 |
| CLI 参数解析 | 氧化还原配平（进阶） |
| 单元测试 | 摩尔质量与物质的量 |

---

## 系列预告

| 周次 | 项目 | 技术栈 |
|------|------|--------|
| 1-2 | 🔬 **StoichKit** 化学计量工具箱 | Python 基础 |
| 3-4 | 🧪 虚拟滴定实验 | NumPy + Matplotlib |
| 5-6 | 📈 反应动力学模拟 | SciPy 微分方程 |
| 7-8 | 🧬 分子结构可视化 | RDKit / Matplotlib |
| 9-10 | 🔗 分子网络与 SMILES | 图论 + Python |
| 11-12 | 🔥 热化学计算器 | 面向对象 + 数据驱动 |

---

## 关于作者

南开大学 · 有机化学 × 软件工程 双学位 · 大一

*从化学理解世界，用代码构建工具。*
