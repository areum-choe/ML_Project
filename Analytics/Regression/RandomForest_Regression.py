import numpy as np
import pandas as pd
import warnings
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import CommonLib.Common as common
from sklearn.metrics import accuracy_score # 정확도 함수
import CommonLib.Performance.PerformanceManager as pfm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
import matplotlib.font_manager as fm
import matplotlib
# 그래프에서 마이너스 폰트 깨지는 문제에 대한 대처
matplotlib.rcParams['axes.unicode_minus'] = False
## 한글 폰트 적용 ( 안하면 한글 깨짐 )
f_name = fm.FontProperties(fname="C:/Windows/Fonts/malgunbd.ttf").get_name()
plt.rc('font', family=f_name)
from sklearn.metrics import confusion_matrix


warnings.filterwarnings(action='ignore')

def randomforest_run(request_json):
    try:

        n_estimators = 5
        max_depth = 5
        min_samples_leaf = 4
        min_samples_split = 4

        if __name__ == "__main__":
            df = pd.read_csv(common.get_local_file_path() + '로지스틱_회귀.csv')
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
        else:
            df = df

        df = df.dropna(axis=0)
        x = df.iloc[:, 1:]
        y = df.iloc[:, [0]]
        y = y.astype('int')


        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)

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

        print('Accuracy: ', metrics.accuracy_score(y_test, pred_y))


        # params = {'n_estimators': [100,200],
        #          'max_depth': [2, 4, 6, 8, 10, 12],
        #         'min_samples_leaf': [2, 4, 6, 8, 12, 18],
        #         'min_samples_split': [2, 4, 6, 8, 16, 20]}
        #
        # rf_clf = RandomForestClassifier(n_jobs=-1)
        # grid_cv = GridSearchCV(rf_clf, param_grid=params, cv=2, n_jobs=-1)
        # grid_cv.fit(X_train, y_train.values.ravel())
        # a = grid_cv.best_params_
        # result_all = pd.concat([result_all, pd.DataFrame.from_records([a])], axis=1)

        # print('최적의 하이퍼 파라미터 :', grid_cv.best_params_)
        # print('최적의 예측 정확도 :', grid_cv.best_score_)


        # np.random.seed(123)
        # x=np.random.randn(10000)
        # y=2*np.random.randn(10000+2)
        # plt.hist(result_all.실제값, bins=80, color='blue',density=True, alpha=0.3)
        # plt.hist(result_all.예측값, bins=80, color='red', density=True, alpha=0.3)
        # plt.show()

        sns.kdeplot(result_all.실제값,shade=True,bw=2,label="실제값")
        sns.kdeplot(result_all.예측값, shade=True, bw=2, label="예측값")
        plt.legend()
        plt.show()
        # print(result_all.index)
        # sns.distplot(data=result_all.index,data2=result_all.실제값, bins=80, color='blue')
        # sns.distplot(data=result_all.index,data2=result_all.예측값, bins=80, color='red')
        # plt.title('HISTOGRAM')  # 그래프 제목
        # plt.xlabel("X")  # x축 이름
        # plt.ylabel("Density")  # y축 이름
        # plt.show()

        bins = np.linspace(0, len(result_all.예측값))
        plt.hist(result_all.실제값, bins, alpha=0.5, label='a')
        plt.hist(result_all.예측값, bins, alpha=0.5, label='b')
        plt.legend(loc='upper left')

        plt.show()

        return acc

    except Exception as err:
        common.exception_print(err)


if __name__ == "__main__":
    randomforest_run(None)