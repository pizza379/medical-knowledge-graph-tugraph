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
 [数据导入过程如图所示](screenshots/数据导入成功.png)

（3）数据导入验证：
输入cypher查询语言，查询数据是否导入成功。
```cypher
match(n) return n
```
 [数据导入验证成功](screenshots/数据导入成功验证.png)

## 三、在TuGraph中使用cypher语句+Python交互
### 1.文字描述
基于 TuGraph 的medical数据库（医疗知识图谱），通过 Python 的neo4j库连接 TuGraph，执行 Cypher 语句实现疾病 - 症状 - 药物的核心查询，完成 Python 与 TuGraph 的交互，支撑后续对话系统开发。
核心逻辑：
连接 TuGraph 的medical数据库（医疗知识图谱）；
封装 Cypher 查询函数（疾病查症状、症状查疾病、疾病查药物）；
执行 Cypher 语句并返回结构化结果。

### 2.核心代码
#### （1）链接TuGraph数据库
输入实际的TuGraph配置，初始化连接类，通过 Bolt 协议（7687 端口）连接 TuGraph 的medical数据库，并验证连接。
```python
from neo4j import GraphDatabase, basic_auth
TUGRAPH_CONFIG = {
    "uri": "bolt://localhost:7687",  
    "username": "admin",            
    "password": "73@TuGraph",      
    "database": "default"           
}
class TuGraphMedicalQuery:
    def __init__(self):
        """初始化TuGraph连接"""
        # 建立Bolt连接（TuGraph兼容Neo4j协议，禁用加密）
        self.driver = GraphDatabase.driver(
            TUGRAPH_CONFIG["uri"],
            auth=basic_auth(TUGRAPH_CONFIG["username"], TUGRAPH_CONFIG["password"]),
            encrypted=False  # 必须禁用，TuGraph默认不开启TLS
        )
        # 验证连接
        try:
            self.driver.verify_connectivity()
            print("成功连接TuGraph的medical数据库！")
        except Exception as e:
            raise RuntimeError(f"连接失败：{e}")

    def close(self):
        """关闭连接"""
        self.driver.close()
        print("已关闭TuGraph连接")
```
#### (2)封装 Cypher 查询函数
封装 Cypher 语句实现多维度医疗知识查询,例如疾病查症状、症状查疾病、疾病查药物
```python
    def get_disease_drugs(self, disease_name):
        """
        Cypher查询：根据疾病名查治疗药物
        :param disease_name: 疾病名称（如"糖尿病"）
        :return: 药物列表/提示信息
        """
        cypher = """
        MATCH (d:Disease {name: $disease})-[r:HAS_Drug]->(dr:Drug)
        RETURN collect(dr.name) AS drugs
        """
        with self.driver.session(database=TUGRAPH_CONFIG["database"]) as session:
            result = session.run(cypher, disease=disease_name)
            record = result.single()
        
        if record and record["drugs"]:
            return f"疾病【{disease_name}】的治疗药物：{', '.join(record['drugs'])}"
        else:
            return f"未查询到【{disease_name}】的治疗药物"

```
#### (3)执行 Cypher 语句并返回结构化结果。
设计菜单式交互界面，支持用户选择查询类型、输入关键词，返回人性化查询结果。以下为示例代码。
```python
if __name__ == "__main__":
    # 初始化查询类
    query = TuGraphMedicalQuery()
  
    print("\n=== 测试查询：疾病查药物 ===")
    print(query.get_disease_drugs("麦粒肿"))  # 替换为你的疾病名

```
### 3.输出结果
根据示例查询代码，最终在命令窗口得出的输出成果如图所示。
[输出结果](screenshots/输出结果1.png)


## 四、对话系统的输入输出、用户交互
### 1.文字描述
编写了相应的用户交互脚本，核心模块如下：
1.TuGraph 连接模块：通过 neo4j 库建立 Bolt 连接，验证连通性；
2.疾病库加载模块：从 TuGraph 读取所有疾病名称，用于意图识别；
3.意图识别模块：匹配用户输入中的疾病名称和查询意图（基于关键词映射表）；
4.Cypher 查询模块：根据意图动态生成兼容 TuGraph 的 Cypher 语句，执行查询并返回结果；
5.交互模块：实现自然语言对话循环，处理用户输入 / 退出指令。
### 2.核心代码
脚本medical_kg_nlu_dialog.py中的核心代码块如下
#### （1）意图映射表示例代码
```python
QUERY_MAP = {
    "alias": {
        "relation": "HAS_ALIAS",
        "label": "Alias",
        "keywords": ["别名", "又叫", "学名"],
        "reply": "常见别名包括："
    },
    "part": {
        "relation": "IS_OF_PART",
        "label": "Part",
        "keywords": ["部位", "哪里", "哪个部位"],
        "reply": "相关的发病部位是："
    }}
```
#### (2)意图识别方法
```python
def recognize_intent(self, user_input):
        """意图识别：提取查询意图+目标疾病"""
        # 步骤1：提取目标疾病
        disease_name = None
        for d in self.disease_list:
            if d in user_input:
                disease_name = d
                break
        if not disease_name:
            return None, None
        
        # 步骤2：识别查询意图
        intent_key = None
        for key, config in QUERY_MAP.items():
            for keyword in config["keywords"]:
                if keyword in user_input:
                    intent_key = key
                    break
            if intent_key:
                break
        return intent_key, disease_name

```
#### (3)执行查询方法
```python
    def execute_query(self, intent_key, disease_name):
        """执行Cypher查询（TuGraph兼容语法）"""
        if not intent_key or not disease_name:
            return "❓ 未识别到查询意图或疾病名称（示例：颈椎病该挂什么科？）"
        
        # 获取意图配置
        config = QUERY_MAP[intent_key]
        relation = config["relation"]
        label = config["label"]
        reply_prefix = config["reply"]

        # 修复：标准Cypher WHERE子句（TuGraph兼容）
        cypher = f"""
        MATCH (d:Disease)-[r:{relation}]->(n:{label})
        WHERE d.name = $disease
        RETURN collect(n.name) AS results
        """
        with self.driver.session(database=TUGRAPH_CONFIG["database"]) as session:
            result = session.run(cypher, disease=disease_name)
            record = result.single()
        
        # 处理结果
        if record and record["results"] and len(record["results"]) > 0:
            return f"\n📌 {reply_prefix}\n{', '.join(record['results'])}\n"
        else:
            return f"\n❓ 未查询到【{disease_name}】的{config['keywords'][0]}相关信息\n"
```
### 3.运行结果
在命令行中输入
```bash
python medical_kg_nlu_dialog.py
```
对话系统的交互成果如下图所示：
[交互结果](screenshots/对话系统截图.png)
