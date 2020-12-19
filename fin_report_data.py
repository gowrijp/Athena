import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date

# To scrape Market Watch and return financial data like EPS, EPS Growth, Net Income, and EBITDA.
def get_financial_report(ticker):

    # try:
    urlfinancials = 'https://www.marketwatch.com/investing/stock/'+ticker+'/financials'
    urlbalancesheet = 'https://www.marketwatch.com/investing/stock/'+ticker+'/financials/balance-sheet'

    text_soup_financials = BeautifulSoup(requests.get(urlfinancials).text,"html") #read in
    text_soup_balancesheet = BeautifulSoup(requests.get(urlbalancesheet).text,"html") #read in


    # build lists for Income statement
    titlesfinancials = text_soup_financials.findAll('td', {'class': 'overflow__cell fixed--column'})
    epslist=[]
    netincomelist = []
    longtermdebtlist = []
    interestexpenselist = []
    ebitdalist= []

    for title in titlesfinancials:
        if 'EPS (Basic)' in title.text.splitlines()[1]:
            epslist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'overflow__cell'}) if td.text])
        if 'Net Income' in title.text.splitlines()[1]:
            netincomelist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'overflow__cell'}) if td.text])
        if 'Interest Expense' in title.text.splitlines()[1]:
            interestexpenselist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'overflow__cell'}) if td.text])
        if 'EBITDA' in title.text.splitlines()[1]:
            ebitdalist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'overflow__cell'}) if td.text])


    # find the table headers for the Balance sheet
    titlesbalancesheet = text_soup_balancesheet.findAll('td', {'class': 'overflow__cell fixed--column'})
    equitylist=[]
    for title in titlesbalancesheet:
        if 'Total Shareholders\' Equity' in title.text.splitlines()[1]:
            equitylist.append( [td.text for td in title.findNextSiblings(attrs={'class': 'overflow__cell'}) if td.text])
        if 'Long-Term Debt' in title.text.splitlines()[1]:
            longtermdebtlist.append( [td.text for td in title.findNextSiblings(attrs={'class': 'overflow__cell'}) if td.text])

    #get the data from the income statement lists
    #use helper function get_element
    eps = epslist[0][0:5]
    epsGrowth = epslist[1][0:5]
    netIncome = netincomelist[0][0:5]
    shareholderEquity = equitylist[0][0:5]
    roa = equitylist[1][0:5]

    longtermDebt = longtermdebtlist[0][0:5]
    interestExpense =  interestexpenselist[0][0:5]
    ebitda = ebitdalist[0][0:5]

    # load all the data into dataframe
    fin_df= pd.DataFrame({'eps': eps,'eps Growth': epsGrowth,'net Income': netIncome,'shareholder Equity': shareholderEquity,'roa':
                  roa,'longterm Debt': longtermDebt,'interest Expense': interestExpense,'ebitda': ebitda},index=range(date.today().year-5,date.today().year))

    fin_df.reset_index(inplace=True)

    return fin_df



'''def get_element(list,element):
    try:
        return list[element]
    except:
        return '-'
'''
