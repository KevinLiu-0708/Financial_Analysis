# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:31:34 2022

@author: 111036
"""

import requests
import pandas as pd
import time
import numpy as np


def Statement_Parse(stock_id):

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    
    # balance sheet
    url = 'https://emops.twse.com.tw/server-java/t164sb03_e?TYPEK=all&step=show&co_id={}&year=2022&season=1&report_id=C'.format(stock_id)
       
    res = requests.get(url, headers=headers, verify=False)
    BalanceSheet = pd.read_html(res.text)[2]
    
    column_list = ['Accounting_Title', '2022Q1', 'col1', '2021Q1']
    BalanceSheet.columns = column_list
    
    BalanceSheet['Accounting_Title'] = BalanceSheet['Accounting_Title'].replace('¡@', '', regex=True)
    BalanceSheet = BalanceSheet[['Accounting_Title', '2022Q1', '2021Q1']]
    BalanceSheet = BalanceSheet.set_index('Accounting_Title')
    BalanceSheet.to_excel('C:/Users/111036/Desktop/股價/BalanceSheet.xlsx')
    time.sleep(5)
    
    # Comprehensive Income
    url = 'https://emops.twse.com.tw/server-java/t164sb04_e?TYPEK=all&step=show&co_id={}&year=2022&season=1&report_id=C'.format(stock_id)
    
    res = requests.get(url, headers=headers, verify=False)
    Comp_Income = pd.read_html(res.text)[2]
    
    column_list = ['Accounting_Title', '2022Q1', '2021Q1']
    Comp_Income.columns = column_list
    Comp_Income['Accounting_Title'] = Comp_Income['Accounting_Title'].replace('¡@', '', regex=True)
    Comp_Income = Comp_Income.drop_duplicates(subset=('Accounting_Title'))
    Comp_Income = Comp_Income.set_index('Accounting_Title')
    Comp_Income.to_excel('C:/Users/111036/Desktop/股價/Comp_Income.xlsx')
    time.sleep(5)
    
    # Cash Flow
    url = 'https://emops.twse.com.tw/server-java/t164sb05_e?TYPEK=all&step=show&co_id={}&year=2022&season=1&report_id=C'.format(stock_id)
    
    res = requests.get(url, headers=headers, verify=False)
    CashFlow = pd.read_html(res.text)[2]
    
    column_list = ['Accounting_Title', '2022Q1', '2021Q1']
    CashFlow.columns = column_list
    
    CashFlow['Accounting_Title'] = CashFlow['Accounting_Title'].replace('¡@', '', regex=True)
    CashFlow = CashFlow.set_index('Accounting_Title')
    CashFlow.to_excel('C:/Users/111036/Desktop/股價/CashFlow.xlsx')

    return BalanceSheet, Comp_Income, CashFlow

def F_Score(BalanceSheet, Comp_Income, CashFlow, stock_id):
    dic = dict()
    # F Score
    ## Profitability
    ### 1. ROA
    ROA = Comp_Income.loc['Profit (loss) from continuing operations', '2022Q1'] / BalanceSheet.loc['Total assets', '2022Q1']
    if ROA > 0:
        dic['F_ROA'] = 1
    else:
        dic['F_ROA'] = 0
    ### 2. CFO
    CFO = CashFlow.loc['Net cash flows from (used in) operating activities', '2022Q1']
    if CFO > 0:
        dic['F_CFO'] = 1
    else:
        dic['F_CFO'] = 0
    ### 3. D_ROA
    ROA_lastYear =  Comp_Income.loc['Profit (loss) from continuing operations', '2021Q1'] / BalanceSheet.loc['Total assets', '2021Q1']
    if ROA > ROA_lastYear:
        dic['F_D_ROA'] = 1
    else:
        dic['F_D_ROA'] = 0
    ### 4. ACCRUAL
    if CFO > Comp_Income.loc['Profit (loss) from continuing operations', '2022Q1']:
        dic['F_ACCRUAL'] = 1
    else:
        dic['F_ACCRUAL'] = 0
    
    
    ## Leverage, Liquidity, source of fund
    ### 1. Leverage
    LTD_ratio = BalanceSheet.loc['Total non-current liabilities', '2022Q1'] / BalanceSheet.loc['Total assets', '2022Q1']
    LTD_ratio_lastYear = BalanceSheet.loc['Total non-current liabilities', '2021Q1'] / BalanceSheet.loc['Total assets', '2021Q1']
    if LTD_ratio < LTD_ratio_lastYear:
        dic['F_D_LEVER'] = 1
    else:
        dic['F_D_LEVER'] = 0
    ### 2. Liquidity
    Curr_ratio = BalanceSheet.loc['Total current assets', '2022Q1'] / BalanceSheet.loc['Total current liabilities', '2022Q1']
    Curr_ratio_lastYear = BalanceSheet.loc['Total current assets', '2021Q1'] / BalanceSheet.loc['Total current liabilities', '2021Q1']
    if Curr_ratio > Curr_ratio_lastYear:
        dic['F_D_LIQUID'] = 1
    else:
        dic['F_D_LIQUID'] = 0
    ### 3. source of fund
    if BalanceSheet.loc['Ordinary share', '2022Q1'] > BalanceSheet.loc['Ordinary share', '2021Q1']:
        dic['F_EQ_OFFER'] = 1
    else:
        dic['F_EQ_OFFER'] = 0
    ## Operating efficiency
    ### 1. Gross Margin
    Gross_Margin = Comp_Income.loc['Gross profit (loss) from operations', '2022Q1'] / Comp_Income.loc['Total operating revenue', '2022Q1']
    Gross_Margin_lastYear = Comp_Income.loc['Gross profit (loss) from operations', '2021Q1'] / Comp_Income.loc['Total operating revenue', '2021Q1']
    if Gross_Margin > Gross_Margin_lastYear:
        dic['F_D_MARGIN'] = 1
    else:
        dic['F_D_MARGIN'] = 0
    ### 2. Asset TurnOver
    Asset_TO = Comp_Income.loc['Total operating revenue', '2022Q1'] / BalanceSheet.loc['Total assets', '2022Q1']
    Asset_TO_lastYear = Comp_Income.loc['Total operating revenue', '2021Q1'] / BalanceSheet.loc['Total assets', '2021Q1']
    if Asset_TO > Asset_TO_lastYear:
        dic['F_D_TURN'] = 1
    else:
        dic['F_D_TURN'] = 0
    
    dic['F_Score'] = sum(dic.values())
    
    df = pd.DataFrame(list(dic.items()), columns=['Title', stock_id])
    df = df.set_index('Title')
    return df
'''
stocks = ['3498', '3093', '4554', '5493', '5489', '3541', '8047', '6146', '3303', 
          '3285', '6613', '3642', '3551', '5536', '3289']
'''
stocks = ['6547']
score_table = pd.DataFrame()
for stock_id in stocks:
    BalanceSheet, Comp_Income, CashFlow = Statement_Parse(stock_id)
    df = F_Score(BalanceSheet, Comp_Income, CashFlow, stock_id)
    score_table = pd.concat([score_table, df] , axis = 1)
    

