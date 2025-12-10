# medical-knowledge-graph-tugraph
专业综合实践课程的作业二-cufe
## 林雨珊 2022310943
## 作业要求
1. TuGraph-安装、启动，文字描述+运行成功截图-6分
2. TuGraph-数据导入（图谱构建），文字描述+核心代码，运行成功截图-6分
3. 在TuGraph中使用cypher语句+Python交互，文字描述+核心代码-6分
4. 对话系统的输入输出、用户交互，运行成功截图-6分
5. 提交csdn/github网页链接或将网页输出成pdf提交-6分

## 一、TuGraph-安装、启动
### 1.启动Docker Desktop
双击桌面上Docker Desktop图标（蓝底白色鲸鱼），启动后跳过注册和升级界面，至出现如下界面，正常启动并联网成功时，界面左下角绿色字显示“Engine running”
### 2.输入命令行
在D盘新建文件夹，例如新建名为wangmaoning的文件夹，用于后续文件存放和docker容器共享路径
在windows命令提示符界面输入：docker run -d -v D:\wangmaoning:/mnt -p 7070:7070 -p 7687:7687 docker.1ms.run/tugraph/tugraph-runtime-ubuntu18.04 lgraph_server ，启动成功后会显示一串字符，如下图所示：
！[命令行截图](screenshots/TuGraph启动命令.png)
### 3.在浏览器中启动TuGraph
打开浏览器，地址栏输入localhost:7070可以进入TuGraph平台登录界面，用默认账号admin，密码73@TuGraph可以登录，成功登录后如图所示
！[TuGraph成功启动截图](screenshots/TuGraph成功启动.png)

## 二、TuGraph-数据导入（图谱构建）
### 1.安装依赖包
```bash
pip install pandas neo4j
```
！[依赖包安装完成截图](screenshots/安装依赖包.png)

### 2.数据预处理
将原始 CSV 拆分为 TuGraph 可识别的「节点文件」和「边文件」，成功运行后，在当前目录下会新增27个代码文件（1 个疾病节点文件 + 13 个关联实体节点文件 + 13 个边文件）
```bash
# 进入实际路径
cd desktop\medical-knowledge-graph-tugraph\code
# 运行预处理脚本
python write_V_E_files.py
```
！[数据预处理运行截图](screenshots/运行数据预处理脚本.png)

### 3.生成 TuGraph 元数据配置文件（schema）
告诉 TuGraph 节点 / 边的结构（如节点类型、属性、主键、边的起止节点约束），否则导入时 TuGraph 无法识别数据。
```bash
#运行配置文件生成脚本，生成 JSON 格式的配置文件
python write_conf.py
```
