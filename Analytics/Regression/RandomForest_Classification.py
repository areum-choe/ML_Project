import numpy as np
import pandas as pd
import warnings
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import CommonLib.Common as common
from sklearn.metrics import accuracy_score # 정확도 함수
import CommonLib.Performance.PerformanceManager as pfm
import CommonLib.Report.WordManager as word
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.metrics import confusion_matrix
pd.set_option('display.max_rows', None)

warnings.filterwarnings(action='ignore')

def randomforest_run(request_json):
    try:

        n_estimators = 5
        max_depth = 5
        min_samples_leaf = 4
        min_samples_split = 4

        if __name__ == "__main__":
            df = pd.read_csv(common.get_local_file_path() + '로지스틱.csv')
            df['sex'] = df['sex'].map({'F': 0, 'M': 1})
        else:
            df = pd.DataFrame(request_json)

        # df = df.dropna(axis=0)
        # df = df.astype('float')


        if 'n_estimators' in df.columns:
            df_params = df.loc[:, ['n_estimators','max_depth','random_state']]
            df_params = df_params.dropna()
            n_estimators = df_params['n_estimators'].values[0].astype('int')
            max_depth = df_params['max_depth'].values[0].astype('int')
            min_samples_leaf = df_params['min_samples_leaf'].values[0].astype('int')
            min_samples_split = df_params['min_samples_split'].values[0].astype('int')
            df = df.drop(['n_estimators', 'max_depth', 'random_state'], axis=1)

            df = df.dropna(axis=0)
            x = df.iloc[:, 1:]
            y = df.iloc[:, [0]]
            y = y.astype('int')

            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        else:
            df = df
            df = df.dropna(axis=0)
            x = df.iloc[:, 1:]
            y = df.iloc[:, [0]]
            y = y.astype('int')

            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            params = {'n_estimators': [100, 200],
                      'max_depth': [2, 4, 6, 8, 10, 12],
                      'min_samples_leaf': [2, 4, 6, 8, 12, 18],
                      'min_samples_split': [2, 4, 6, 8, 16, 20]}

            rf_clf = RandomForestClassifier(n_jobs=-1)
            grid_cv = GridSearchCV(rf_clf, param_grid=params, cv=2, n_jobs=-1)
            grid_cv.fit(X_train, y_train.values.ravel())
            best_params = grid_cv.best_params_
            best_params = pd.DataFrame.from_records([best_params])

            n_estimators = int(best_params['n_estimators'])
            max_depth = int(best_params['max_depth'])
            min_samples_leaf = int(best_params['min_samples_leaf'])
            min_samples_split = int(best_params['min_samples_split'])

        clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_leaf=min_samples_leaf, min_samples_split=min_samples_split )
        clf.fit(X_train, y_train.values.ravel())

        pred_y = clf.predict(X_test)
        acc = [accuracy_score(y_test, pred_y)]

        y_test = y_test.reset_index(drop=True)
        y_test.columns = ['실제값']

        result_all = pd.concat([y_test, pd.DataFrame(pred_y, columns=['예측값'])], axis=1)
        result_all = pd.concat([result_all, pd.DataFrame(result_all.실제값 - result_all.예측값, columns=['오차값'])], axis=1)

        # 정확도
        result_all = pd.concat([result_all, pd.DataFrame(list(acc), columns=['정확도'])], axis=1)

        # 평가지표
        eval_all = pfm.eval_all(y_test, pd.DataFrame(pred_y))
        result_all = pd.concat([result_all, pd.DataFrame(eval_all, columns=['평가지표'])], axis=1)

        # 피처 중요도
        feature_importance = clf.feature_importances_
        feature_importance = pd.Series(feature_importance, index=X_train.columns)
        feature_top = feature_importance.sort_values(ascending=False)[:len(x)]

        feature = pd.DataFrame(feature_top.reset_index())
        feature.columns =['feature','importance']

        result_all = pd.concat([result_all, feature], axis=1)

        result_Image = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'RandomForesttImg_' + common.Regexp_OnlyNumberbyDate() + '.png'

        confusion_matrix = pd.crosstab(result_all['실제값'], result_all['예측값'], rownames=['Actual'], colnames=['Predicted'])
        sns.heatmap(confusion_matrix, annot=True)
        plt.savefig(result_Image)

        # 설명변수명 리스트
        feature_name = x.columns
        plt.figure(figsize=(10, 30))
        for col_idx in range(len(feature_name)):
            # 6행 2열 서브플롯에 각 feature 박스플롯 시각화
            plt.subplot(4, 2, col_idx + 1)
            # 0에 해당하는 데이터 histogram 시각화
            plt.hist(df[df[df.columns[0]] == 0][feature_name[col_idx]], label=df.columns[0]+":0", alpha=0.5)
            # 1에 해당하는 데이터 histogram 시각화
            plt.hist(df[df[df.columns[0]] == 1][feature_name[col_idx]], label=df.columns[0]+":1", alpha=0.5)
            plt.legend()
            # 그래프 타이틀: feature name
            plt.title("Feature: " + feature_name[col_idx], fontsize=10)
        plt.show()

        result_all = result_all.round({'정확도': 3, '평가지표': 3,'importance': 3})

        # # 분석결과 리포트 생성
        fileNameArr = [word.CreateReport_RandomForest(result_all, result_Image)]
        result_df = pd.concat([result_all, pd.DataFrame(fileNameArr, columns=["FILENAME"])], axis=1)


        return acc

    except Exception as err:
        common.exception_print(err)


if __name__ == "__main__":
    randomforest_run(None)