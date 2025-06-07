import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

def build_and_evaluate_model(file_path):
    # 1. 데이터 로드
    df = pd.read_excel(file_path)
    
    # 2. 피처 및 타겟 설정
    target = "인구소멸지수"
    X = df.select_dtypes(include=["number"]).drop(columns=[target])
    y = df[target]

    # 3. 결측치 처리
    X = X.fillna(X.mean())
    y = y.fillna(y.mean())

    # 4. 모델 정의 (튜닝된 하이퍼파라미터)
    model = XGBRegressor(
        subsample=0.6,
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        colsample_bytree=0.8,
        random_state=42
    )

    # 5. 교차검증 설정
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # 6. 교차검증 수동 수행
    r2_list, mse_list, rmse_list = [], [], []

    for train_idx, val_idx in kf.split(X):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        r2 = r2_score(y_val, y_pred)
        mse = mean_squared_error(y_val, y_pred)
        rmse = np.sqrt(mse)

        r2_list.append(r2)
        mse_list.append(mse)
        rmse_list.append(rmse)

    # 7. 평가 출력
    print(" Fold별 R²:", np.round(r2_list, 4))
    print(" Fold별 MSE:", np.round(mse_list, 6))
    print(" Fold별 RMSE:", np.round(rmse_list, 4))
    print(f"\n📈 평균 R²: {np.mean(r2_list):.4f}")
    print(f" 평균 MSE: {np.mean(mse_list):.6f}")
    print(f" 평균 RMSE: {np.mean(rmse_list):.4f}")

    # 전체 데이터로 모델 재학습
    model.fit(X, y)
    return model, X  # 최종 모델과 피처 순서 반환

# 🔮 사용자 입력 기반 예측 함수
def predict_new(model, X_columns, region_data: dict):
    input_df = pd.DataFrame([region_data])
    input_df = input_df[X_columns]  # 컬럼 순서 맞추기
    predicted_value = model.predict(input_df)[0]
    print(f"\n 예측된 인구소멸지수: {predicted_value:.4f}")
    return predicted_value

def show_feature_importance(model, feature_names):
    importances = model.feature_importances_
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)


    plt.figure(figsize=(8, 6))
    plt.barh(importance_df['Feature'][:10][::-1], importance_df['Importance'][:10][::-1])
    plt.xlabel("Importance Score")
    plt.title("🔍 XGBoost Feature Importance (Top 10)")
    plt.tight_layout()
    plt.show()

# 🧪 실행 예시
def main():
    model, X = build_and_evaluate_model("최종_통합_2018_2021_요양포함.xlsx")

    # 예시 입력값
    example_region = {
        '합계출산율': 1.09,
        '성비': 105.41,
        '고령인구비율': 10, #23.53 -> 10 
        '인구십만명당 문화기반시설 수': 15.89,
        '인구10만명당 사회복지시설수': 41.3,
        '재정자립도': 50, #25.7 -> 50
        '초등학교 수': 13,
        '전문대학 및 대학교 수': 0,
        '연도': 2018,
        '요양기관 수_전체': 197.0361
    }
    import matplotlib.font_manager as fm
    import platform

    plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
    show_feature_importance(model, X.columns.tolist())

    predict_new(model, X.columns.tolist(), example_region)


# 🚀 실행
if __name__ == "__main__":
    main()
