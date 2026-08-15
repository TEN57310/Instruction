# 雷达数据处理

## data 类型：
```
Phased : 不可直接读取数据   Height:几十米   eg.TC站点     
Standard : 可直接读取数据   Height:几百米
```
## Scripts脚本概述

本目录包含用于**雷达数据处理与可视化**的 Python 脚本。各脚本功能具体如下：

### 数据处理

* `standardization.py` —— 对**单站雷达基础数据进行标准化预处理**
  将不可直接读取的Phased 转换成 可直接读取的Standard H*10

#### 1.按SWAN数据的分层方式

* `milab_cappi.py` —— 使用 **MeteoInfoLab** 计算**单站 CAPPI 数据**
* `mosaic.py` —— 通过**合并多个雷达站数据生成雷达拼图（mosaic）**
* `run.py` —— **主处理流程脚本**，按顺序调用标准化、CAPPI 计算以及拼图处理脚本`standardization.py`、`milab_cappi.py`、`mosaic.py`

#### 2.按XPAR数据的分层方式(100m)

* `milab_cappi_section.py` —— 使用 **MeteoInfoLab** 计算**单站 CAPPI 数据**
* `mosaic_section.py` —— 通过**合并多个雷达站数据生成雷达拼图（mosaic）**
* `section_plot.py` 模式为`Mosaic`时—— **主处理流程脚本**，按顺序调用标准化、CAPPI 计算以及拼图处理脚本
  
* `fusion.py` —— 将**雷达拼图数据与 SWAN 数据进行融合**

### 雷达可视化

* `product.py` —— **单站雷达基础数据可视化**
  路径：`figures/variables`
* `swan.py` —— **对比雷达拼图数据与 SWAN 数据**
  路径：`figures/swan_mosaic`
* `comparison.py` —— **融合雷达数据产品的可视化**
  路径：`figures/fusion`

### WRF 实验可视化

* `domain_distribution.py` —— **WRF 实验区域（domain）配置的可视化**
* `wrf_case.py` —— **WRF 实验结果可视化**
* `sequence.py` —— **WRF 实验指标的时间序列绘图**

### 工具与配置

* `build.sh` —— **用于构建包含雷达数据的数据目录的构建脚本**
* `structure.py` —— **存储并处理雷达结构数据**
* `viztools.py` —— **可视化工具及辅助函数**
* `viztools.yaml` —— **可视化工具的配置文件**
* `metrics.py` —— **用于计算评价指标（如 FSS）的类**

---

## 目录结构

* `ncfile/` —— 存放**输入和输出的雷达数据文件**
* `figures/` —— 存放**生成的可视化图像和绘图结果**

---

## 数据处理流程

标准的数据处理流程如下：

1. 对单站雷达基础数据进行标准化处理（`standardization.py`）
2. 计算单站 **CAPPI** 数据（`milab_cappi.py`）
3. 使用多站雷达数据生成 **雷达拼图（mosaic）**（`mosaic.py`）
4. 将雷达拼图与 **SWAN 数据进行融合**（`fusion.py`）

可以通过以下命令按顺序执行整个流程：

```bash
python run.py
python fusion.py
```

---

## 可视化

* **雷达数据可视化脚本**：
  `product.py`、`swan.py`、`comparison.py`

* **WRF 实验可视化脚本**：
  `domain_distribution.py`、`wrf_case.py`、`sequence.py`

---

