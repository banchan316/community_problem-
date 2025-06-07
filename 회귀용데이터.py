import pandas as pd

# ▶ 결과 저장용 리스트
all_years = []

# ▶ 처리할 연도
for year in range(2018, 2022):  # 2018 ~ 2021
    file_path = f"회귀모델데이터_{year}.csv"
    print(f"📂 {year}년 파일 처리 중...")

    # ① CSV 로드
    df = pd.read_csv(file_path)

    # ② '요양기관 수_전체' 컬럼을 숫자형으로 변환
    df["요양기관 수_전체"] = pd.to_numeric(df["요양기관 수_전체"], errors="coerce")

    # ③ 평균 계산 (0, NaN 제외)
    valid_mask = (df["요양기관 수_전체"].notna()) & (df["요양기관 수_전체"] != 0)
    mean_val = df.loc[valid_mask, "요양기관 수_전체"].mean()

    # ④ 0 또는 NaN → 평균값으로 대체
    df["요양기관 수_전체"] = df["요양기관 수_전체"].replace(0, pd.NA)
    df["요양기관 수_전체"] = df["요양기관 수_전체"].fillna(mean_val)

    # ⑤ 시군구별 중복 제거
    df_unique = df.groupby("시군구", as_index=False).first()

    # ⑥ 연도 컬럼 추가
    df_unique["연도"] = year

    # ⑦ 리스트에 추가
    all_years.append(df_unique)

# ▶ 연도별 데이터 병합
final_df = pd.concat(all_years, ignore_index=True)

# ▶ 엑셀로 저장
final_df.to_excel("최종_통합_2018_2021_요양포함.xlsx", index=False)

print("✅ 모든 연도 통합 완료: 최종_통합_2018_2021_요양포함.xlsx")
