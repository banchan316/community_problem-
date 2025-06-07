import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import platform

plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 데이터 불러오기
df = pd.read_csv("최종병합결과_2019.csv")

# 수치형 컬럼만 선택
numeric_df = df.select_dtypes(include=["number"])

# 상관계수 계산
corr_matrix = numeric_df.corr()

# 인구소멸지수 기준 정렬된 상관계수만 추출
target = "인구소멸지수"
if target in corr_matrix.columns:
    target_corr = corr_matrix[[target]].drop(index=target).sort_values(by=target, ascending=False)

    # 히트맵 시각화
    plt.figure(figsize=(6, len(target_corr) * 0.5 + 1))
    sns.heatmap(target_corr,
                annot=True,
                cmap='coolwarm',
                fmt=".2f",
                cbar=True,
                linewidths=0.5)

    plt.title("📊 인구소멸지수와 변수별 상관관계 (히트맵)", fontsize=14)
    plt.tight_layout()
    plt.show()
else:
    print("❌ '인구소멸지수' 컬럼이 존재하지 않습니다!")
