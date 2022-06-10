import CommonLib.Common as common
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import CommonLib.Performance.PerformanceManager as pfm
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.tree import DecisionTreeClassifier
import CommonLib.Report.WordManager as word
import warnings
warnings.filterwarnings(action='ignore')


common.DataFrame_PrintFull(pd)


def logisticRegression_run(request_json):
    try:
        if __name__ == "__main__":
            df = pd.read_csv(common.get_local_file_path() + '로지스틱.csv')
            df['sex'] = df['sex'].map({'F': 0, 'M': 1})
        else:
            df = pd.DataFrame(request_json)

        df = df.dropna(axis=0)
        df = df.astype('float')

        x = df.iloc[:, 1:]
        y = df.iloc[:, [0]]
        y = y.astype('int')

        train_x, test_x, train_y, test_y = train_test_split(x, y, train_size=0.7, test_size=0.3, random_state=1)

        model = sm.Logit(train_y, train_x)
        results = model.fit()

        # summary
        summary_arr = [str(results.summary())]
        df_summary = pd.DataFrame(summary_arr)

        df_summary.rename(columns={df_summary.columns[0]: "SUMMARY"}, inplace=True)

        # 오즈 비(Odds Ratio) 출력 - height을 예로 들어보면 키가 커질 수록 남자가 될 확률이 높아진다는 뜻
        params = pd.DataFrame(np.exp(results.params)).reset_index()
        params.columns = ['Params', 'Odds Ratio']

        # 합치기
        result_all = pd.concat([df_summary, params], axis=1)

        # 모델 적용 전 정규화
        scaler = StandardScaler()
        train_x_scaled = scaler.fit_transform(train_x)
        test_x_scaled = scaler.transform(test_x)

        # 모델 적용
        lr = LogisticRegression()
        lr.fit(train_x_scaled, train_y)

        # train 정확도
        train_score = lr.score(train_x_scaled, train_y)

        # test 정확도
        test_score = lr.score(test_x_scaled, test_y)

        # 예측정확도
        y_pred = lr.predict(test_x_scaled)
        acc = metrics.accuracy_score(test_y, y_pred)

        result_all = pd.concat([result_all, pd.DataFrame(list(np.array(acc).reshape(1)), columns=['Acc'])], axis=1)



        # 모델 피쳐 중요도
        feature_importance = pd.DataFrame(list(zip(train_x.columns, np.array(lr.coef_).reshape(7))),
                                          columns=['Features', 'Importances']).sort_values('Importances')

        result_all = pd.concat([result_all, feature_importance], axis=1)

        # 평가지표
        eval_all = pfm.eval_all(test_y, pd.DataFrame(y_pred))
        result_all = pd.concat([result_all, pd.DataFrame(eval_all, columns=['평가지표'])], axis=1)

        result_Image = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'LogisticImg_' + common.Regexp_OnlyNumberbyDate() + '.png'

        # 결정 트리
        dt = DecisionTreeClassifier(max_depth=3, random_state=42)
        dt.fit(x, y)
        plt.figure(figsize=(16, 8))
        plot_tree(dt, filled=True, feature_names=list(x.columns.values))
        plt.savefig(result_Image)

        # todo 이부분 추가됌
        # 설명변수명 리스트
        feature_name = x.columns
        plt.figure(figsize=(10, 30))
        for col_idx in range(len(feature_name)):
            # 6행 2열 서브플롯에 각 feature 박스플롯 시각화
            plt.subplot(4, 2, col_idx + 1)
            # 0에 해당하는 데이터 histogram 시각화
            plt.hist(df[df[df.columns[0]] == 0][feature_name[col_idx]], label="0", alpha=0.5)
            # 1에 해당하는 데이터 histogram 시각화
            plt.hist(df[df[df.columns[0]] == 1][feature_name[col_idx]], label="1", alpha=0.5)
            plt.legend()
            # 그래프 타이틀: feature name
            plt.title("Feature: " + feature_name[col_idx], fontsize=10)


        # sklearn에서 ROC 패키지 활용
        fpr, tpr, thresholds = metrics.roc_curve(test_y, y_pred, pos_label=1)

        # ROC curve
        plt.plot(fpr, tpr)

        # AUC
        auc = np.trapz(tpr, fpr)
        # AUC는 1에 가까울수록 모델의 성능이 좋은 것이며, ROC curve는 (0,1)로 그래프가 가까이 갈 수록 정확도가 좋은 것

        result_all = pd.concat([result_all, pd.DataFrame(list(np.array(auc).reshape(1)), columns=['AUC'])], axis=1)

        result_all = result_all.round({'Odds Ratio':3,'Importances':3,'Acc':3, 'AUC':3})


        # # 분석결과 리포트 생성
        # fileNameArr = [word.CreateReport_LogisticRegression(result_all, result_Image)]
        # return_df = pd.concat([result_all, pd.DataFrame(fileNameArr, columns=["FILENAME"])], axis=1)

        print(result_all)
        return result_all

    except Exception as err:
        common.exception_print(err)


if __name__ == "__main__":
    logisticRegression_run(None)