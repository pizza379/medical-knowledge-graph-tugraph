# coding=utf-8
"""
医疗知识图谱自然语言对话系统（修复Cypher语法版）
"""
from neo4j import GraphDatabase, basic_auth
import re
import sys

# ===================== 1. 配置项 =====================
TUGRAPH_CONFIG = {
    "uri": "bolt://localhost:7687",       # TuGraph Bolt端口
    "username": "admin",                  # 默认用户名
    "password": "73@TuGraph",             # 默认密码
    "database": "default"            # 替换为你的真实数据库名
}

# ===================== 2. 意图映射表 =====================
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
    },
    "age": {
        "relation": "IS_OF_AGE",
        "label": "Age",
        "keywords": ["人群", "年龄", "易感"],
        "reply": "常见易感人群包括："
    },
    "infection": {
        "relation": "IS_INFECTIOUS",
        "label": "Infection",
        "keywords": ["传染", "感染"],
        "reply": "该疾病的传染性情况是："
    },
    "insurance": {
        "relation": "In_Insurance",
        "label": "Insurance",
        "keywords": ["医保", "报销"],
        "reply": "医保相关信息："
    },
    "department": {
        "relation": "IS_OF_Department",
        "label": "Department",
        "keywords": ["科室", "挂什么科"],
        "reply": "应就诊的科室包括："
    },
    "checklist": {
        "relation": "HAS_Checklist",
        "label": "Checklist",
        "keywords": ["检查", "检测", "做什么检查"],
        "reply": "通常推荐的检查项目包括："
    },
    "symptom": {
        "relation": "HAS_SYMPTOM",
        "label": "Symptom",
        "keywords": ["症状", "表现"],
        "reply": "可能出现的症状包括："
    },
    "complication": {
        "relation": "HAS_Complication",
        "label": "Complication",
        "keywords": ["并发症", "合并症"],
        "reply": "可能出现的并发症包括："
    },
    "treatment": {
        "relation": "HAS_Treatment",
        "label": "Treatment",
        "keywords": ["治疗", "方式", "怎么治"],
        "reply": "常用治疗方式包括："
    },
    "drug": {
        "relation": "HAS_Drug",
        "label": "Drug",
        "keywords": ["药", "药物", "用药"],
        "reply": "常用药物包括："
    },
    "period": {
        "relation": "Cure_Period",
        "label": "Period",
        "keywords": ["周期", "多久能好"],
        "reply": "治疗周期一般为："
    },
    "rate": {
        "relation": "Cure_Rate",
        "label": "Rate",
        "keywords": ["治愈率", "成功率"],
        "reply": "治愈率相关信息："
    },
    "money": {
        "relation": "NEED_Money",
        "label": "Money",
        "keywords": ["费用", "多少钱", "花费"],
        "reply": "治疗费用大约为："
    }
}

# ===================== 3. 疾病名称提取 =====================
def get_all_diseases(driver, database):
    """获取数据库中所有疾病名称（TuGraph兼容语法）"""
    cypher = "MATCH (d:Disease) RETURN d.name AS name"
    with driver.session(database=database) as session:
        result = session.run(cypher)
        diseases = [record["name"] for record in result if record["name"]]
    return diseases

# ===================== 4. 自然语言意图识别核心类 =====================
class MedicalNLUDialog:
    def __init__(self):
        """初始化连接+加载疾病库+意图映射"""
        # 1. 连接TuGraph
        try:
            self.driver = GraphDatabase.driver(
                TUGRAPH_CONFIG["uri"],
                auth=basic_auth(TUGRAPH_CONFIG["username"], TUGRAPH_CONFIG["password"]),
                encrypted=False
            )
            self.driver.verify_connectivity()
            self.clear_screen()
            print("="*60)
            print("🎯 医疗知识图谱自然语言对话系统")
            print("="*60)
            print("✅ 已连接TuGraph数据库！")
            print("💡 支持查询：疾病的症状/科室/药物/治愈率等（示例：阳痿有哪些症状？）")
            print("💡 输入'退出'可关闭系统")
            print("="*60)
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            sys.exit(1)
        
        # 2. 加载所有疾病名称
        self.disease_list = get_all_diseases(self.driver, TUGRAPH_CONFIG["database"])
        if not self.disease_list:
            print("⚠️ 警告：数据库中未检测到疾病数据，建议先导入数据！")
        else:
            print(f"📚 已加载 {len(self.disease_list)} 种疾病数据\n")

    def clear_screen(self):
        """清空屏幕"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

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

    def run(self):
        """运行自然语言对话循环"""
        while True:
            user_input = input("\n请输入你的查询（自然语言）：").strip()
            
            # 退出指令
            if user_input in ["退出", "quit", "exit"]:
                self.driver.close()
                print("\n🔌 已关闭数据库连接，感谢使用！")
                break
            
            # 空输入处理
            if not user_input:
                print("⚠️ 输入不能为空！")
                continue
            
            # 意图识别+执行查询
            intent_key, disease_name = self.recognize_intent(user_input)
            result = self.execute_query(intent_key, disease_name)
            print(result)

# ===================== 5. 启动系统 =====================
if __name__ == "__main__":
    dialog = MedicalNLUDialog()
    dialog.run()