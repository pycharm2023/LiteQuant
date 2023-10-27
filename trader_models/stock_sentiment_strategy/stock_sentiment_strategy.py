from trader_tool.stock_data import stock_data
from trader_tool.bond_cov_data import bond_cov_data
from trader_tool.shape_analysis import shape_analysis
from trader_tool.etf_fund_data import etf_fund_data
from trader_tool.stock_upper_data import stock_upper_data
from trader_tool.ths_limitup_data import ths_limitup_data
from trader_tool.trader_frame import trader_frame
import pandas as pd
from trader_tool.ths_rq import ths_rq
from trader_tool.dfcf_rq import popularity
from tqdm import tqdm
import numpy as np
import json
from  trader_tool import jsl_data
import os
#核心数据
class stock_sentiment_strategy:
    def __init__(self,trader_tool='ths',exe='C:/同花顺软件/同花顺/xiadan.exe',tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qq='1029762153@qq.com',open_set='否',qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',qmt_account_type='STOCK'):
        self.exe=exe
        self.tesseract_cmd=tesseract_cmd
        self.qq=qq
        self.trader_tool=trader_tool
        self.open_set=open_set
        self.qmt_path=qmt_path
        self.qmt_account=qmt_account
        self.qmt_account_type=qmt_account_type
        order_frame=trader_frame(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        self.trader=order_frame.get_trader_frame()
        self.data=stock_data()
        self.bond_cov_data=bond_cov_data()
        self.etf_fund_data=etf_fund_data()
        self.ths_rq=ths_rq()
        self.popularity=popularity()
        self.shape_analysis=shape_analysis()
        self.stock_upper_data=stock_upper_data()
        self.ths_limitup_data=ths_limitup_data()
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.trader.connect()
    def stock_dict_data(self):
        '''
        股票字典
        '''
        df=self.data.stock_individual_fund_flow_rank()
        stock_dict=dict(zip(df['代码'].tolist(),df['名称'].tolist()))
        price_dict=dict(zip(df['代码'].tolist(),df['最新价'].tolist()))
        zdf_dict=dict(zip(df['代码'].tolist(),df['今日涨跌幅'].tolist()))
        return stock_dict,price_dict,zdf_dict
    def popularity_models(self,stock='601360',n=20,total_n=100):
        ''' 
        人气排行前20/自己研究前100
        模型20分,一个位置一分
        '''
        df=self.popularity.get_stock_popularity_rank_data()
        stock_list=df['代码'].tolist()[:total_n]
        if stock not in stock_list:
            score=0
        else:
            index=stock_list.index(stock)
            score=abs((total_n-index))*(n/total_n)
        return score
    def cash_models(self,stock='600111',n=10):
        '''
        资金模型
        10日资金
        20分
        '''
        df=self.data.stock_individual_fund_flow(stock=stock)[-n:]
        up_size=df[df['主力净流入净额']>=0].shape[0]
        down_size=df[df['主力净流入净额']<=0].shape[0]
        score=(up_size-down_size)*(20/n)
        return score
    def pct_change_models(self,stock='601858',start_date='20210101',end_date='20500101'):
        '''
        当日涨跌幅模型
        20分
        '''
        df=self.data.get_stock_hist_data_em(stock=stock,start_date=start_date,end_date=end_date)
        score=df['涨跌幅'].tolist()[-1]*2
        if score>=20:
            score=20
        else:
            score=score
        return score
    def mean_line_models(self,stock='600100',start_date='',end_date='20500101'):
        '''
        均线模型
        趋势模型
        5，10，20，30，60
        '''
        df=self.data.get_stock_hist_data_em(stock=stock,start_date=start_date,end_date=end_date)
        df1=pd.DataFrame()
        df1['date']=df['date']
        df1['5']=df['close'].rolling(window=5).mean()
        df1['10']=df['close'].rolling(window=10).mean()
        df1['20']=df['close'].rolling(window=20).mean()
        df1['30']=df['close'].rolling(window=30).mean()
        df1['60']=df['close'].rolling(window=60).mean()
        score=0
        #加分的情况
        mean_5=df1['5'].tolist()[-1]
        mean_10=df1['10'].tolist()[-1]
        mean_20=df1['20'].tolist()[-1]
        mean_30=df1['30'].tolist()[-1]
        mean_60=df1['60'].tolist()[-1]
        #相邻2个均线进行比较
        if mean_5>mean_10:
            score+=5
        if mean_10>mean_20:
            score+=5
        if mean_20>mean_30:
            score+=5
        if mean_30>mean_60:
            score+=5
        if mean_5<mean_10:
            score-=5
        if mean_10<mean_20:
            score-=5
        if mean_20<mean_30:
            score-=5
        if mean_30<mean_60:
            score-=5
        return score
    def stock_change_rate(self,stock='002292',start_date='',end_date='20500101'):
        '''
        涨跌幅情况变化
        上涨强度
        '''
        df=self.data.get_stock_hist_data_em(stock=stock,start_date=start_date,end_date=end_date)[-10:]
        up=df[df['涨跌幅']>0].shape[0]
        down=df[df['涨跌幅']<0].shape[0]
        score=up*2
        return score
    def total_sore_models(self,stock='600105',start_date='20210101',end_date='20500101'):
        '''
        总分模型
        '''
        popularity=self.popularity_models(stock=stock)
        cash=self.cash_models(stock=stock)
        change=self.pct_change_models(stock=stock,start_date=start_date,end_date=end_date)
        mean=self.mean_line_models(stock=stock,start_date=start_date,end_date=end_date)
        zd=self.stock_change_rate(stock=stock,start_date=start_date,end_date=end_date)
        total_score=popularity+cash+mean+change+zd
        stock_dict,price_dict,zdf_dict=self.stock_dict_data()
        data=pd.DataFrame()
        data['人气得分']=[popularity]
        data['资金得分']=[cash]
        data['涨跌幅得分']=[change]
        data['趋势得分']=[mean]
        data['上涨强度得分']=[zd]
        data['总分']=[total_score]
        data['证券代码']=[stock]
        data['股票名称']=[stock_dict[stock]]
        data['今日涨跌幅']=[zdf_dict[stock]]
        data['最新价']=[price_dict[stock]]
        return data
    def cacal_more_stock_score(self,stock_list=['600031','600111','600100'],start_date='20210101',end_date='20500101'):
        '''
        计算多个股票
        '''
        df=pd.DataFrame()
        for i in tqdm(range(len(stock_list))):
            try:
                df1=self.total_sore_models(stock=stock_list[i],start_date=start_date,end_date=end_date)
                df=pd.concat([df,df1],ignore_index=True)
            except:
                print('{}有问题'.format(i))
        df2=df.sort_values(by='总分',ascending=False,ignore_index=True)
        return df2
    def cacal_all_stock_popularity(self,n=10,start_date='20210101',end_date='20500101'):
        '''
        东方财富人气分析
        '''
        df=self.popularity.get_stock_popularity_rank_data()
        print(df)
        stock_list=df['代码'].tolist()[:n]
        result=self.cacal_more_stock_score(stock_list=stock_list,start_date=start_date,end_date=end_date)
        return result
    def add_dfcf_rq(self,):
        df=self.popularity.get_stock_popularity_rank_data()
        df.to_excel(r'{}/东方财富人气.xlsx'.format(self.path))
        code_list=df['代码'].tolist()
        stock=stock_em()
        stock.del_stock_zh_name(name='东方财富人气')
        stock.create_stock_zh(name='东方财富人气')
        for code in code_list:
            stock.add_stock_to_account(name='东方财富人气',stock=code)
        from datetime import datetime
        data=stock_data()
        trader_list=data.get_trader_date_list()
        now_date=''.join(trader_list[-1].split('-'))
        stock.all_zt_stock_add_to_account(date=now_date)
        return df
    def add_stock_to_account(stock_list=['600031','600111'],name='东方财富人气'):
        '''
        添加股票到组合
        '''
        stock=stock_em()
        stock.del_stock_zh_name(name=name)
        stock.create_stock_zh(name=name)
        for code in stock_list:
            stock.add_stock_to_account(name=name,stock=code)
    def get_analysis_result_1(self,):
        '''
        获取分析的结果1
        买入股票池
        '''
        with open('{}/股票人气交易模型交易配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        n=text['人气排行前N']
        price_max=text['价格上限']
        price_min=text['价格下限']
        zdf_max=text['今日涨跌幅上限']
        zdf_min=text['今日涨跌幅下限']
        del_cyb=text['是否剔除创业板']
        trade_rank=text['交易排行']
        score_min=text['分数下限']
        score_max=text['分数上限']
        df=self.cacal_all_stock_popularity(n=n)
        trader_date=self.data.get_trader_date_list()[-1]
        df.to_excel(r'{}\股票排名原始数据\股票排名原始数据.xlsx'.format(self.path))
        rank_data=df[:trade_rank]
        rank_data.to_excel(r'{}\排名股票池\排名股票池.xlsx'.format(self.path))
        def select_data(x):
            if x[:3]=='300':
                return '是'
            else:
                return '不是'
        if del_cyb=='是':
            df['选择']=df['证券代码'].apply(select_data)
            df1=df[df['选择']=='不是']
            df=df1
        else:
            df=df
        df['今日涨跌幅']=df['今日涨跌幅'].replace('-',0)
        df['最新价']=df['最新价'].replace('-',0)
        df1=df[df['今日涨跌幅']<=zdf_max]
        df2=df1[df1['今日涨跌幅']>=zdf_min]
        df3=df2[df2['最新价']<=price_max]
        df4=df3[df3['最新价']>=price_min]
        df5=df4[df4['总分']>=score_min]
        df6=df5[df5['总分']<=score_max]
        df6.to_excel(r'{}\交易股票数据池\交易股票数据池.xlsx'.format(self.path))
        return df6
    def get_analysis_result_2(self):
        '''
        获取分析的结果，比较激进的交易方式
        排序股票池
        '''
        with open('{}\股票人气交易模型交易配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        n=text['人气排行前N']
        price_max=text['价格上限']
        price_min=text['价格下限']
        zdf_max=text['今日涨跌幅上限']
        zdf_min=text['今日涨跌幅下限']
        del_cyb=text['是否剔除创业板']
        trade_rank=text['交易排行']
        df=self.cacal_all_stock_popularity(n=n)[:trade_rank]
        return df
    def anlaysis_acc_result(self):
        '''
        分析股票收益
        '''
        with open('{}/股票人气交易模型交易配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        n=text['人气排行前N']
        price_max=text['价格上限']
        price_min=text['价格下限']
        zdf_max=text['今日涨跌幅上限']
        zdf_min=text['今日涨跌幅下限']
        del_cyb=text['是否剔除创业板']
        trade_rank=text['交易排行']
        hold_limit=text['持股限制']
        fix_trade=text['指定买入']
        fix_amount=text['指定买入数量']
        one_limit=text['单一股票持股限制']
        n=text['最近N个交易日']
        acc_result=text['最近N个交易日涨跌幅']
        max_down=text['最大回撤']
        df=pd.read_excel(r'{}\交易股票数据池\交易股票数据池.xlsx'.format(self.path),dtype='object')
        stock_list=df['证券代码'].tolist()
        result_list=[]
        list1=[]
        list2=[]
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            df1=self.data.get_stock_hist_data_em(stock=stock)
            #涨跌幅
            prices=df1[-n:]['close']
            zdf= ((prices.iloc[-1] / prices.iloc[0]) - 1)*100
            #最大回撤
            max_down_result=((prices / prices.expanding(min_periods=1).max()).min() - 1)*100
            #累计收益】
            list1.append(zdf)
            #最大回撤
            list2.append(max_down_result)
            if zdf<=acc_result and max_down_result>=max_down:
                result_list.append(stock)
            else:
                pass
        all_df=pd.DataFrame()
        df['最近{}个交易日累计收入'.format(n)]=list1
        df['最近{}个交易最大回撤'.format(n)]=list2
        print(df)
        df.to_excel(r'{}\原始交易股票池\原始交易股票池.xlsx'.format(self.path))
        if len(result_list)>0:
            for stock in result_list:
                df2=df[df['证券代码']==stock]
                all_df=pd.concat([all_df,df2],ignore_index=True)
        all_df.to_excel(r'{}\交易股票数据池\交易股票数据池.xlsx'.format(self.path))
        return all_df
    def get_buy_sell_stock_by_rank(self):
        '''
        获取买入股票池
        '''
        with open('{}/股票人气交易模型交易配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        n=text['人气排行前N']
        price_max=text['价格上限']
        price_min=text['价格下限']
        zdf_max=text['今日涨跌幅上限']
        zdf_min=text['今日涨跌幅下限']
        del_cyb=text['是否剔除创业板']
        trade_rank=text['交易排行']
        hold_limit=text['持股限制']
        fix_trade=text['指定买入']
        fix_amount=text['指定买入数量']
        one_limit=text['单一股票持股限制']
        hold_min_sore=text['持有最低分']
        if fix_trade=='假':
            hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            if hold_stock.shape[0]>0:
                def select_data(x):
                    if x[0]=='6' or x[0]=='3' or x[0]=='0':
                        return "是"
                    else:
                        return "不是"
                hold_stock['选择']=hold_stock['证券代码'].apply(select_data)
                hold_stock=hold_stock[hold_stock['选择']=='是']
                select_stock=pd.read_excel(r'{}\股票排名原始数据\股票排名原始数据.xlsx'.format(self.path),dtype='object')[:trade_rank]
                #卖出的股票
                result=[]
                if hold_stock.shape[0]==0:
                    buy_amount=hold_limit
                else:
                    for stock in hold_stock['证券代码'].tolist():
                        if stock not in select_stock['证券代码'].tolist():
                            result.append(stock)
                        if True:
                            rank_data=pd.read_excel(r'{}\股票排名原始数据\股票排名原始数据.xlsx'.format(self.path),dtype='object')
                            try:
                                rank_data1=rank_data[rank_data['证券代码']==stock]
                                sroce=rank_data1['总分'].tolist()[0]
                                if sroce<=hold_min_sore:
                                    result.append(stock)
                                    print('{}不满足最低分数要求'.format(stock))
                                else:
                                    print('{}满足最低分数要求'.format(stock))
                            except:
                                result.append(stock)
                    sell_df=pd.DataFrame({'证券代码':result})
                    sell_df=sell_df.drop_duplicates()
                    sell_df['交易状态']='未卖'
                    sell_df.to_excel(r'卖出股票\卖出股票.xlsx')
                    now_amount=hold_stock.shape[0]-len(result)
                    if now_amount>=hold_limit:
                        buy_amount=len(result)
                    else:
                        buy_amount=hold_limit-now_amount
                    self.anlaysis_acc_result()
                    trader_stock=df=pd.read_excel(r'{}\交易股票数据池\交易股票数据池.xlsx'.format(self.path),dtype='object')
                    hold_stock_list=hold_stock['证券代码'].tolist()
                    trader_stock.index=trader_stock['证券代码']
                    for stock in hold_stock_list:
                        try:
                            trader_stock=trader_stock.drop(stock,axis=0)
                        except:
                            pass
                    buy_df=trader_stock[:buy_amount]
                    buy_df['交易状态']='未买'
                    buy_df.to_excel(r'买入股票\买入股票.xlsx')
                    print('买卖数据更新完成')
                    return buy_df,sell_df
            else:
                self.anlaysis_acc_result()
                trader_stock=df=pd.read_excel(r'{}\交易股票数据池\交易股票数据池.xlsx'.format(self.path),dtype='object')
                print('没有持股,启动默认买入')
                if fix_amount>0:
                    df=trader_stock[:fix_amount]
                else:
                    df=trader_stock[:fix_amount]
                df['交易状态']='未买'
                df.to_excel(r'买入股票\买入股票.xlsx')
                return df
        else:
            trader_stock=df=pd.read_excel(r'{}\交易股票数据池\交易股票数据池.xlsx'.format(self.path),dtype='object')
            if fix_amount>0:
                df=trader_stock[-fix_amount:]
            else:
                df=trader_stock[-fix_amount:]
            df['交易状态']='未买'
            df.to_excel(r'买入股票\买入股票.xlsx')
            return df
    def get_buy_sell_stock_by_score(self):
        '''
        获取买入股票池
        分散
        '''
        with open('{}/股票人气交易模型交易配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        n=text['人气排行前N']
        price_max=text['价格上限']
        price_min=text['价格下限']
        zdf_max=text['今日涨跌幅上限']
        zdf_min=text['今日涨跌幅下限']
        del_cyb=text['是否剔除创业板']
        score_max=text['分数上限']
        score_min=text['分数下限']
        trade_rank=text['交易排行']
        hold_limit=text['持股限制']
        hold_stock=pd.read_excel(r'{}\持股数据\持股数据.xlsx'.format(self.path),dtype='object')
        def select_data(x):
            if x[0]=='6' or x[0]=='3' or x[0]=='0':
                return "是"
            else:
                return "不是"
        hold_stock['选择']=hold_stock['证券代码'].apply(select_data)
        hold_stock=hold_stock[hold_stock['选择']=='是']
        select_stock=pd.read_excel(r'{}\股票排名原始数据\股票排名原始数据.xlsx'.format(self.path),dtype='object')[:trade_rank]
        #卖出的股票
        result=[]
        for stock in hold_stock['证券代码'].tolist():
            score=select_stock[select_stock['证券代码']==stock]
            if score.shape[0]==0:
                result.append(stock)
            else:
                score=score['总分'].tolist()[-1]
                if score>score_max or score<score_min:
                    result.append(stock)
                else:
                    pass
        sell_df=pd.DataFrame({'证券代码':result})
        sell_df.to_excel(r'卖出股票\卖出股票.xlsx')
        trader_stock=pd.read_excel(r'{}\股票排名原始数据\股票排名原始数据.xlsx'.format(self.path),dtype='object')
        buy_amount=hold_limit-len(result)
        #这个得看效果
        buy_df=trader_stock[-buy_amount:]
        buy_df.to_excel(r'买入股票\买入股票.xlsx')
        return buy_df,sell_df
    def update_all_data(self):
        '''
        跟新全部数据
        '''
        #市场情绪
        #maker_analysis.get_hist_zt_dt_data()
        with open(r'{}/股票人气交易模型交易配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        account=self.trader.balance()
        try:
            if account==False:
                pass
        except:
            account.to_excel(r'账户数据\账户数据.xlsx')
            print('账户数据保持成功')
        hold_stock=self.trader.position()
        try:
            if hold_data==False:
                pass
        except:
            if hold_stock.shape[0]>0 and hold_stock is not None:
                hold_data=hold_stock[hold_stock['股票余额']>=100]
                hold_data.index=hold_data['证券代码']
                hold_data.to_excel(r'持股数据\持股数据.xlsx')
            print('持股数据保持成功')
        self.get_analysis_result_1()
        self.get_buy_sell_stock_by_rank()
    def dynamic_stop_profit_stop_loss(stock='002174'):
        '''
        动态止盈止损
        '''
        df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        df1=df[df['证券代码']==stock]
        if df1.shape[0]==0:
            print('没有持股')
        else:
            df2=data.get_stock_set_bidding(stock=stock)
            cost_price=df1['参考成本价'].tolist()[-1]
            now_price=df2['成交价'].tolist()[-1]
        result_ratio=((now_price-cost_price)/cost_price)*100
        return result_ratio
    def adjust_hold_data(stock='603918',trader_type='sell',amount=100):
            '''
            模拟持股数据
            '''
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            del df['Unnamed: 0']
            df.index=df['证券代码']
            df1=df[df['证券代码']==stock]
            if df1.shape[0]>0:
                #可用余额
                available_balance=df1['可用余额'].tolist()[-1]
                #股票余额
                stock_balance=df1['股票余额'].tolist()[-1]
                if trader_type=='buy':
                    stock_balance+=float(amount)
                elif trader_type=='sell':
                    available_balance-=float(amount)
                    if available_balance<=0:
                        available_balance=0
                    stock_balance-=float(amount)
                    if stock_balance<=0:
                        stock_balance=0
                else:
                    pass
                df1['可用余额']=[available_balance]
                df1['股票余额']=[stock_balance]
                data=df.drop(stock,axis=0)
                data=pd.concat([data,df1],ignore_index=True)
                data.to_excel(r'持股数据\持股数据.xlsx')
                print('持股数据调整成功')
            else:
                print('{}没有持股'.format(stock))
    #adjust_hold_data(stock='002546',trader_type='sell',amount=200)
    #update_all_data_by_rank()
    #print(dynamic_stop_profit_stop_loss(stock='000977'))


        


        