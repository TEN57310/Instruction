# Python

## cfgrib 库调用命令

```python
import xarray as xr
xr.open_dataset(filename, engine = 'cfgrib')

```
## 读取变量值

示例：
```python
data = xr.open_dataset('/public/home/XiaAnRen/data3/vscode/python_3.11/misc/radar/data/wmc/中国近地面实况分析产品-UTC/气温/qiwen.csvZ_NAFP_C_BABJ_20250304011417_P_HRCLDAS_RT_BEJN_0P01_HOR-TAIR-2025030401.GRB2',engine='cfgrib')
data.variables['t2m'].values
```

## NetCDF库调用

```bash
nctest  #查看可调用 NetCDF 库的环境
export HDF5_USE_FILE_LOCKING=FALSE  #解决 NetCDF 库调用失败的问题
```

## history command 查看(Xshell)
```bash
<command snippet> + Ctrl + ↑ #查找命令片段
```

## *.tar.gz 压缩包压缩、解压命令
```bash
tar -xzvf *.tar.gz #解压缩
tar -czvf *.tar.gz #压缩
```

## *.tar 压缩包压缩、解压命令
```bash
tar -xvf *.tar #解压缩
```

## SWAN 雷达资料存储路径
```bash
/data3/XiaAnRen/SWAN
```

## 下载飞机观测数据
```bash
 export TOKEN="CEDA Access Tokens"
 #  CEDA Access Tokens 访问令牌由网址"https://services.ceda.ac.uk/account/token/#"生成
 nohup wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/faam/data/2013/b790-jul-28/non-core/man-cip-images/ --header "Authorization: Bearer $TOKEN" &
```

## 同化试验案例快速新建复制
```bash
cp -rd ../fusion_case_0.001/!(wrfout*|auxhist*) . #以 fusion_case 为例
```