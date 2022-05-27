# -*- coding: utf-8 -*-
"""
Created on Wed May 25 08:40:44 2022

@author: 111036
"""

import requests
import pandas as pd
import time
import numpy as np


def FinancialStatements(to_year, mkt, num):
    BalanceSheet=pd.DataFrame()
    ComprehensiveIncome=pd.DataFrame()
    CashFlow=pd.DataFrame()
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    
    
    for year in range(int(to_year)-2, int(to_year)+1):
        print(year)
        # balance sheet
        url = 'https://mops.twse.com.tw/mops/web/t163sb05'
        
        payloads = {'encodeURIComponent': '1',
                    'step': '1',
                    'firstin': '1',
                    'off': '1',
                    'isQuery': 'Y',
                    'TYPEK': mkt,
                    'year': year,
                    'season': '01'}
           
        res = requests.post(url, headers=headers, data=payloads)
        df = pd.read_html(res.text)[num]
        df['Season'] = str(year)+'-'+payloads['season']
        df = df.set_index('Season')
        BalanceSheet = pd.concat([df, BalanceSheet])
        time.sleep(3)
        
        # Comprehensive Income
        url = 'https://mops.twse.com.tw/mops/web/t163sb04'
           
        res = requests.post(url, headers=headers, data=payloads)
        df = pd.read_html(res.text)[num]
        df['Season'] = str(year)+'-'+payloads['season']
        df = df.set_index('Season')
        ComprehensiveIncome = pd.concat([df, ComprehensiveIncome])
        time.sleep(3)
        
        # Cash Flow Statement
        url = 'https://mops.twse.com.tw/mops/web/t163sb20'      
           
        res = requests.post(url, headers=headers, data=payloads)
        df = pd.read_html(res.text)[num]
        df['Season'] = str(year)+'-'+payloads['season']
        df = df.set_index('Season')
        CashFlow = pd.concat([df, CashFlow])
        time.sleep(3)
  
    return BalanceSheet, ComprehensiveIncome, CashFlow

def F_score(BalanceSheet, ComprehensiveIncome, CashFlow, stock_id):
    
    BalanceSheet = BalanceSheet[BalanceSheet['公司代號']==stock_id]
    BalanceSheet = BalanceSheet.drop('公司名稱', axis=1)
    BalanceSheet = BalanceSheet.replace('--', 0)
    BalanceSheet = BalanceSheet.fillna(0)
    BalanceSheet = BalanceSheet.astype(int)

    ComprehensiveIncome = ComprehensiveIncome[ComprehensiveIncome['公司代號']==stock_id]
    ComprehensiveIncome = ComprehensiveIncome.drop('公司名稱', axis=1)
    ComprehensiveIncome = ComprehensiveIncome.replace('--', 0)
    ComprehensiveIncome = ComprehensiveIncome.astype(int)

    CashFlow = CashFlow[CashFlow['公司代號']==stock_id]
    CashFlow = CashFlow.drop('公司名稱', axis=1)
    CashFlow = CashFlow.replace('--', 0)
    CashFlow = CashFlow.astype(int)
    
    dic = dict()
    
    ## Profitability
    ### 1. ROA
    ROA = ComprehensiveIncome.loc['111-01', '本期淨利（淨損）'] * 2 / (BalanceSheet.loc['111-01', '資產總計'] + BalanceSheet.loc['110-01', '資產總計'])
    if ROA > 0:
        dic['F_ROA'] = 1
    else:
        dic['F_ROA'] = 0
    
    ### 2. CFO
    CFO = CashFlow.loc['111-01', '營業活動之淨現金流入（流出）']
    if CFO > 0:
        dic['F_CFO'] = 1
    else:
        dic['F_CFO'] = 0
    ### 3. D_ROA
    ROA_lastYear =  ComprehensiveIncome.loc['110-01', '本期淨利（淨損）'] * 2 / (BalanceSheet.loc['110-01', '資產總計'] + BalanceSheet.loc['109-01', '資產總計'])
    if ROA > ROA_lastYear:
        dic['F_D_ROA'] = 1
    else:
        dic['F_D_ROA'] = 0
    ### 4. ACCRUAL
    if CFO > ComprehensiveIncome.loc['111-01', '本期淨利（淨損）']:
        dic['F_ACCRUAL'] = 1
    else:
        dic['F_ACCRUAL'] = 0
    
    ## Leverage, Liquidity, source of fund
    ### 1. Leverage
    LTD_ratio = BalanceSheet.loc['111-01', '非流動負債'] / BalanceSheet.loc['111-01', '資產總計']
    LTD_ratio_lastYear = BalanceSheet.loc['110-01', '非流動負債'] / BalanceSheet.loc['110-01', '資產總計']
    if LTD_ratio < LTD_ratio_lastYear:
        dic['F_D_LEVER'] = 1
    else:
        dic['F_D_LEVER'] = 0
    ### 2. Liquidity
    Curr_ratio = BalanceSheet.loc['111-01', '流動資產'] / BalanceSheet.loc['111-01', '流動負債']
    Curr_ratio_lastYear = BalanceSheet.loc['110-01', '流動資產'] / BalanceSheet.loc['110-01', '流動負債']
    if Curr_ratio > Curr_ratio_lastYear:
        dic['F_D_LIQUID'] = 1
    else:
        dic['F_D_LIQUID'] = 0
    ### 3. source of fund
    if BalanceSheet.loc['111-01', '預收股款（權益項下）之約當發行股數（單位：股）'] <= BalanceSheet.loc['110-01', '預收股款（權益項下）之約當發行股數（單位：股）']:
        dic['F_EQ_OFFER'] = 1
    else:
        dic['F_EQ_OFFER'] = 0
    ## Operating efficiency
    ### 1. Gross Margin
    Gross_Margin = ComprehensiveIncome.loc['111-01', '營業毛利（毛損）'] / ComprehensiveIncome.loc['111-01', '營業收入']
    Gross_Margin_lastYear = ComprehensiveIncome.loc['110-01', '營業毛利（毛損）'] / ComprehensiveIncome.loc['110-01', '營業收入']
    if Gross_Margin > Gross_Margin_lastYear:
        dic['F_D_MARGIN'] = 1
    else:
        dic['F_D_MARGIN'] = 0
    ### 2. Asset TurnOver
    Asset_TO = ComprehensiveIncome.loc['111-01', '營業收入'] / BalanceSheet.loc['111-01', '資產總計']
    Asset_TO_lastYear = ComprehensiveIncome.loc['110-01', '營業收入'] / BalanceSheet.loc['110-01', '資產總計']
    if Asset_TO > Asset_TO_lastYear:
        dic['F_D_TURN'] = 1
    else:
        dic['F_D_TURN'] = 0
    
    dic['F_Score'] = sum(dic.values())
    
    df = pd.DataFrame(list(dic.items()), columns=['Title', str(stock_id)])
    df = df.set_index('Title')
    print(CFO)
    return df

stock_ids_OTC = [3498, 8064, 6234, 5443, 6125, 1595, 5536, 6613, 3455, 5489, 6667]
stock_ids_TWSE = [2464, 6438, 3583, 6277, 3535, 4770, 2360]

BalanceSheet_OTC, ComprehensiveIncome_OTC, CashFlow_OTC = FinancialStatements('111', 'otc', 11)
BalanceSheet_TWSE, ComprehensiveIncome_TWSE, CashFlow_TWSE = FinancialStatements('111', 'sii', 12)

OTC_df = pd.DataFrame()
TWSE_df = pd.DataFrame()

stock_ids_OTC = [3498]

for stock_id in stock_ids_OTC:
    df = F_score(BalanceSheet_OTC, ComprehensiveIncome_OTC, CashFlow_OTC, stock_id)
    OTC_df = pd.concat([OTC_df,df], axis=1)

for stock_id in stock_ids_TWSE:
    df = F_score(BalanceSheet_TWSE, ComprehensiveIncome_TWSE, CashFlow_TWSE, stock_id)
    TWSE_df = pd.concat([TWSE_df,df], axis=1)

data = pd.concat([OTC_df, TWSE_df], axis=1)
data['mean'] = data.mean(axis=1)
data.to_excel('C:/Users/111036/Desktop/Case_Study/F_Score_Table.xlsx')