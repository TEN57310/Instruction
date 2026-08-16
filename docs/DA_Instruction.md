# 资料同化步骤

## 同化X / Fusion步骤：

### 1. 准备输入资料

```bash
cd /public/home/gengruomei/data3/datest/data

mkdir cma_decoded   # 创建中国气象局地面观测资料文件夹，目前为空
mkdir gfs4          # 创建gfs资料文件夹
cd gfs4
```

gfs4完整资料存储于 ```/data1/premdev/datainput_arc/gfs4/```
内部资料为压缩包形式
将所需要时间段的资料软链接至自己的gfs资料文件夹下并解压

```bash
ln -s /data1/premdev/datainput_arc/gfs4/202503/gfs4.2025030212.tar
tar -xvf gfs4.2025030212.tar #解压缩
mkdir special      # 创建地面站/风廓线资料文件夹，目前为空
```
若要同化地面站/风廓线资料，将处理好的试验所需时间段的地面站/风廓线*.decode文件直接全部软链接至该文件夹下。

### 2. 运行WRF-FDDA 程序（准备背景场）

```bash
# 创建公用临时目录(首次需创建)
mkdir -p /public/home/gengruomei/data3/datest/cycles/share

# 准备模式运行程序的相关代码(首次需要准备)
cp -rd /public/home/gengruomei/data3/datest/fddahome

# 创建新的工作目录
cd /public/home/gengruomei/data3/datest/GMODJOBS
# 也可通过复制之前的工作目录并修改相应参数设置
cp -rd THOMPSON $GMODJOBS   # $GMODJOBS为新工作目录名
cd $GMODJOBS

# 初始场相关参数设置
flexinput.pl
$DATADIR="/public/home/gengruomei/data3/datest/data"

# 运行程序计算节点选择
member-nodes

# 参数设置
rtfddaflex.pl
# $HOMEDIR = "/data3/$MYLOGIN/datest"

# 运行程序
start_rtfddaflex_gmod.pl
```

#### 修改微物理参数化方案：

```bash
/data3/gengruomei/datest/GMODJOBS/$GMODJOBS/namelists/WRF.nl.template.WCTRL   # 修改&physics部分
/data3/gengruomei/datest/GMODJOBS/$GMODJOBS/namelists/README.namelist        # namelist说明文档
```

<details>
<summary>参数化方案</summary>

```
 &physics

 Note: even the physics options can be different in different nest domains, 
       caution must be used as what options are sensible to use

 chem_opt                            = 0,       ; chemistry option - use WRF-Chem
 mp_physics (max_dom)                microphysics option
                                     = 0, no microphysics
                                     = 1, Kessler scheme
                                     = 2, Lin et al. scheme
                                     = 3, WSM 3-class simple ice scheme
                                     = 4, WSM 5-class scheme
                                     = 5, Ferrier (new Eta) microphysics, operational High-Resolution Window version
                                     = 6, WSM 6-class graupel scheme
                                     = 7, Goddard GCE scheme (also uses gsfcgce_hail, gsfcgce_2ice)
                                     = 8, Thompson scheme (new for V3.1)
                                     = 9, Milbrandt-Yau 2-moment scheme (new for V3.2)
                                     = 10, Morrison (2 moments)
                                     = 11, CAM 5.1 microphysics
                                     = 13, SBU_YLIN scheme
                                     = 14, WDM 5-class scheme
                                     = 16, WDM 6-class scheme
                                     = 17, NSSL 2-moment 4-ice scheme (steady background CCN)
                                     = 18, NSSL 2-moment 4-ice scheme with predicted CCN (better for idealized than real cases)
                                       ; to set a global CCN value, use
                                       nssl_cccn  = 0.7e9   ; CCN for NSSL scheme (18). Also sets same value to ccn_conc for mp_physics=18
                                     = 19, NSSL 1-moment (7 class: qv,qc,qr,qi,qs,qg,qh; predicts graupel density)
                                     = 21, NSSL 1-moment, (6-class), very similar to Gilmore et al. 2004
                                           Can set intercepts and particle densities in physics namelist, e.g., nssl_cnor
                                       For NSSL 1-moment schemes, intercept and particle densities can be set for snow, 
                                       graupel, hail, and rain. For the 1- and 2-moment schemes, the shape parameters 
                                       for graupel and hail can be set.
                                       nssl_alphah  = 0.    ! shape parameter for graupel
                                       nssl_alphahl = 2.    ! shape parameter for hail
                                       nssl_cnoh    = 4.e5  ! graupel intercept
                                       nssl_cnohl   = 4.e4  ! hail intercept
                                       nssl_cnor    = 8.e5  ! rain intercept
                                       nssl_cnos    = 3.e6  ! snow intercept
                                       nssl_rho_qh  = 500.  ! graupel density
                                       nssl_rho_qhl = 900.  ! hail density
                                       nssl_rho_qs  = 100.  ! snow density
                                     = 28, aerosol-aware Thompson scheme with water- and ice-friendly aerosol climatology 
                                           (new for V3.6)
                                       This option has two climatogical aerosol input options:
                                       use_aero_icbc = .F. : use constant values
                                       use_aero_icbc = .T. : use input from WPS
                                     = 30, HUJI (Hebrew University of Jerusalem, Israel) spectral bin microphysics,
                                           fast version
                                     = 32, HUJI spectral bin microphysics, full version
                                     = 95, Ferrier (old Eta) microphysics, operational NAM (WRF NMM) version
```

</details>


|物理过程|方案|
|:---:|:---:|
|微物理|Thompson|
|长短波辐射|RRTMG|
|边界层|YSU|
|近地层|Revised MM5 Monin-Obukhov|
|陆面过程|Noah-MP land-surface|
|积云对流|Grell-Freitas ensemble(仅D01使用)|


|physics|parameter|
|:---:|:---:|
|!physics_suite|'CONUS'|
|mp_physics|8,8,8,8,|
|cu_physics|3,0,0,0,|
|ra_lw_physics|4,4,4,4,|
|ra_sw_physics|4,4,4,4,|
|bl_pbl_physics|1,1,1,1,|
|sf_sfclay_physics|1,1,1,1,|
|sf_surface_physics|2,2,2,2,|


```bash
./start_rtfddaflex_gmod.pl $GMODJOBS 2024101709   
# 运行，$GMODJOBS与工作目录名一致
# 背景场开始预报的时间：2024101709/2025030203
# (PS. 开始预报时间最好为3的倍数)
```

### 3. 准备XPAR资料

运行`run.py` 调整date和起始、终止时间;  
运行`fusion.py`调整date和起始、终止时间以及domain和mode;  
输出目录为`/public/home/gengruomei/scripts/grm_scripts/ncfile/fusion/$mode`
`*_radar_process` 分别为同化不同雷达资料的工作目录

将 fusion.py 生成的文件软链接至 `/public/home/gengruomei/data3/datest/*_radar_process/outdata/$GMODJOBS/cappi_mask_out`

```bash

cd /public/home/gengruomei/data3/datest/*_radar_process
./combine_*_process.sh $GMODJOBS 2 2024101709   # 处理X和Fusion只需要step3
./combine_*_process.sh $GMODJOBS 3 2024101709

cd ~/data3/datest/*_radar_process/outdata/$GMODJOBS/cappi_wrf_vertical_h
ncrcat wrffdda_d02_* wrffdda_d02
ncrcat wrffdda_d03_* wrffdda_d03
```

### 4. 运行WRF-FDDA 程序（进行同化试验）

#### 准备同化试验工作目录

```bash
cd /data3/gengruomei/datest/cycles/$GMODJOBS/GFS_WCTRL/2024101709/WRF_P/
rm rsl.*
mkdir restrts
```

#### 修改输入的namelist

```bash
vi namelist.input
```

- 根据同化的时间修改 `&time_control` 部分；
- 关闭 `&time_control` 中的重启动功能：`restart = .false.,`
- 根据计算节点的空闲核数修改 `&domains` 中的核数分配方式：  
  `nproc_x * nproc_y = 计算节点的占用核数`  
  `nproc_x = 4,`  
  `nproc_y = 4,`
- 关闭 `&physics` 中的用于控制地形对近地面风场影响的修正方案：  
  `topo_wind = 0,0,0,0,0,0,0,`
- 根据同化的区域domain修改 `&fdda` 部分：  
  `grid_fdda = 0, 1, 1, 0,`
- 修改 `&fdda` 中的 `gfdda_end_h` 部分：  
  `gfdda_end_h = 24, 3, 3, 24,`
- 修改 `&fdda` 中用于控制开始同化qr层数的 `k_zfac_qr` 部分：
  `if_zfac_qr               = 0,     1,     1,    0,`
  `k_zfac_qr                = 10,    1,     1,    8,`

#### 修改同化试验的初始场

```bash
rm wrfinput_d0*
ln -s ../wrfout_d0*_2024-10-17_09:00:00.GFS_WCTRL_P+FCST wrfinput_d0*
cp -rd WRF_P *_case
cd *_case
```

#### 同化试验案例快速新建复制
```bash
cp -rd ../fusion_case_0.001/!(wrfout*|auxhist*) . #以 fusion_case 为例
```

#### 将拼接后的wrffdda文件软链接至namelist同级目录

```bash
ln -s /public/home/gengruomei/data3/datest/*_radar_process/outdata/$GMODJOBS/cappi_wrf_vertical_h/wrffdda_d02
ln -s /public/home/gengruomei/data3/datest/*_radar_process/outdata/$GMODJOBS/cappi_wrf_vertical_h/wrffdda_d03
```

#### 选择空闲的计算节点运行WRF

```bash
ssh node*   # 去计算节点运行WRF
cd /data3/gengruomei/datest/cycles/$GMODJOBS/GFS_WCTRL/2024101709/x_case
```

| 节点   | 12-14 | 15-16 |
|:---:|:---:|:---:|
| 核数   | 32    | 36    |

后台运行WRF-FDDA命令：

```bash
nohup mpirun -np <占用核数> ./wrf.mpich >& log &
# 例如：
nohup mpirun -np 32 ./wrf.mpich >& log &
nohup mpirun -np 36 ./wrf.mpich >& log &
```
若使用自编译的WRF程序运行WRF-FDDA命令：

```bash
# 先将编译好的 wrf.exe 复制到文件夹下
cp /public/home/gengruomei/data3/datest/program/HZY_HLHN/main/wrf.exe /data3/gengruomei/datest/cycles/$GMODJOBS/GFS_WCTRL/2024101709/x_case/
nohup mpirun -np 32 ./wrf.exe &> /dev/null &
nohup mpirun -np 36 ./wrf.exe &> /dev/null &
```

查看WRF运行状态命令：

```bash
tail -f restrts/rsl.error.0000
```

#### 多节点运行WRF

创建节点选用脚本：

```bash
for node in 13 14; do echo "node$node:32"; done > hosts  #覆盖
for node in 15 16; do echo "node$node:36"; done >> hosts #追加
```

根据计算节点的选用情况修改namelist.input脚本 `&domains` 中的核数分配方式：  
`nproc_x * nproc_y = 计算节点的占用核数 (node_i + node_j)`  
`nproc_x = 8,`  
`nproc_y = 8,`

后台运行WRF-FDDA命令：

```bash
nohup mpirun -machinefile hosts ./wrf.mpich >& log &
```

查看WRF运行状态命令：

```bash
tail -f restrts/rsl.error.0000
```

---

## FDDA同化模块修改

### (1) 可以复制FDDA同化程序所在文件夹并修改

文件夹地址：

```bash
/public/home/gengruomei/data3/datest/program/assimilation/ORIGIN #原版
```
```bash
/public/home/gengruomei/data3/datest/program/assimilation/QVAPOR #此文件夹下的 nc_utils.F90 文件比原版输出的 nc 文件要多一个水汽变量
```

1. 修改 `radar_to_wrffdda.F90` 文件
2. 修改完进行编译，在 `radar_to_wrffdda.F90` 文件所在的文件夹下输入 `make` 来编译
   
### (2) 修改并编译完成后重新生成 wrffdda 文件
！！！注意要修改 wrffdda 生成脚本里的 exe 调用路径

```bash
cd /public/home/gengruomei/data3/datest/SWAN_radar_process/RDA_wrffdda/new_run_wrffdda_c.sh

exe=/public/home/premopr/data/SWAN_radar_process/RDA_wrffdda/RADAR_TO_WRFFDDA_netcdf4_qx_mask/radar_to_wrffdda.exe #原版 FDDA 程序路径 line 90
```

```bash
cd /public/home/gengruomei/data3/datest/X_radar_process/RDA_wrffdda/new_run_wrffdda_c.sh

exe=/public/home/premopr/data/SWAN_radar_process/RDA_wrffdda/RADAR_TO_WRFFDDA_netcdf4_qx_mask/radar_to_wrffdda.exe #原版 FDDA 程序路径 line 96
```

```bash
cd /public/home/gengruomei/data3/datest/Fusion_radar_process/RDA_wrffdda/new_run_wrffdda_c.sh

exe=/public/home/premopr/data/SWAN_radar_process/RDA_wrffdda/RADAR_TO_WRFFDDA_netcdf4_qx_mask/radar_to_wrffdda.exe #原版 FDDA 程序路径 line 96
```

---

## FDDA 源代码修改

FDDA 源代码压缩包路径：

```bash
/public/home/gengruomei/data3/datest/program/HLHN.tar
```
解压缩并重命名获得 HZY_HLHN文件夹

### (1) 修改 FDDA 源代码，路径：

```bash
/public/home/gengruomei/data3/datest/program/HZY_HLHN/phys/module_fdda_psufddagd.F
```
### (2) 修改完成后进行编译
1. 在 GPU 节点位于 HZY_HLHN文件夹路径下使用`./compile em_real` 命令编译

```bash
#若要保留输出，则使用：
./compile em_real | tee log
#若要重新进行完整干净编译，则使用：
./clean -a
mv configure.wrf.backup configure.wrf
./compile em_real
```
2. 生成 exe 可执行文件，路径：
```bash
/public/home/gengruomei/data3/datest/program/HZY_HLHN/main/wrf.exe
```
1. 将 exe 可执行文件复制到 *_case 文件夹下
---

## 同化SWAN步骤：

### (1) 生成逐小时的wrffdda文件

脚本地址：

```bash
cd /public/home/gengruomei/data3/datest/SWAN_radar_process/
```

运行前准备 `indata` 工作目录（`GMODJOBS` 为自己创建的工作目录名）：

1. `indata/SWANdata`：软链接SWAN雷达数据到此位置，数据存储位置为 `/data1/premdev/datainput_arc/radar/raw/`
2. `/indata/geofile/GMODJOBS`

运行命令：

```bash
# domain为具体的同化区域，date为同化起始时间
./combine_swan_process.sh GMODJOBS domain date   # step1~3需逐步运行
```

输出地址：

```
/outdata/GMODJOBS/cappi_wrf_vertical_h
```

### (2) 拼接逐小时的wrffdda文件

运行命令：

```bash
ncrcat wrffdda_d02_* wrffdda_d02
ncrcat wrffdda_d03_* wrffdda_d03
```

### (3) 准备同化试验工作目录

```bash
/public/home/gengruomei/data3/datest/cycles/GMODJOBS/GFS_WCTRL/2024101709/swan_case
```

### (4) 修改输入的namelist

```bash
vi namelist.input
```

- 根据同化的区域domain修改namelist中的 `&fdda` 部分：  
  `grid_fdda = 0, 1, 0, 0,`
- 根据计算节点的空闲核数修改 `&domains` 中的核数分配方式：  
  `nproc_x * nproc_y = 计算节点的占用核数`  
  `nproc_x = 4,`  
  `nproc_y = 4,`

### (5) 将拼接后的wrffdda文件软链接至namelist同级目录

```bash
ln -s /public/home/gengruomei/data3/datest/SWAN_radar_process/outdata/GESDHYD/cappi_wrf_vertical_h/wrffdda_d02 wrffdda_d02
```

### (6) 选择空闲的计算节点运行WRF

| 节点   | 12-14 | 15-16 |
|:---:|:---:|:---:|
| 核数   | 32    | 36    |

后台运行WRF-FDDA命令：

```bash
nohup mpirun -np <占用核数> ./wrf.mpich >& log &
```

查看WRF运行状态命令：

```bash
tail -f restrts/rsl.error.0000
```
