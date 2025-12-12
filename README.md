# 基于TuGraph的医疗知识图谱对话系统
专业综合实践课程的作业二-cufe
## 林雨珊 2022310943
## 作业要求
1. TuGraph-安装、启动，文字描述+运行成功截图-6分
2. TuGraph-数据导入（图谱构建），文字描述+核心代码，运行成功截图-6分
3. 在TuGraph中使用cypher语句+Python交互，文字描述+核心代码-6分
4. 对话系统的输入输出、用户交互，运行成功截图-6分
5. 提交csdn/github网页链接或将网页输出成pdf提交-6分

## 一、TuGraph-安装、启动
### 1.文字描述
本次实验在304机房完成，采用 Docker 方式部署 TuGraph，核心步骤如下：
确保本地已安装 Docker 并启动服务；
执行 Docker 运行命令，挂载本地 D:\wangmaoning 目录到容器 /mnt，映射 7070（Web 控制台）和 7687（Cypher 交互）端口，使用官方 tugraph-runtime-ubuntu18.04 镜像启动 lgraph_server；
启动成功后，通过浏览器访问 http://localhost:7070 进入 TuGraph Web 控制台，默认账号 admin，密码 73@TuGraph。
注：为方便复制命令行，直接copy了老师的文件夹命名，本次作业我的文件夹同命名为wangmaoning
### 2.运行过程
#### （1）启动Docker Desktop
双击桌面上Docker Desktop图标（蓝底白色鲸鱼），启动后跳过注册和升级界面，至出现如下界面，正常启动并联网成功时，界面左下角绿色字显示“Engine running”
#### （2）输入命令行
在D盘新建文件夹，例如新建名为wangmaoning的文件夹，用于后续文件存放和docker容器共享路径
在windows命令提示符界面输入：docker run -d -v D:\wangmaoning:/mnt -p 7070:7070 -p 7687:7687 docker.1ms.run/tugraph/tugraph-runtime-ubuntu18.04 lgraph_server ，启动成功后会显示一串字符，如下图所示：
！[命令行截图](screenshots/TuGraph启动命令.png)
#### （3）在浏览器中启动TuGraph
打开浏览器，地址栏输入localhost:7070可以进入TuGraph平台登录界面，用默认账号admin，密码73@TuGraph可以登录，成功登录后如图所示
！[TuGraph成功启动截图](screenshots/TuGraph成功启动.png)

## 二、TuGraph-数据导入（图谱构建）
### 1.思路文字描述
数据导入是构建医疗知识图谱的核心环节，主要分为以下三部分：
#### （1）准备数据文件：基于老师提供的 disease3.csv数据集，通过 write_V_E_files.py 生成节点（Vertex）和边（Edge）的 CSV 文件；
#### （2）定义图谱模式：通过 write_conf.py 生成 TuGraph 所需的元数据配置文件example.json，声明节点 / 边的标签、属性和约束，即模型模版
#### （3）导入 TuGraph：通过 TuGraph 的可视化界面，将模型配置文件和数据文件导入数据库，完成图谱构建。

### 2.实验过程
#### 1.安装依赖包
```bash
pip install pandas neo4j
```
！[依赖包安装完成截图](screenshots/安装依赖包.png)

#### 2.数据预处理
将原始 CSV 拆分为 TuGraph 可识别的「节点文件」和「边文件」，成功运行后，在当前目录下会新增27个代码文件（1 个疾病节点文件 + 13 个关联实体节点文件 + 13 个边文件）
```bash
# 进入实际路径
cd desktop\medical-knowledge-graph-tugraph\code
# 运行预处理脚本
python write_V_E_files.py
```
！[数据预处理运行截图](screenshots/运行数据预处理脚本.png)

#### 3.生成 TuGraph 元数据配置文件（schema）
本实验使用write_conf.py脚本，在当前目录生成example.json文件，定义图谱的元数据（节点 / 边的标签、属性类型、主键、关联约束）
```bash
#运行配置文件生成脚本，生成 JSON 格式的配置文件
python write_conf.py
```
example.json文件格式示例如下
```json
 {
    "label": "Disease",
    "type": "VERTEX",
    "properties": [
      {
        "name": "name",
        "type": "STRING",
        "optional": false,
        "unique": true,
        "index": true
      }
    ],
    "primary": "name"
  }
```
#### 4.在TuGraph可视化界面导入数据
 
（1）模型导入：
 在TuGraph 可视化建模界面中，选中左侧导航栏中的“建模”，在顶端选择“导入模型”，选择刚刚通过脚本生成的example.json文件，系统节课直接创建对应的标签结构，无需手动单个创建标签与关系。
 [导入后的模型如图所示](screenshots/模型导入成功.png)
（2）数据导入：
在左侧导航栏中选择“导入”，点击选择文件选择刚刚通过write_V_E_files.py脚本生成的所有点和边的csv数据文件，选择相应标签后进行映射，映射成功后点击导入。
 [导入后的模型如图所示](screenshots/数据导入成功.png)
（3）数据导入验证：
输入cypher查询语言，查询数据是否导入成功。
```cypher
match(n) return n
```
 [导入后的模型如图所示](screenshots/数据导入成功验证.png)

 