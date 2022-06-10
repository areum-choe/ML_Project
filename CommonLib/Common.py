import os
import sys
from datetime import datetime


def exception_print(err):
    """
    try 에러 발생시 오류구문 정의
    :param err:
    :return:
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print("★" * 40 + "Exception 오류발생 내용" + "★" * 40)
    print("Exception 내용:" + str(exc_type),
          "\nException 설명:" + str(err),
          "\n파일명:" + str(fname),
          "\n오류위치:" + str(exc_tb.tb_lineno))
    print("★" * 103)


def DataFrame_PrintFull(dataFrame, row=None, col=None):
    dataFrame.set_option('display.max_columns', col)  # 모든 열을 출력한다.
    dataFrame.set_option('display.max_rows', row)  # 모든 열을 출력한다.


def Create_EDA_Report(df):
    """
    탐색적 데이터 분석 EDA(Exploratory Data Analysis) 리포트 생성
    :param df:
    :return:
    """
    try:
        from pandas_profiling import ProfileReport  # pip install pandas-profiling
        # EDA Report 생성
        profile = ProfileReport(df,
                                minimal=False,
                                explorative=True,
                                title='Data Profiling',
                                plot={'histogram': {'bins': 8}},
                                pool_size=4,
                                progress_bar=False)

        # Report 결과 경로에 저장
        # todo 파일저장 멀티사용에 대한 처리 필요
        profile.to_file(output_file="data_profiling.html")
    except Exception as err:
        exception_print(err)


def get_local_file_path():
    return "C:/Users/areum/Desktop/POC시연자료/"


def DataFrame_Information(df):
    print("##############################################################")
    print("================= DataFrame - head() =========================")
    print("##############################################################")
    print(df.head())
    print("##############################################################")
    print("================= DataFrame - shape  =========================")
    print("##############################################################")
    print(df.shape)
    print("##############################################################")
    print("================= DataFrame - isnull().sum() =================")
    print("##############################################################")
    print(df.isnull().sum())
    print("##############################################################")
    print("================= DataFrame - info() =========================")
    print("##############################################################")
    print(df.info())
    print("##############################################################")


# def Word_Make_Sentense(paragraph, replace, text, color, fontSize, bold=False):
def Word_Make_Sentense(paragraph, item):
    """
    Word 문서에 작성할 Text 정의
    :param paragraph: paragraph객체
    :param replace: 공백변환 문자열
    :param text: 작성 text
    :param color: font 색상
    :param fontSize: font 크기
    :param bold: font 볼드 Y/N
    :return:
    """
    paragraph.text = paragraph.text.replace(str(item.text), "")
    run = paragraph.add_run(str(item.replaceText))
    run.font.color.rgb = item.color
    run.bold = item.bold
    run.font.size = item.fontSize
    run.font.name = '맑은 고딕'


def Word_Make_Image(paragraph, imagePath):
    """
    Word 문서에 작성할 이미지 정의
    :param paragraph:
    :param imagePath:
    :return:
    """
    run = paragraph.add_run()
    run.add_picture(imagePath)


def Regexp_OnlyNumberbyDate():
    """
    현재일자 공백없는 숫자만 출력
    :return:
    """
    import re
    return re.sub(r'[^0-9]', '', str(datetime.now()))


def ToDay(onlyDate=True):
    """
    현재일자 리턴
    :param onlyDate: True-현재일자 YYYY-mm-dd False-YYYY-mm-dd HH:MM
    :return:
    """
    if onlyDate:
        resultDate = str(datetime.today().strftime('%Y-%m-%d'))
    else:
        resultDate = str(datetime.today().strftime('%Y-%m-%d %H:%M'))

    return resultDate


def Path_Prj_Main():
    """
    프로젝트 메인 상대경로를 리턴
    :return:
    """
    from pathlib import Path
    return str(str(Path(__file__).parent.parent) + '\\').replace('\\', '/')
