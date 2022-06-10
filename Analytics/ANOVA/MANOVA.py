import pandas as pd
import warnings
import CommonLib.Common as common
import CommonLib.IMGManager as imgmanager
warnings.filterwarnings(action='ignore')
from statsmodels.multivariate.manova import MANOVA
import statsmodels.stats.multicomp as mc
import seaborn as sns
import matplotlib.pyplot as plt
common.DataFrame_PrintFull(pd)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from  sklearn.datasets import load_iris
import glob
nowdate = common.Regexp_OnlyNumberbyDate()

def histogram(df, independ, num):
    colour = ['red', 'green', 'blue', 'yellow', 'pink', 'purple', 'gray', 'navy', 'brown']
    df_new = df.drop_duplicates(subset='depend')
    df_new = sorted(df_new['depend'])
    df['depend'] = df['depend'].astype(str)

    result_Image = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'MANOVA_'+ str(num) +'Img_' + nowdate + '.png'

    group = []
    match = {}

    for i in range(len(df_new)):
        group.append(str(df_new[i]))
        match[group[i]] = colour[i]

    plt.clf()
    for group in match:
        subset = df[df['depend'] == group]
        sns.distplot(subset[independ], hist=True, kde=True, color=match[group], label=group)
    plt.title('depend'+"분류에 의한 종속변수 분포")
    plt.legend(prop={'size': 12}, title='group')
    plt.savefig(result_Image)

def tukeyhsdsummary(df, independ, num):

    result_Image = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'MANOVA_' + str(num) + 'Img_' + nowdate + '.png'

    # 사후 검정
    comp = mc.MultiComparison(df[independ], df['depend'])
    tukeyhsd = comp.tukeyhsd(alpha=0.05)
    fig = tukeyhsd.plot_simultaneous()
    plt.savefig(result_Image)

    tukeyhsd = [str(tukeyhsd.summary())]
    return tukeyhsd


def box(df, independ, num):
    result_Image = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'MANOVA_'+ str(num) +'Img_' + nowdate + '.png'
    df.boxplot(column=independ, by='depend', grid=False)
    plt.savefig(result_Image)


def manova_run(request_json):
    try:
        manova = []
        if __name__ == "__main__":
            df = pd.read_csv(common.get_local_file_path() + '연습.csv')
        else:
            df = pd.DataFrame(request_json)
        df_len = len(df.columns)


        for i in range(0, df_len):
            if i == 0:
                df.rename(columns={df.columns[i]: 'depend'}, inplace=True)
            else:
                df.rename(columns={df.columns[i]: 'independ'+str(i)}, inplace=True)

        for i in range(1,df_len):
            histogram(df, df.columns[i], i)
            box(df, df.columns[i], i+3)
            tukeyhsdsummary(df, df.columns[i], i+6)

        if df_len == 3:
            fit = MANOVA.from_formula('independ1 + independ2 ~ depend', data = df)
        elif df_len == 4:
            fit = MANOVA.from_formula('independ1 + independ2 + independ3 ~ depend', data = df)
        manova.append(str(fit.mv_test()))
        result_all = pd.DataFrame(manova, columns=['manova'])

        # print(pd.DataFrame(df.groupby('depend').mean()))
        # print(pd.DataFrame(df.groupby('depend').min()))
        # result_all = pd.concat([result_all, pd.DataFrame(str(df.groupby('depend').mean()), columns=["Mean"])], axis=1)
        # print(result_all)


        # 그룹별 사이즈, 평균, 표준편차, 최소, 최대
        mean = [str(df.groupby('depend').mean())]
        mean = pd.DataFrame(mean)
        mean.rename(columns={mean.columns[0]: "Mean"}, inplace=True)

        min = [str(df.groupby('depend').min())]
        min = pd.DataFrame(min)
        min.rename(columns={min.columns[0]: "Min"}, inplace=True)

        max = [str(df.groupby('depend').max())]
        max = pd.DataFrame(max)
        max.rename(columns={max.columns[0]: "Max"}, inplace=True)

        result_all = pd.concat([result_all, mean], axis=1)
        result_all = pd.concat([result_all, min], axis=1)
        result_all = pd.concat([result_all, max], axis=1)

        return result_all
    except Exception as err:
        common.exception_print(err)


if __name__ == "__main__":
    manova_run(None)

files = []
img = []
img2 = []
img3 = []
im = 'C:/Users/areum/Documents/GitHub/ML_Project/Data/Image/ReportResult/MANOVA_'
for i in range(1, 10):
    file = glob.glob(im + str(int(i)) +'Img_'+ nowdate + '.png')
    if len(file) == 1:
        files.append(file)

if len(files) == 9:
    img.extend([str(files[0][0]), str(files[3][0]), str(files[6][0])])
    img2.extend([str(files[1][0]), str(files[4][0]), str(files[7][0])])
    img3.extend([str(files[2][0]), str(files[5][0]), str(files[8][0])])
    imgmanager.all(img, 1)
    imgmanager.all(img2, 2)
    imgmanager.all(img3, 3)
else:
    img.extend([str(files[0][0]), str(files[2][0]), str(files[4][0])])
    img2.extend([str(files[1][0]), str(files[3][0]), str(files[5][0])])
    imgmanager.all(img, 1)
    imgmanager.all(img2, 2)