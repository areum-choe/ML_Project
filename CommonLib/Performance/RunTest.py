import pandas as pd
import CommonLib.Common as common


def front_Rexp(text, frontText, endText):
    try:
        return text[text.find(frontText):text.find(endText)].replace(frontText, '').strip()
    except Exception as err:
        common.exception_print(err)


def end_Rexp(text, frontText):
    try:
        return text[text.find(frontText):].replace(frontText, '').strip()
    except Exception as err:
        common.exception_print(err)

try:
    result_text = """Dep. Variable:                  DEPEN   R-squared:                       0.098
    Model:                            OLS   Adj. R-squared:                  0.091
    Method:                 Least Squares   F-statistic:                     12.88
    Date:                Fri, 21 Jan 2022   Prob (F-statistic):           0.000485
    Time:                        10:20:06   Log-Likelihood:                -492.36
    No. Observations:                 120   AIC:                             988.7
    Df Residuals:                     118   BIC:                             994.3
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept     -3.2910      3.911     -0.842      0.402     -11.035       4.453
    INDEPEN        0.2288      0.064      3.589      0.000       0.103       0.355
    ==============================================================================
    Omnibus:                      150.960   Durbin-Watson:                   1.403
    Prob(Omnibus):                  0.000   Jarque-Bera (JB):             4276.478
    Skew:                           4.598   Prob(JB):                         0.00
    Kurtosis:                      30.762   Cond. No.                         178."""

    print(front_Rexp(result_text, 'No. Observations:', 'AIC:'))
    print(end_Rexp(result_text, 'Cond. No.'))



    # print('R-squared:' + front_Rexp(result_text, 'R-squared:', 'Model:'))
    # print('Adj. R-squared:' + front_Rexp(result_text, 'Adj. R-squared:', 'Method:'))
    # print(front_Rexp(result_text, 'Method:', 'F-statistic:'))
    # print(front_Rexp(result_text, 'Prob (F-statistic):', 'Time:'))
    # print(front_Rexp(result_text, 'Log-Likelihood:', 'No. Observations:'))
    # print(end_Rexp(result_text, 'Cond. No.'))


except Exception as err:
    common.exception_print(err)