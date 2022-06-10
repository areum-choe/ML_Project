import pandas as pd
import warnings
import CommonLib.Common as common
warnings.filterwarnings(action='ignore')
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.stats.multicomp as mc
import CommonLib.IMGManager as imgmanager
common.DataFrame_PrintFull(pd)
import glob
from PIL import Image


plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

nowdate = common.Regexp_OnlyNumberbyDate()

def histogram(df, independ):
    colour = ['red', 'green', 'blue', 'yellow', 'pink', 'purple', 'gray', 'navy', 'brown']
    df_new = df.drop_duplicates(subset=independ)
    df_new = sorted(df_new[independ])
    df[independ] = df[independ].astype(str)

    result_Image = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'ANOVA_' + independ + 'Img_' + nowdate + '.png'

    group = []
    match = {}

    for i in range(len(df_new)):
        group.append(str(df_new[i]))
        match[group[i]] = colour[i]

    plt.clf()
    for group in match:
        subset = df[df[independ] == group]
        sns.distplot(subset['depend'], hist=True, kde=True, color=match[group], label=group)
    plt.title(independ+"분류에 의한 종속변수 분포")
    plt.legend(prop={'size': 12}, title='group')
    plt.savefig(result_Image)




def tukeyhsdsummary(df, independ):

    result_Image = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'ANOVA_' + independ + 'Img_' + nowdate + '.png'

    # 사후 검정
    comp = mc.MultiComparison(df['depend'], df[independ])
    tukeyhsd = comp.tukeyhsd(alpha=0.05)
    fig = tukeyhsd.plot_simultaneous()
    plt.savefig(result_Image)

    tukeyhsd = [str(tukeyhsd.summary())]
    return tukeyhsd


def anova_run(request_json):
    try:
        anovalm = []

        if __name__ == "__main__":
            df = pd.read_csv(common.get_local_file_path() + 'anova_test.csv')
        else:
            df = pd.DataFrame(request_json)

        df.columns = ['independ1','independ2','depend']

        # 정규분포 시각화
        histogram(df, 'independ1')
        histogram(df, 'independ2')

        result_Image2 = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'ANOVA_independ3Img_' + nowdate + '.png'
        result_Image3 = common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'ANOVA_independ4Img_' + nowdate + '.png'

        # 첫번째 범주로 구분한 boxplot
        df.boxplot(column='depend', by='independ1', grid=False)
        plt.savefig(result_Image2)
        # # 두번째 범주로 구분한 boxplot
        df.boxplot(column='depend', by='independ2', grid=False)
        plt.savefig(result_Image3)


        model = ols('depend~ C(independ1) * C(independ2)', df).fit()
        anovalm.append(str(anova_lm(model)))


        df.columns = ['independ5', 'independ6', 'depend']

        # 사후검정
        # tukeyhsd_summary1 = tukeyhsdsummary(df, 'independ1')
        # tukeyhsd_summary2 = tukeyhsdsummary(df, 'independ2')


        result_all = pd.concat([pd.DataFrame(anovalm, columns=['anova_lm']),
                                pd.DataFrame(tukeyhsdsummary(df, 'independ5'), columns=['tukeyhsd_summary1'])], axis=1)

        result_all = pd.concat([result_all,pd.DataFrame(tukeyhsdsummary(df, 'independ6'), columns=['tukeyhsd_summary2'])], axis=1)
        # print(result_all)


        # files = []
        # img = []
        # im = 'C:/Users/areum/PycharmProjects/FastAPIServer2/Data/Image/ReportResult/ANOVA_independ'
        # for i in range(0, 6):
        #     file = glob.glob(im + str(int(i+1)) +'Img_'+ nowdate + '.png')
        #     files.append(file)
        #     img.append(str(files[i][0]))
        #
        # img1 = cv2.imread(img[0], 1)
        # img2 = cv2.imread(img[1], 1)
        # img3 = cv2.imread(img[2], 1)
        # img4 = cv2.imread(img[3], 1)
        # img5 = cv2.imread(img[4], 1)
        # img6 = cv2.imread(img[5], 1)
        #
        # img1 = cv2.resize(img1, (1030, 960))
        # img2 = cv2.resize(img2, (1030, 960))
        # img3 = cv2.resize(img3, (1030, 960))
        # img4 = cv2.resize(img4, (1030, 960))
        # img5 = cv2.resize(img5, (1030, 960))
        # img6 = cv2.resize(img6, (1030, 960))
        #
        # addv1 = cv2.vconcat([img1, img3, img5])
        # addv2 = cv2.vconcat([img2, img4, img6])
        # cv2.imwrite(common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'All1_ANOVA' + nowdate + '.png', addv1)
        # cv2.imwrite(common.Path_Prj_Main() + 'Data/Image/ReportResult/' + 'All2_ANOVA' + nowdate + '.png', addv2)

        return result_all
    except Exception as err:
        common.exception_print(err)


if __name__ == "__main__":
    anova_run(None)

files = []
img = []
img2 = []
im = 'C:/Users/areum/Documents/GitHub/ML_Project/Data/Image/ReportResult/ANOVA_independ'
for i in range(0, 6):
    file = glob.glob(im + str(int(i+1)) +'Img_'+ nowdate + '.png')
    files.append(file)
    if i % 2 == 0:
        img.append(str(files[i][0]))
    else:
        img2.append(str(files[i][0]))

imgmanager.all(img, 1)
imgmanager.all(img2, 2)
