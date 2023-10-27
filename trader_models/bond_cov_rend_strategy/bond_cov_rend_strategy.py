from trader_tool.stock_data import stock_data
from trader_tool.bond_cov_data import bond_cov_data
from trader_tool.shape_analysis import shape_analysis
from trader_tool.analysis_models import analysis_models
import pandas as pd
from trader_tool.ths_rq import ths_rq
from tqdm import tqdm
import numpy as np
import json
from  trader_tool import jsl_data
from qmt_trader.qmt_trader_ths import qmt_trader_ths
from xgtrader.xgtrader import xgtrader
import os
class bond_cov_rend_strategy:
    def __init__(self,trader_tool='ths',exe='C:/同花顺软件/同花顺/xiadan.exe',tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qq='1029762153@qq.com',open_set='否',qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',qmt_account_type='STOCK'):
        '''
        分析模型
        '''
        self.exe=exe
        self.tesseract_cmd=tesseract_cmd
        self.qq=qq
        self.trader_tool=trader_tool
        self.open_set=open_set
        self.qmt_path=qmt_path
        self.qmt_account=qmt_account
        self.qmt_account_type=qmt_account_type
        if trader_tool=='ths':
            self.trader=xgtrader(exe=self.exe,tesseract_cmd=self.tesseract_cmd,open_set=open_set)
        else:
            self.trader=qmt_trader_ths(path=qmt_path,account=qmt_account,account_type=qmt_account_type)
        self.stock_data=stock_data()
        self.bond_cov_data=bond_cov_data()
        self.ths_rq=ths_rq()
        self.path=os.path.dirname(os.path.abspath(__file__))
    def save_position(self):
        '''
        保存持股数据
        '''
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        self.trader.connect()
        df=self.trader.position()
        def select_bond_cov(x):
            '''
            选择可转债
            '''
            if x[:3] in ['110','113','123','127','128','111','118'] or x[:2] in ['11','12']:
                return '是'
            else:
                return '不是'
        try:
            if df==False:
                print('获取持股失败')
        except:
            if df.shape[0]>0:
                df['选择']=df['证券代码'].apply(select_bond_cov)
                try:
                    df['持股天数']=df['持股天数'].replace('--',1)
                except:
                    df['持股天数']=1
                df1=df[df['选择']=='是']
                df1=df1[df1['可用余额']>=10]
                df1.to_excel(r'持股数据\持股数据.xlsx')
                return df1
            else:
                df=pd.DataFrame()
                df['账号类型']=None
                df['资金账号']=None
                df['证券代码']=None
                df['股票余额']=None
                df['可用余额']=None
                df['成本价']=None
                df['市值']=None
                df['选择']=None
                df['持股天数']=None
                df['交易状态']=None
                df['明细']=None
                df['证券名称']=None
                df['冻结数量']=None
                df['市价']=None	
                df['盈亏']=None
                df['盈亏比(%)']=None
                df['当日买入']=None	
                df['当日卖出']=None
                df.to_excel(r'持股数据\持股数据.xlsx')
                return df

    def save_position_1(self):
        '''
        保存持股数据
        '''
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        self.trader.connect()
        df=self.trader.position()
        def select_bond_cov(x):
            '''
            选择可转债
            '''
            if x[:3] in ['110','113','123','127','128','111'] or x[:2] in ['11','12']:
                return '是'
            else:
                return '不是'
        try:
            if df==False:
                print('获取持股失败')
        except:
            if df.shape[0]>0:
                df['选择']=df['证券代码'].apply(select_bond_cov)
                try:
                    df['持股天数']=df['持股天数'].replace('--',1)
                except:
                    df['持股天数']=1
                df1=df[df['选择']=='是']
                #df1=df1[df1['可用余额']>=10]
                df1.to_excel(r'持股数据\持股数据.xlsx')
                return df1
            else:
                df=pd.DataFrame()
                df=pd.DataFrame()
                df['账号类型']=None
                df['资金账号']=None
                df['证券代码']=None
                df['股票余额']=None
                df['可用余额']=None
                df['成本价']=None
                df['市值']=None
                df['选择']=None
                df['持股天数']=None
                df['交易状态']=None
                df['明细']=None
                df['证券名称']=None
                df['冻结数量']=None
                df['市价']=None	
                df['盈亏']=None
                df['盈亏比(%)']=None
                df['当日买入']=None	
                df['当日卖出']=None
                df.to_excel(r'持股数据\持股数据.xlsx')
                return df
    def select_bond_cov(self,x):
        '''
        选择证券代码
        '''
        if x[:3] in ['110','113','123','127','128','111'] or x[:2] in ['11','12']:
            return '是'
        else:
            return '不是'
    def save_balance(self):
        '''
        保持账户数据
        '''
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        self.trader.connect()
        df=self.trader.balance()
        df.to_excel(r'账户数据\账户数据.xlsx')
        return df
    def get_all_jsl_data(self):
        '''
        获取可转债全部数据
        '''
        print('获取可转债全部数据')
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        max_yjl=text['可转债溢价率上限']
        min_yjl=text['可转债溢价率下限']
        user=text['集思录账户']
        password=text['集思录密码']
        df=jsl_data.get_all_cov_bond_data(jsl_user=user,jsl_password=password)
        df['代码']=df['证券代码'].tolist()
    
        df1=df[df['转股溢价率']<=max_yjl]
        df2=df1[df1['转股溢价率']>=min_yjl]
        #df2.to_excel(r'目前溢价率可转债\目前溢价率可转债.xlsx')
        return df2
        
    def select_cov_bond_data(self):
        '''
        选择股票
        '''
        print('选择可转债')
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        max_price=text['价格上限']
        min_price=text['价格下限']
        max_spot_zdf=text['实时涨跌幅上限']
        min_spot_zdf=text['实时涨跌幅下限']
        max_yjl=text['可转债溢价率上限']
        min_yjl=text['可转债溢价率下限']
        #df=pd.read_excel(r'目前溢价率可转债\目前溢价率可转债.xlsx',dtype='object')
        df=self.get_all_jsl_data()
        try:
            del df['Unnamed: 0']
        except:
            pass
        df1=df[df['价格']<=max_price]
        df2=df1[df1['价格']>=min_price]
        df3=df2[df2['涨跌幅']<=max_spot_zdf]
        df4=df3[df3['涨跌幅']>=min_spot_zdf]
        df5=df4[df4['转股溢价率']<=max_yjl]
        df6=df5[df5['转股溢价率']>=min_yjl]
        #df6.to_excel(r'选择可转债\选择可转债.xlsx')
        return df6
    def mean_line_models(self,df):
        '''
        均线模型
        趋势模型
        5，10，20，30，60
        '''
        df=df
        #df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,start=start_date,end=end_date,limit=1000000000)
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
            score+=25
        if mean_10>mean_20:
            score+=25
        if mean_20>mean_30:
            score+=25
        if mean_30>mean_60:
            score+=25
        return score
    def get_return_ananlysis(self,df='',n=5):
        '''
        收益率分析
        '''
        #涨跌幅
        df1=df
        prices=df1[-n:]['close']
        zdf= ((prices.iloc[-1] / prices.iloc[0]) - 1)*100
        #最大回撤
        max_down_result=((prices / prices.expanding(min_periods=1).max()).min() - 1)*100
        #累计收益】
        return zdf,max_down_result
    def get_cov_bond_shape_analysis(self):
        '''
        可转债形态分析
        '''
        print('可转债形态分析')
        #df=pd.read_excel(r'选择可转债\选择可转债.xlsx',dtype='object')
        df=self.select_cov_bond_data()
        try:
            del df['Unnamed: 0']
        except:
            pass
        stock_list=df['证券代码'].tolist()
        over_lining=[]
        mean_line=[]
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            hist_df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock)
            models=shape_analysis(df=hist_df)
            try:
                over=models.get_over_lining_sell()
                over_lining.append(over)
                #均线分析
                line=models.get_down_mean_line_sell()
                mean_line.append(line)
            except:
                over_lining.append(None)
                mean_line.append(None)

        df['上影线']=over_lining
        df['跌破均线']=mean_line
        df1=df[df['上影线']=='不是']
        df1=df1[df1['跌破均线']=='不是']
        #df1.to_excel(r'选择可转债\选择可转债.xlsx')
        return df1
    def get_stock_mean_line_retuen_analysis(self):
        '''
        可转债均线收益分析
        '''
        print('可转债均线收益分析')
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        n=text['最近N天']
        max_retuen=text['最近N天最大收益率']
        min_return=text['最近N天最小收益率']
        max_down=text['最近N天最大回撤']
        min_secore=text['均线最低分数']
        mean_sorce_list=[]
        zdf_list=[]
        max_down_list=[]
        #df=pd.read_excel(r'选择可转债\选择可转债.xlsx',dtype='object')
        df=self.get_cov_bond_shape_analysis()
        try:
            df['Unnamed: 0']
        except:
            pass
        stock_list=df['证券代码'].tolist()
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            try:
                df1=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,start='19990101',end='20500101',limit=10000000)
                sorce=self.mean_line_models(df=df1)
                zdf,down=self.get_return_ananlysis(df=df1,n=n)
                mean_sorce_list.append(sorce)
                zdf_list.append(zdf)
                max_down_list.append(down)
            except:
                mean_sorce_list.append(None)
                zdf_list.append(None)
                max_down_list.append(None)
        df['均线得分']=mean_sorce_list
        df['最近{}天收益'.format(n)]=zdf_list
        df['最近天{}最大回撤'.format(n)]=max_down_list
        #df.to_excel(r'分析原始数据\分析原始数据.xlsx')
        df1=df[df['均线得分']>=min_secore]
        df2=df1[df1['最近{}天收益'.format(n)]>=min_return]
        df3=df2[df2['最近{}天收益'.format(n)]<=max_retuen]
        df4=df3[df3['最近天{}最大回撤'.format(n)]>=max_down]
        #df4.to_excel(r'交易股票池\交易股票池.xlsx')
        return df4
    def get_stock_daily_return_analysis(self):
        '''
        正股今天收益率分析
        '''
        print('正股今天收益率分析')
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        max_zdf=text['正股涨跌幅上限']
        min_zdf=text['正股涨跌幅下限']
        #df=pd.read_excel(r'交易股票池\交易股票池.xlsx',dtype='object')
        df=self.get_stock_mean_line_retuen_analysis()
        try:
            del df['Unnamed: 0']
        except:
            pass
        stock_list=df['证券代码'].tolist()
        zdf_list=[]
        stock_code_list=[]
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            try:
                stock=self.bond_cov_data.get_cov_bond_spot(stock=stock)['证券代码']
                stock_spot=self.stock_data.get_stock_spot_data(stock=stock)['涨跌幅']
                zdf_list.append(stock_spot)
                stock_code_list.append(stock)
            except:
                zdf_list.append(None)
                stock_code_list.append(None)
        df['正股代码']=stock_code_list
        df['正股涨跌幅']=zdf_list
        df1=df[df['正股涨跌幅']<=max_zdf]
        df2=df1[df1['正股涨跌幅']>=min_zdf]
        #df2.to_excel(r'交易股票池\交易股票池.xlsx')
        return df2
    def get_del_qzsh_data(self):
        '''
        剔除强制赎回
        '''
        print('剔除强制赎回')
        with open('{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        del_select=text['是否剔除强制赎回']
        n=text['距离强制赎回天数']
        df=self.bond_cov_data.bank_cov_qz()
        del_list=[]
        for i in range(1,n+1):
            n_text='至少还需{}天'.format(i)
            del_list.append(n_text)
        del_list.append('临近到期')
        del_list.append('已满足强赎条件')
        del_list.append('是否剔除强制赎回')
        text_n=''
        for select_text in del_list:
            text_n+='"{}" in x or '.format(select_text)
        text_n=text_n[:-3]
        if del_select=='是':
            df1=df
            def select_bond_cov(x):
                '''
                选择可转债
                '''
                if eval(text_n):
                    return '是'
                else:
                    return '不是'
            df1['选择']=df1['cell.redeem_count'].apply(select_bond_cov)
            df2=df1[df1['选择']=='是']
            #df2.to_excel(r'强制赎回\强制赎回.xlsx')
            #trader_stock=pd.read_excel(r'交易股票池\交易股票池.xlsx',dtype='object')
            trader_stock=self.get_stock_daily_return_analysis()
            def select_trader_stock(x):
                '''
                选择交易股票池
                '''
                if x not in df2['cell.bond_id'].tolist():
                    return '不是'
                else:
                    return '是'
            trader_stock['强制赎回']=trader_stock['证券代码'].apply(select_trader_stock)
            trader_stock=trader_stock[trader_stock['强制赎回']=='不是']
            #trader_stock.to_excel(r'交易股票池\交易股票池.xlsx')
            return df2,trader_stock
        else:
            df.to_excel(r'非强制赎回\非强制赎回.xlsx')
            return df
    def get_del_buy_sell_data(self):
        '''
        处理交易股票池买入股票
        '''
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        limit=text['持股限制']
        df=self.save_position()
        df1=df[df['可用余额']>=10]
        hold_stock_list=df['证券代码'].tolist()
        stats,trader_df=self.get_del_qzsh_data()
        def select_data(stock):
            if stock in hold_stock_list:
                num=df1[df1['证券代码']==stock]['可用余额'].tolist()[-1]
                if float(num)>=float(limit):
                    return '持股超过限制'
                else:
                    return '持股不足'
            else:
                return '没有持股'
        trader_df['持股检查']=trader_df['证券代码'].apply(select_data)
        trader_df=trader_df[trader_df['持股检查'] !='持股超过限制']
        trader_df=trader_df.sort_values(by='均线得分',ascending=False)
        #trader_df.to_excel(r'交易股票池\交易股票池.xlsx')
        return trader_df
    def get_buy_sell_stock(self):
        '''
        获取买卖数据
        '''
        with open('{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        buy_num=text['买入前N']
        hold_limit=text['持有限制']
        df=self.save_position()
        hold_min_score=text['持有均线最低分']
        df1=df[df['可用余额']>=10]
        hold_stock_list=df['证券代码'].tolist()
        def select_stock(x):
            '''
            选择股票
            '''
            if x in hold_stock_list:
                return '持股不足'
            else:
                return "持股不足"
        try:
            del df['Unnamed: 0']
        except:
            pass
        #trader_df=pd.read_excel(r'交易股票池\交易股票池.xlsx',dtype='object')
        trader_df=self.get_del_buy_sell_data()
        print('交易股票池*******************')
        print(trader_df)
        trader_df['选择']=trader_df['证券代码'].apply(select_stock)
        trader_df=trader_df[trader_df['选择']=='持股不足']
        select=text['是否开启持股周期']
        hold_daily_limit=text['持股持股周期天数']
        try:
            del trader_df['Unnamed: 0']
        except:
            pass
        if df1.shape[0]>0:
            #卖出列表
            sell_list=[]
            #持股列表
            hold_stock_list=df['证券代码'].tolist()
            #排名列表
            if select=='是':
                hold_daily=df[df['证券代码']==stock]['持股天数'].tolist()[-1]
                if hold_daily>=hold_daily_limit:
                    sell_list.append(stock)
                else:
                    print('人气排行目前持股 {} 没有大于{}'.format(hold_daily,hold_daily_limit))
            else:
                print('不启动持股限制')
            #对持有的可转债做均线分析
            for stock in hold_stock_list:
                try:
                    bond_data=self.bond_cov_data.get_cov_bond_hist_data(stock=stock)
                    socre=self.mean_line_models(df=bond_data)
                    if socre<hold_min_score:
                        if select=='是':
                            hold_daily=df[df['证券代码']==stock]['持股天数'].tolist()[-1]
                            if hold_daily>=hold_daily_limit:
                                sell_list.append(stock)
                            else:
                                print('持有的可转债做均线分析目前持股 {} 没有大于{}'.format(hold_daily,hold_daily_limit))
                        else:
                            sell_list.append(stock)
                            print('{} 目前{}分数 不符合最低分数{}'.format(stock,socre,hold_min_score))
                except:
                    pass
                else:
                    pass
            #跌破均线分析
            for stock in hold_stock_list:
                    hist_df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock)
                    models=shape_analysis(df=hist_df)
                    mean_line=models.get_down_mean_line_sell()
                    if mean_line=='是':
                        if select=='是':
                            hold_daily=df[df['证券代码']==stock]['持股天数'].tolist()[-1]
                            if hold_daily>=hold_daily_limit:
                                sell_list.append(stock)
                            else:
                                print('跌破均线分析目前持股 {} 没有大于{}'.format(hold_daily,hold_daily_limit))
                        else:
                            print('{}跌破均线'.format(stock))
                            sell_list.append(stock)
                    else:
                        pass
            sell_df=pd.DataFrame()
            sell_df['证券代码']=sell_list
            sell_df['交易状态']='未卖'
            #剔除新股申购
            sell_df['选择']=sell_df['证券代码'].apply(self.select_bond_cov)
            sell_df=sell_df[sell_df['选择']=='是']
            if sell_df.shape[0]>0:
                print('卖出可转债*****************')
                print(sell_df)
                sell_df.to_excel(r'卖出股票\卖出股票.xlsx')
            else:
                print('没有卖出的可转债')
                sell_df['证券代码']=[None]
                sell_df['交易状态']=[None]
                sell_df.to_excel(r'卖出股票\卖出股票.xlsx')
            hold_num=df1.shape[0]
            if hold_num>0:
                av_buy_num=hold_limit-hold_num
                av_buy_num=av_buy_num+sell_df.shape[0]
                buy_df=trader_df[:av_buy_num]
            else:
                buy_df=trader_df[:buy_num]
            buy_df['交易状态']='未买'
            print('买入可转债*****************')
            print(buy_df)
            buy_df.to_excel(r'买入股票\买入股票.xlsx')
            return buy_df
        else:
            buy_df=trader_df[:hold_limit]
            buy_df['交易状态']='未买'
            print('买入可转债*****************')
            print(buy_df)
            buy_df.to_excel(r'买入股票\买入股票.xlsx')
            return buy_df
    def updata_all_data(self):
        '''
        更新全部数据
        '''
        with open(r'{}/可转债趋势策略交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        hold_select=text['是否开启持股周期']
        #self.save_position()
        #self.save_balance()
        #self.get_all_jsl_data()
        #self.select_cov_bond_data()
        #self.get_cov_bond_shape_analysis()
        #self.get_stock_mean_line_retuen_analysis()
        #self.get_stock_daily_return_analysis()
        #self.get_del_qzsh_data()
        #self.get_del_buy_sell_data()
        self.get_buy_sell_stock()
    def updata_all_data_1(self):
        '''
        更新全部数据
        '''
        self.save_position_1()
        self.save_balance()
        self.get_all_jsl_data()
        self.select_cov_bond_data()
        self.get_cov_bond_shape_analysis()
        self.get_stock_mean_line_retuen_analysis()
        self.get_stock_daily_return_analysis()
        self.get_del_qzsh_data()
        self.get_del_buy_sell_data()
        self.get_buy_sell_stock()
    def cacal_zig_data(self,stock='123018',x=0.005):
        '''
        计算之字转向
        x=5%之子转向
        :return:
        '''
        ZIG_STATE_START = 0
        ZIG_STATE_RISE = 1
        ZIG_STATE_FALL = 2
        df=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        df['价格']=df['价格'].astype(float)
        # print(list(df["close"]))
        df = df[::-1]
        df = df.reset_index(drop=True)
        # df = df.iloc[-100:]
        x = x
        k = df["价格"]
        d = df["时间"]
        peer_i = 0
        candidate_i = None
        scan_i = 0
        peers = [0]
        z = np.zeros(len(k))
        state = ZIG_STATE_START
        while True:
            scan_i += 1
            if scan_i == len(k) - 1:
                # 扫描到尾部
                if candidate_i is None:
                    peer_i = scan_i
                    peers.append(peer_i)
                else:
                    if state == ZIG_STATE_RISE:
                        if k[scan_i] >= k[candidate_i]:
                            peer_i = scan_i
                            peers.append(peer_i)
                        else:
                            peer_i = candidate_i
                            peers.append(peer_i)
                            peer_i = scan_i
                            peers.append(peer_i)
                    elif state == ZIG_STATE_FALL:
                        if k[scan_i] <= k[candidate_i]:
                            peer_i = scan_i
                            peers.append(peer_i)
                        else:
                            peer_i = candidate_i
                            peers.append(peer_i)
                            peer_i = scan_i
                            peers.append(peer_i)
                break
            if state == ZIG_STATE_START:
                if k[scan_i] >= k[peer_i] * (1 + x):
                    candidate_i = scan_i
                    state = ZIG_STATE_RISE
                elif k[scan_i] <= k[peer_i] * (1 - x):
                    candidate_i = scan_i
                    state = ZIG_STATE_FALL
            elif state == ZIG_STATE_RISE:
                if k[scan_i] >= k[candidate_i]:
                    candidate_i = scan_i
                elif k[scan_i] <= k[candidate_i] * (1 - x):
                    peer_i = candidate_i
                    peers.append(peer_i)
                    state = ZIG_STATE_FALL
                    candidate_i = scan_i
            elif state == ZIG_STATE_FALL:
                if k[scan_i] <= k[candidate_i]:
                    candidate_i = scan_i
                elif k[scan_i] >= k[candidate_i] * (1 + x):
                    peer_i = candidate_i
                    peers.append(peer_i)
                    state = ZIG_STATE_RISE
                    candidate_i = scan_i
        for i in range(len(peers) - 1):
            peer_start_i = peers[i]
            peer_end_i = peers[i + 1]
            start_value = k[peer_start_i]
            end_value = k[peer_end_i]
            a = (end_value - start_value) / (peer_end_i - peer_start_i)  # 斜率
            for j in range(peer_end_i - peer_start_i + 1):
                z[j + peer_start_i] = start_value + a * j
        df['结果']=z
        #前天
        line_1=df['结果'].shift(2)
        #昨天
        line_2=df['结果'].shift(1)
        #今天
        line_3=df['结果'].shift(0)
        result=[]
        for x,y,z in zip(line_1,line_2,line_3):
            if x<y and y>z:
                result.append('sell')
            elif x>y and y<z:
                result.append('buy')
            else:
                result.append(None)
        df['买卖点']=result
        df1=df.sort_index(ascending=False,ignore_index=True)
        return df1
    def get_mean_line_trader_analysis(self,stock='128036',window=30):
        '''
        均线交易分析模型，
        数据为3秒一次
        60 3分钟
        '''
        import numpy as np
        df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,data_type='1')
        df['close']=df['close'].astype(float)
        df['mean_5']=df['close'].rolling(5).mean()
        x1=df['mean_1'].shift(2)
        x2=df['mean_1'].shift(1)
        x3=df['mean_1'].shift(0)
        df['买点']=np.logical_and(x1<x2,x3>x2)
        df['卖点']=np.logical_and(x1>x2,x3<x2)
        print(df[df['买点']==True])
        buy_spot=df['买点'].tolist()[-1]
        sell_spot=df['卖点'].tolist()[-1]
        if buy_spot==True:
            return 'buy'
        else:
            return False
        if sell_spot==True:
            return 'sell'
        else:
            return False
    def get_macd_trader_analysis(self,stock='111007'):
        '''
        macd
        '''
        pass
    def get_mi_pulse_trader_analysis(self,n=10,x1=1,x2=-2,stock='111007',select='是',h='9',mi='3300',num=1.5):
        '''
        分钟脉冲分析     
        '''
        df=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        date=df['时间'].tolist()[-1]
        if select=='是':
            now_date=float(h+mi)
            if float(date)<=now_date:
                x1=x1*num
            else:
                x1=x1
        else:
            x1=x1
        n=20*n
        zdf_list=df['涨跌幅'].tolist()[-n:]
        zdf=zdf_list[-1]-zdf_list[1]
        print(stock,zdf)
        if zdf>=x1:
            return 'sell'
        elif zdf<=x2:
            return 'buy'
        else:
            return False
    def get_dynamic_trader_analysis(self,daily=5,mi=10,x=0.3,x1=-0.3,stock='128041'):
        '''
        动态分钟脉冲
        '''
        df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock)
        df['平均振幅']=df['振幅'].rolling(daily).mean()
        zdf=df['平均振幅'].tolist()[-1]
        zdf=abs(zdf)
        #实时交易数据
        df1=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        n=20*mi
        zdf_list=df1['涨跌幅'].tolist()[-n:]
        spot_zdf=zdf_list[-1]-zdf_list[0]
        if spot_zdf>=0:
            sell_zdf=zdf*x
            if spot_zdf>sell_zdf:
                return 'sell'
            else:
                return False
        elif spot_zdf<0:
            buy_zdf=zdf*x1
            if spot_zdf<=buy_zdf:
                return 'buy'
            else:
                return False
        else:
            return False
    def get_hour_pulse_trader_analysis(self,hour=1,x1=5,x2=-3,stock=''):
        '''
        小时趋势
        '''
        df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,data_type='1')
        df['累计涨跌幅']=df['涨跌幅'].cumsum()
        zdf_list=df['累计涨跌幅'].tolist()[-hour:]
        zdf=zdf_list[-1]-zdf_list[0]
        if zdf>=x1:
            return 'sell'
        elif zdf<=x2:
            return 'buy'
        else:
            return False
    def surge_and_fall_overfall_rebound(self,stock='123018',min_return=7,max_down=-1,max_df=-5,ft_return=3):
        '''
        冲高回落--超跌反弹
        min_return冲高的涨跌幅
        max_down最大的回撤
        #超跌反弹
        max_df最大跌幅
        ft_return反弹收益
        '''
        df=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        #最大涨跌幅
        max_return_ratio=max(df['涨跌幅'].tolist())
        #现在的涨跌幅
        now_return_ratio=df['涨跌幅'].tolist()[-1]
        #目前的收益回撤
        max_down_ratio=now_return_ratio-max_return_ratio
        if max_return_ratio>min_return and max_down_ratio<=max_down:
            text='冲高回落，股票{} 最大涨跌幅{} 现在的涨跌幅{} 收益回撤{}'.format(stock,max_return_ratio,now_return_ratio,max_down_ratio)
            return '冲高回落',True,text
        else:
            text='不符合冲高回落，股票{} 最大涨跌幅{} 现在的涨跌幅{} 收益回撤{}'.format(stock,max_return_ratio,now_return_ratio,max_down_ratio)
            return '冲高回落',False,text
        #最小涨跌幅
        min_return_ratio=min(df['涨跌幅'].tolist())
        #反弹收益
        ft_return_ratio=now_return_ratio-min_return_ratio
        if min_return_ratio<max_df and ft_return_ratio >ft_return:
            text='超跌反弹，股票{} 最大跌幅{} 现在的涨跌幅{} 收益反弹{}'.format(stock, min_return_ratio,now_return_ratio,ft_return_ratio)
            return '超跌反弹',True,text
        else:
            text='不符合超跌反弹，股票{} 最大跌幅{} 现在的涨跌幅{} 收益反弹{}'.format(stock, min_return_ratio,now_return_ratio,ft_return_ratio)
            return "超跌反弹",False,text
    def get_trader_mean_line_analysis(self,stock='128041',n=5,mean_line=20):
        '''
        盘中参考均线分析
        '''
        df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,data_type='5',limit=100000000)
        df['mean_line']=df['close'].rolling(mean_line).mean()
        open_price=df['open'].tolist()[-1]
        close_price=df['close'].tolist()[-1]
        mean_price=df['mean_line'].tolist()[-1]
        if open_price <mean_price and close_price>mean_price:
            return 'buy'
        elif open_price>mean_price and close_price<mean_price:
            return 'sell'
        else:
            return False
    def get_rising_speed_analysis(self,n=5,stock='110070'):
        '''
        涨速分析
        '''
        import matplotlib.pyplot as plt
        df=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        df['实时涨跌幅'][-200:].plot()
        plt.show()
    def get_creat_cov_bond_grid(self,daily=5,n=6,df='',entiy_select='0.5',bs=2,spot_zdf=2):
        '''
        生成网格交易 从上到下一次为1，2，3，4，5网格
        '''
        #df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock)
        df=df
        #因为数据是实时数据，题材今天的数据
        df1=df[-daily+1:-1]
        mean_zf=df1['振幅'].mean()
        #单元格
        entiy=mean_zf/n
        if entiy<=entiy_select:
            entiy=entiy*bs
        else:
            entiy=entiy
        data_dict={}
        for i in range(1,int(n/2)+1):
            data_dict['{}'.format(i)]=entiy*(abs((i-1)-int(n/2)))
        for i in range(int(n/2)+1,n+1):
            data_dict['{}'.format(i)]=entiy*(int(n/2)-i)
        for j in range(1,n):
            if spot_zdf>data_dict['1']:
                index='up'
            elif spot_zdf<data_dict[str(n)]:
                index='down'
            elif spot_zdf<=data_dict[str(j)] and spot_zdf>=data_dict[str(j+1)]:
                index=j
        #print(data_dict)
        return data_dict,entiy,index
    def get_grid_analysis(self,stock='110074',daily=5,n=6,time_size=600,buy_sell_dot=0.75,
    stop=True,stop_line=-3,entiy_select='0.5',bs=2):
        '''
        网格分析数据3秒一次数据
        daily最近N天，振幅为平均值为上下网格
        n网格线多少
        time_size时间窗口 20是一分钟
        buy_sell_dot 到到目标网格的分位数
        stop开启网格止损
        stop_line=-3止损线
        '''
        from datetime import datetime
        now_time=datetime.now()
        hist_df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock)
        df=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        #print(df)
        zdf_list=df['涨跌幅'].tolist()[-time_size:]
        #前N分钟的涨跌幅
        pre_zdf=zdf_list[0]
        #现在的涨跌幅
        now_zdf=zdf_list[-1]
        if now_zdf<=stop_line and stop==True:
            text='{} {} 现在的涨跌幅 {}达到止损线全部卖出'.format(now_time,stock,now_zdf)
            return 'all_sell',text
        else:
            #前面涨跌幅在的格子
            pre_dict,entiy,pre_index=self.get_creat_cov_bond_grid(daily=daily,n=n,df=hist_df,spot_zdf=pre_zdf,entiy_select=entiy_select,bs=bs)
            #现在涨跌幅在的格子
            now_dict,entiy,now_index=self.get_creat_cov_bond_grid(daily=daily,n=n,df=hist_df,spot_zdf=now_zdf,entiy_select=entiy_select,bs=bs)
            #现在的可转债涨跌幅大于上边线自动添加一个卖出网格
            if now_index in ['up'] and now_zdf>=pre_dict[str(1)]+(entiy*buy_sell_dot):
                text='卖出 时间{} 可转债{} 突破上边线而且达到{}分位数'.format(now_time,stock,buy_sell_dot)
                return 'sell_up',text
            elif now_index=='down' or pre_index=='down':
                text='卖出 时间{} 控制住{}跌破下边线'.format(now_time,stock)
                return 'sell_down',text
            elif now_index in ['up'] or pre_index=='up':
                text='卖出 时间{} 可转债{}突破上边线'.format(now_time,stock)
                return 'sell',text
            #向上多单元格跳动，比如从3单元格直接跳动到1 单元格
            elif (pre_index-now_index)>=2:
                text='卖出 向上多单元格跳动 {} {} 从{}单元格跳到{}单元格'.format(now_time,stock,pre_index,now_index)
                return 'sell',text
            #向下多单元格跳动，比如从1单元格直接跳动到3 单元格
            elif (pre_index-now_index)<=-2:
                text='买入 向下多单元格跳动 {} {} 从{}单元格跳到{}单元格'.format(now_time,stock,pre_index,now_index)
                return 'buy',text
            #一个一个单元格跳动
            #在同一个单元格不操作
            elif now_index==pre_index:
                text='{} 可转债{} 现在的涨跌幅{} 在同一个网格布交易 目前的网格{}'.format(now_time,stock,now_zdf,now_index)
                return False,text
            else:
                #买入的操作
                #可转债从上一个格子进入下一个格子同时现在的涨跌幅在新格子的1-buy_sell_dot的分位数位置
                if pre_index <now_index:
                    if now_zdf<=pre_dict[str(now_index)]-(entiy*buy_sell_dot):
                        text='买入 {} {} 从{}单元格跌到{}单元格 达到{}单元格的{}位置'.format(now_time,
                        stock,pre_index,now_index,now_index,buy_sell_dot)
                        return 'buy',text
                    else:
                        text='{} {} 从{}单元格跌到{}单元格目前没有达到{}买入点'.format(now_time,
                        stock,pre_index,now_index,buy_sell_dot)
                        return False,text
                #卖出操作
                elif pre_index >now_index:
                    if now_zdf>=pre_dict[str(pre_index)]+(entiy*buy_sell_dot):
                        text='卖出 {} {} 从{}单元格上涨{}单元格 达到{}单元格 的{}位置'.format(now_time,
                        stock,pre_index,now_index,now_index,buy_sell_dot)
                        return 'sell',text
                    else:
                        text='{} {} 从{}单元格上涨{}单元格目前没有达到{}卖出点'.format(now_time,
                        stock,pre_index,now_index,buy_sell_dot)
                        return False,text 
                else:
                    return False,0   
    def hold_bond_cov_exchange(self,stock='127080',trader_type='sell'):
        '''
        可转债上影线
        '''      
        df=pd.read_excel(r'持股数据\持股数据.xlsx')
        try:
            del df['Unnamed: 0']
        except:
            pass
        stock_list=df['代码'].tolist()
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            models=shape_analysis(stock=stock)
            print(models.get_over_lining_sell())