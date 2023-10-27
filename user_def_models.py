#自定义模块检验用同花顺数据
from xgtrader.stock_data_ths import stock_data_ths
from xgtrader.bond_cov_data_ths import bond_cov_data_ths
from xgtrader.etf_fund_data_ths import etf_fund_data_ths
from xgtrader.xgtrader import xgtrader
from xgtrader.unification_data_ths import unification_data_ths
from trader_tool.ths_limitup_data import ths_limitup_data
from trader_tool.dfcf_rq import popularity
from trader_tool.ths_rq import ths_rq
from trader_tool import jsl_data
from trader_tool.dfcf_theme import dfcf_theme
from trader_tool.stock_upper_data import stock_upper_data
from trader_tool.analysis_models import analysis_models
from trader_tool.shape_analysis import shape_analysis
from trader_tool.trader_frame import trader_frame
import time
import json
import pywencai
import pandas as pd
from trader_tool.stock_em import stock_em
#可转债趋势策略
from trader_models.bond_cov_rend_strategy.bond_cov_rend_strategy import bond_cov_rend_strategy
#涨停板策略
from trader_models.limit_trading_strategy.limit_trading_strategy import limit_trading_strategy
#etf趋势策略
from trader_models.etf_trend_strategy.etf_trend_strategy import etf_trend_strategy
#可转债人气策略
from trader_models.bond_cov_popularity_strategy.bond_cov_popularity_strategy import bond_cov_popularity_strategy
#股票人气排行策略
from trader_models.stock_sentiment_strategy.stock_sentiment_strategy import stock_sentiment_strategy
class user_def_models:
    def __init__(self,trader_tool='ths',exe='C:/同花顺软件/同花顺/xiadan.exe',tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qq='1029762153@qq.com',open_set='否',qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',qmt_account_type='STOCK'):
        '''
        自定义模型
        '''
        self.exe=exe
        self.tesseract_cmd=tesseract_cmd
        self.qq=qq
        self.trader_tool=trader_tool
        self.open_set=open_set
        self.qmt_path=qmt_path
        self.qmt_account=qmt_account
        self.qmt_account_type=qmt_account_type
        self.data=unification_data_ths()
        order_frame=trader_frame(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        self.trader=order_frame.get_trader_frame()
    def connect(self):
        self.trader.connect()
    def get_wencai_buy_data(self):
        '''
        获取买入数据
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        word=text['问财买入条件']
        df=pywencai.get(loop=True,question=word)
        df.to_excel(r'{}.xlsx'.format(word))
        df['证券代码']=df['code']
        df['交易状态']='未买'
        df.to_excel(r'买入股票\买入股票.xlsx')
        return df
    def get_wencai_sell_data(self):
        '''
        获取问财买入数据
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        word=text['问财卖出条件']
        df=pywencai.get(loop=True,question=word)
        df['证券代码']=df['证券代码'].apply(lambda x:str(x)[:6])
        hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        def select_stock(x):
            if x in df['证券代码'].to_list():
                return '是'
            else:
                return '不是'
        if hold_stock.shape[0]>0:
            hold_stock['证券代码']=hold_stock['证券代码'].apply(lambda x:str(x)[:6])
            hold_stock['选择']=hold_stock['证券代码'].apply(select_stock)
            hold_stock=hold_stock[hold_stock['选择']=='是']
            hold_stock['交易状态']='未卖'
            hold_stock.to_excel(r'卖出股票\卖出股票.xlsx')
        else:
            print('没有持股数据')
    def get_dfcf_zh_buy_stock(self):
        '''
        获取东方财富自选股组合买入股票
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        cookie=text['东方财富cookie']
        appkey=text['东方财富appkey']
        name=text['东方财富买入自选股模块名称']
        models=stock_em(Cookie=cookie,appkey=appkey)
        df=models.get_all_zh_code(name=name)
        df['证券代码']=df['security']
        df['交易状态']='未买'
        df.to_excel(r'买入股票\买入股票.xlsx')
    def get_dfcf_zh_sell_stock(self):
        '''
        获取东方财富自选股组合卖出股票
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        cookie=text['东方财富cookie']
        appkey=text['东方财富appkey']
        name=text['东方财富卖出自选股模块名称']
        models=stock_em(Cookie=cookie,appkey=appkey)
        df=models.get_all_zh_code(name=name)
        df['证券代码']=df['security']
        df['交易状态']='未卖'
        df.to_excel(r'卖出股票\卖出股票.xlsx')
    def run_bond_cov_rend_strategy(self):
        '''
        运行可转债趋势轮动策略
        '''
        models=bond_cov_rend_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        models.updata_all_data()
    def run_limit_trading_strategy(self):
        '''
        运行涨停板交易策略
        '''
        models=limit_trading_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        models.updata_all_data()
    def run_etf_trend_strategy(self):
        '''
        运行etf趋势策略
        '''
        models=etf_trend_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        models.updata_all_data()
    def run_bond_cov_popularity_strategy(self):
        '''
        运行可转债人气交易策略
        '''
        models=bond_cov_popularity_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        models.updata_all_data()
    def run_stock_sentiment_strategy(self):
        '''
        运行股票人气排行策略
        '''
        models=stock_sentiment_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        models.update_all_data()
    def run_tdx_yj_trader_func(self):
        '''
        运行通达信警告交易函数
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        path=text['通达信警告保存路径']
        columns=text['通达信警告列名称']
        buy_con=text['买入警告条件']
        sell_con=text['卖出警告条件']
        buy_df=pd.read_excel(r'买入股票\买入股票.xlsx',dtype='object')
        if '未买' not in buy_df.columns.tolist():
            buy_df['交易状态']=='未买'
        else:
            pass
        buy_df=buy_df[buy_df['交易状态']=='未买']
        try:
            del buy_df['Unnamed: 0']
        except:
            pass
        sell_df=pd.read_excel(r'卖出股票\卖出股票.xlsx',dtype='object')
        if '未卖' not in sell_df.columns.tolist():
            sell_df['交易状态']='未卖'
        else:
            pass 
        sell_df=sell_df[sell_df['交易状态']=='未卖']
        try:
            del sell_df['Unnamed: 0']
        except:
            pass
        with open(r'{}'.format(path),'r+') as f:
            com=f.readlines()
        result_list=[]
        for i in com:
            result_list.append(i.strip().split())
        tdx_df=pd.DataFrame(result_list)
        if tdx_df.shape[0]>0:
            tdx_df.columns=columns
            def select_buy_sell(x):
                if buy_con in x:
                    return '未买'
                elif sell_con in x:
                    return '未卖'
                else:
                    return '未知交易状态'
            tdx_df['交易状态']=tdx_df['买卖条件'].apply(select_buy_sell)
            tdx_df_buy=tdx_df[tdx_df['交易状态']=='未买']
            tdx_df_sell=tdx_df[tdx_df['交易状态']=='未卖']
            try:
                if len(buy_df.columns.tolist()) !=len(tdx_df_buy.columns.tolist()):
                    buy_df=pd.DataFrame()
                else:
                    buy_df=buy_df
                buy_df=pd.concat([buy_df,tdx_df_buy],ignore_index=True)
                buy_df=buy_df.drop_duplicates(subset=['证券代码'], keep='last')
                buy_df.to_excel(r'买入股票\买入股票.xlsx')
            except:
                if len(buy_df.columns.tolist()) !=len(tdx_df_buy.columns.tolist()):
                    buy_df=pd.DataFrame()
                else:
                    buy_df=buy_df
                buy_df=pd.concat([buy_df,tdx_df_buy],ignore_index=True)
                buy_df=buy_df.drop_duplicates(subset=['证券代码'], keep='last')
                buy_df.to_excel(r'买入股票\买入股票.xlsx')
            try:
                if len(sell_df.columns.tolist()) !=len(tdx_df_sell.columns.tolist()):
                    sell_df=pd.DataFrame()
                else:
                    sell_df=sell_df
                sell_df=pd.concat([sell_df,tdx_df_sell],ignore_index=True)
                sell_df=sell_df.drop_duplicates(subset=['证券代码'], keep='last')
                sell_df.to_excel(r'卖出股票\卖出股票.xlsx')
            except:
                if len(sell_df.columns.tolist()) !=len(tdx_df_sell.columns.tolist()):
                    sell_df=pd.DataFrame()
                else:
                    sell_df=sell_df
                sell_df=pd.concat([sell_df,tdx_df_sell],ignore_index=True)
                sell_df=sell_df.drop_duplicates(subset=['证券代码'], keep='last')
                sell_df.to_excel(r'卖出股票\卖出股票.xlsx')
            print(buy_df,sell_df)
        else:
            print('通达信没有警告数据')
if __name__=='__main__':
    with open('分析配置.json','r+',encoding='utf-8') as f:
        com=f.read()
    text=json.loads(com)
    trader_tool=text['交易系统']
    exe=text['同花顺下单路径']
    tesseract_cmd=text['识别软件安装位置']
    qq=text['发送qq']
    test=text['测试']
    open_set=text['是否开启特殊证券公司交易设置']
    qmt_path=text['qmt路径']
    qmt_account=text['qmt账户']
    qmt_account_type=text['qmt账户类型']
    models=user_def_models(trader_tool=trader_tool,exe=exe,tesseract_cmd=tesseract_cmd,qq=qq,
                           open_set=open_set,qmt_path=qmt_path,qmt_account=qmt_account,
                           qmt_account_type=qmt_account_type)
    func=text['自定义函数'][-1]
    runc_func='models.{}()'.format(func)
    eval(runc_func)
