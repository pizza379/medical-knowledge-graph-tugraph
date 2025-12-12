# coding=utf-8
"""
TuGraph + Python 医疗知识图谱交互核心代码
适配medical数据库（疾病/症状/药物等节点）
"""
from neo4j import GraphDatabase, basic_auth

# ===================== 1. 配置TuGraph连接 =====================
# 替换为你的TuGraph实际配置（Docker部署默认如下）
TUGRAPH_CONFIG = {
    "uri": "bolt://localhost:7687",  # Bolt协议地址（Docker映射的7687端口）
    "username": "admin",             # 默认用户名
    "password": "73@TuGraph",        # 默认密码
    "database": "default"            # 你的医疗知识图谱数据库名
}

# ===================== 2. 初始化连接类 =====================
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
            print("✅ 成功连接TuGraph的medical数据库！")
        except Exception as e:
            raise RuntimeError(f"❌ 连接失败：{e}")

    def close(self):
        """关闭连接"""
        self.driver.close()
        print("🔌 已关闭TuGraph连接")

    # ===================== 3. 核心Cypher查询函数 =====================
    def get_disease_symptoms(self, disease_name):
        """
        Cypher查询：根据疾病名查症状
        :param disease_name: 疾病名称（如"阳痿"）
        :return: 症状列表/提示信息
        """
        # 核心Cypher语句
        cypher = """
        MATCH (d:Disease {name: $disease})-[r:HAS_SYMPTOM]->(s:Symptom)
        RETURN collect(s.name) AS symptoms
        """
        # 执行Cypher（指定medical数据库）
        with self.driver.session(database=TUGRAPH_CONFIG["database"]) as session:
            result = session.run(cypher, disease=disease_name)
            record = result.single()  # 获取单条结果
        
        if record and record["symptoms"]:
            return f"疾病【{disease_name}】的症状：{', '.join(record['symptoms'])}"
        else:
            return f"未查询到【{disease_name}】的症状信息"

    def get_symptom_diseases(self, symptom_name):
        """
        Cypher查询：根据症状名查疾病
        :param symptom_name: 症状名称（如"颈背疼痛"）
        :return: 疾病列表/提示信息
        """
        cypher = """
        MATCH (d:Disease)-[r:HAS_SYMPTOM]->(s:Symptom {name: $symptom})
        RETURN collect(d.name) AS diseases
        """
        with self.driver.session(database=TUGRAPH_CONFIG["database"]) as session:
            result = session.run(cypher, symptom=symptom_name)
            record = result.single()
        
        if record and record["diseases"]:
            return f"症状【{symptom_name}】对应的疾病：{', '.join(record['diseases'])}"
        else:
            return f"未查询到与【{symptom_name}】相关的疾病"

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

# ===================== 4. 测试交互 =====================
if __name__ == "__main__":
    # 初始化查询类
    query = TuGraphMedicalQuery()
    
    # 执行Cypher查询（测试示例）
    #print("\n=== 测试查询：疾病查症状 ===")
    #print(query.get_disease_symptoms("哮喘"))  # 替换为你的疾病名
    
    #print("\n=== 测试查询：症状查疾病 ===")
    #print(query.get_symptom_diseases("眼痛"))  # 替换为你的症状名
    
    print("\n=== 测试查询：疾病查药物 ===")
    print(query.get_disease_drugs("麦粒肿"))  # 替换为你的疾病名
    
    # 关闭连接
    query.close()