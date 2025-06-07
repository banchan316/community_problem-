import pandas as pd
import os

for year in range(2018, 2024):  # 2018~2023
    short_year = str(year)[2:]  # "2018" → "18"
    print(f"\n📅 {year}년 병합 시작 ===============================")

    # ① 기준 CSV 로드
    base_path = f"인구소멸지수{short_year}_top_bottom10.csv"
    base = pd.read_csv(base_path)
    base = base.rename(columns={"도시": "시군구"})
    base["시군구"] = base["시군구"].astype(str).str.strip()

    # ② 엑셀 파일 리스트
    folder_path = f"C:/Users/ckseh/OneDrive/바탕 화면/공모전/학교/연도 별 feature들/{year}"
    excel_files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]

    # ③ 파일-시트 반복
    for file in excel_files:
        full_path = os.path.join(folder_path, file)
        xls = pd.ExcelFile(full_path)
        sheet_list = xls.sheet_names[1:]  # ✅ 시트 2번째부터 병합

        for sheet in sheet_list:
            print(f"📂 병합 중: {file} - 시트: {sheet}")
            df_raw = pd.read_excel(xls, sheet_name=sheet, header=None)

            if df_raw.shape[0] < 3:
                print(f"⚠️ 시트 {sheet}에 데이터가 부족합니다. 건너뜀.")
                continue

            real_header = df_raw.iloc[1]
            final_columns = ['시도', '시군구'] + real_header[2:].tolist()

            df = df_raw.iloc[2:].copy()
            df.columns = final_columns
            df["시군구"] = df["시군구"].astype(str).str.strip()
            df.columns = df.columns.str.strip()  # ✅ 열 이름 공백 제거
            df = df.drop(columns=["시도"], errors="ignore")

            # ✅ 청년고용률 평균 처리
            if "청년고용률_상반기" in df.columns and "청년고용률_하반기" in df.columns:
                df["청년고용률_상반기"] = pd.to_numeric(df["청년고용률_상반기"], errors="coerce")
                df["청년고용률_하반기"] = pd.to_numeric(df["청년고용률_하반기"], errors="coerce")
                df["청년고용률"] = df[["청년고용률_상반기", "청년고용률_하반기"]].mean(axis=1)
                df.drop(columns=["청년고용률_상반기", "청년고용률_하반기"], inplace=True)

            # ✅ 중복 컬럼 제거
            overlap = [col for col in df.columns if col in base.columns and col != "시군구"]
            df = df.drop(columns=overlap)

            # 병합
            base = pd.merge(base, df, on="시군구", how="left")

    # ④ 저장
    output_path = f"최종병합결과_{year}.csv"
    base.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 저장 완료: {output_path}")
