import pandas as pd
import xml.etree.ElementTree as ET
from statsmodels.formula.api import ols
from itertools import combinations
from lightgbm import LGBMRegressor

# -------------------------
# 1. CSV 불러오기
# -------------------------
csv_path = "data/2024년도.CSV"
df = pd.read_csv(csv_path, encoding="cp949")
df.columns = df.columns.str.replace(" ", "_")

# -------------------------
# 2. XML -> DataFrame 변환
# -------------------------
def parse_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    rows = []
    for ev in root.find("glucose_level").findall("event"):
        rows.append({
            "ts": pd.to_datetime(ev.get("ts"), format="%d-%m-%Y %H:%M:%S"),
            "glucose": float(ev.get("value"))
        })
    return pd.DataFrame(rows)

patient_563 = parse_xml("data/563-ws-training.xml")
patient_588 = parse_xml("data/588-ws-training.xml")
patient_570 = parse_xml("data/570-ws-training.xml")

# -------------------------
# 3. Feature 생성 (예: 평균 혈당)
# -------------------------
for pid, patient_df in [("563", patient_563), ("588", patient_588), ("570", patient_570)]:
    print(f"환자 {pid} 평균 혈당: {patient_df['glucose'].mean():.2f}")

# -------------------------
# 4. CSV + XML 접목: 예시
# -------------------------
# CSV에서 변수 조합 탐색 (OLS)
target = "감마지피티"
col_list = [c for c in df.columns if c not in ["성별코드", target]]

best_score, best_formula = -1, None
for num in range(1, len(col_list)+1):
    for combi in combinations(col_list, num):
        formula = target + " ~ " + " + ".join(combi)
        model = ols(formula, data=df).fit()
        # 간단히 R^2 점수로 비교
        score = model.rsquared
        if score > best_score:
            best_score, best_formula = score, formula

print("최적 변수 조합:", best_formula, ">> R^2=", best_score)

# -------------------------
# 5. LightGBM으로 학습
# -------------------------
X = df[col_list]
y = df[target]

model = LGBMRegressor()
model.fit(X, y)
print("LGBM Feature Importance:", model.feature_importances_)
