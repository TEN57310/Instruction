# WRF 运行指南（4.1.1 版本）

## 1. 获取编译好的安装包

> 注：`$USER` 为个人用户名

WRF 压缩包路径：  
`/public/home/gengruomei/data3/WRF/4.1.1.tar.gz`

复制到个人路径下：  
```bash
cp /public/home/gengruomei/data3/WRF/4.1.1.tar.gz /public/home/$USER
```

解压缩：  
```bash
tar -xzvf 4.1.1.tar.gz
```
得到 `4.1.1` 版本 WRF：`/public/home/$USER/4.1.1`

---

## 2. 运行 geogrid

- 路径：`/public/home/$USER/4.1.1/WPS/geogrid.exe`
- 设置 WRF 模式区域：可通过网站 [WRF Domain Wizard](https://jiririchter.github.io/WRFDomainWizard/) 辅助设置，设置好嵌套层数和模式区域后获取一个 `namelist.input`。
- 按照 `namelist.input` 修改 `/public/home/$USER/4.1.1/WPS/namelist.wps`：

```fortran
&share
max_dom = 3,                       # 嵌套层数
start_date = '2025-03-02_03:00:00','2025-03-02_03:00:00','2025-03-02_03:00:00'   # 开始时间（嵌套层数决定参数数量）
end_date   = '2025-03-02_09:00:00','2025-03-02_09:00:00','2025-03-02_09:00:00'   # 结束时间
interval_seconds = 10800            # GFS驱动资料的步长（秒，组内资料一般为3小时）

&geogrid
# 根据之前获取的 namelist.input 修改相应参数
geog_data_path = '/public/data/geog'   # 组里地形数据路径
```

保存并退出。

运行 geogrid：  
```bash
./geogrid.exe
```

---

## 3. 获取驱动资料

在 `/public/home/$USER/4.1.1` 路径下新建文件夹作为资料存储路径：  
```bash
mkdir gfs
```

### 方式一：使用组内数据

GFS4 资料存储于 `/data1/premdev/datainput_arc/gfs4/`，内部资料为压缩包形式。将所需时间段的资料软链接至自己的 gfs 资料文件夹下并解压：

```bash
ln -s /data1/premdev/datainput_arc/gfs4/202503/gfs4.2025030200.tar .
tar -xvf gfs4.2025030212.tar   # 解压缩示例
```

### 方式二：从网络下载 GFS 数据

示例命令（下载指定时间范围的数据）：  
```bash
for time in {00..24..3}; do wget https://osdf-director.osg-htc.org/ncar/gdex/d084001/2023/20230724/gfs.0p25.2023072400.f0$time.grib2; done
```

进入 WPS 文件夹下，将解压好的 GFS 数据软链接过来：  
```bash
./link_grib.csh ../gfs/2025030200_fh.00*
```

---

## 4. 运行 ungrib

- 变量表路径：`/public/home/$USER/4.1.1/WPS/ungrib/Variable_Tables`
- 将 GFS 对应的变量表软链接至 WPS 文件夹下：

```bash
ln -s ungrib/Variable_Tables/Vtable.GFS Vtable
```

运行 ungrib：  
```bash
./ungrib.exe
```

---

## 5. 运行 metgrid

```bash
./metgrid.exe
```

---

## 6. 运行 real.exe

进入 WRF 运行目录：  
```bash
cd /public/home/$USER/4.1.1/WRF/run
```

将运行完的 metgrid 生成的文件软链接至此文件夹下：  
```bash
ln -s /public/home/$USER/4.1.1/WPS/met_em.d0* .
```

修改 `run` 文件夹下的 `namelist.input`，部分设置按照 WPS 的 `namelist.wps` 修改。示例内容如下：

```fortran
&time_control
run_days                            = 0,
run_hours                           = 6,
run_minutes                         = 0,
run_seconds                         = 0,
start_year                          = 2025, 2025, 2025,
start_month                         = 03,   03,   03,
start_day                           = 02,   02,   02,
start_hour                          = 03,   03,   03,
end_year                            = 2025, 2025, 2025,
end_month                           = 03,   03,   03,
end_day                             = 02,   02,   02,
end_hour                            = 09,   09,   09,
interval_seconds                    = 10800,      # GFS驱动资料的时间步长（秒）
input_from_file                     = .true.,.true.,.true.,
history_interval                    = 180,  60,   30,   # 输出文件的时间间隔（分钟）
frames_per_outfile                  = 1, 1, 1,         # 一个wrfout文件中包含的时刻数量
restart                             = .false.,
restart_interval                    = 7200,
io_form_history                     = 2,
io_form_restart                     = 2,
io_form_input                       = 2,
io_form_boundary                    = 2,
/

&domains
time_step                           = 90,               # 积分步长，推荐值是dx公里数的6倍
time_step_fract_num                 = 0,
time_step_fract_den                 = 1,
max_dom                             = 3,                # 嵌套层数
e_we                                = 182,  235,  286,
e_sn                                = 201,  205,  232,
e_vert                              = 33,    33,    33,
p_top_requested                     = 5000,
num_metgrid_levels                  = 34,               # metgrid层数，改为34
num_metgrid_soil_levels             = 4,
dx                                  = 12000, 4000,  1333.33,   # 按照WPS中的namelist修改
dy                                  = 12000, 4000,  1333.33,   # 按照WPS中的namelist修改
grid_id                             = 1,     2,     3,
parent_id                           = 1,     1,     2,
i_parent_start                      = 1,   54,   66,
j_parent_start                      = 1,   73,   58,
parent_grid_ratio                   = 1,     3,     3,
parent_time_step_ratio              = 1,     3,     3,
feedback                            = 1,
smooth_option                       = 0,
/
```

保存并退出。

---

## 7. 选择空闲的计算节点运行 WRF

### 前台直接运行

```bash
./wrf.exe
```

### 提交到后台运行

```bash
nohup mpirun -np <占用核数> ./wrf.exe >& log &
```

常用示例：  
```bash
nohup mpirun -np 32 ./wrf.exe >& log &
nohup mpirun -np 36 ./wrf.exe >& log &
```

查看 WRF 后台运行状态：  
```bash
tail -f rsl.error.0000
```

### 节点核数信息

| 节点    | 核数 |
|---------|------|
| 12-14   | 32   |
| 15-16   | 36   |
