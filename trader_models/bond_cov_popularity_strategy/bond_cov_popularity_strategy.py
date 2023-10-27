from trader_tool.stock_data import stock_data
from trader_tool.bond_cov_data import bond_cov_data
from trader_tool.shape_analysis import shape_analysis
from trader_tool.etf_fund_data import etf_fund_data
from trader_tool.stock_upper_data import stock_upper_data
from trader_tool.ths_limitup_data import ths_limitup_data
from trader_tool.trader_frame import trader_frame
import pandas as pd
from trader_tool.ths_rq import ths_rq
from tqdm import tqdm
import numpy as np
import json
from  trader_tool import jsl_data
import os
class bond_cov_popularity_strategy:
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
        order_frame=trader_frame(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        self.trader=order_frame.get_trader_frame()
        self.stock_data=stock_data()
        self.bond_cov_data=bond_cov_data()
        self.etf_fund_data=etf_fund_data()
        self.ths_rq=ths_rq()
        self.shape_analysis=shape_analysis()
        self.stock_upper_data=stock_upper_data()
        self.ths_limitup_data=ths_limitup_data()
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.trader.connect()
    def save_position(self):
        '''
        保存持股数据
        '''
        with open(r'{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        exe=text['同花顺下单路径']
        df=trader.position()
        def select_bond_cov(x):
            '''
            选择可转债
            '''
            if x[:3] in ['110','113','123','127','128','111']:
                return '是'
            else:
                return '不是'
        try:
            if df==False:
                print('获取持股失败')
        except:
            if df.shape[0]>0:
                df['选择']=df['证券代码'].apply(select_bond_cov)
                df1=df[df['选择']=='是']
                #df1=df1[df1['可用余额']>=10]
                df1.to_excel(r'持股数据\持股数据.xlsx')
                return df1
            else:
                print('没有持股')
    def save_position(self):
        '''
        保存持股数据
        '''
        with open(r'{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        df=self.trader.position()
        def select_bond_cov(x):
            '''
            选择可转债
            '''
            if x[:3] in ['110','113','123','127','128','111']:
                return '是'
            else:
                return '不是'
        try:
            if df==False:
                print('获取持股失败')
        except:
            if df.shape[0]>0:
                df['选择']=df['证券代码'].apply(select_bond_cov)
                df1=df[df['选择']=='是']
                df1=df1[df1['可用余额']>=10]
                df1.to_excel(r'持股数据\持股数据.xlsx')
                return df1
            else:
                print('没有持股')
    def save_position_1(self):
        '''
        保存持股数据
        '''
        with open(r'{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        df=self.trader.position()
        def select_bond_cov(x):
            '''
            选择可转债
            '''
            if x[:3] in ['110','113','123','127','128','111']:
                return '是'
            else:
                return '不是'
        try:
            if df==False:
                print('获取持股失败')
        except:
            if df.shape[0]>0:
                df['选择']=df['证券代码'].apply(select_bond_cov)
                df1=df[df['选择']=='是']
                #df1=df1[df1['可用余额']>=10]
                df1.to_excel(r'持有可转债\持有可转债.xlsx')
                df1.to_excel(r'持股数据\持股数据.xlsx')
                return df1
            else:
                print('没有持股')
    def select_bond_cov(self,x):
        '''
        选择证券代码
        '''
        if x[:3] in ['110','113','123','127','128','111']:
            return '是'
        else:
            return '不是'
    def save_balance(self):
        '''
        保持账户数据
        '''
        with open(r'{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        df=self.trader.balance()
        df.to_excel(r'账户数据\账户数据.xlsx')
        return df
    def get_ths_rq_data(self):
        '''
        获取同花顺人气数据
        '''
        df=self.ths_rq.get_cov_bond_rot_rank()
        df.to_excel(r'{}\同花顺人气原始数据\同花顺人气原始数据.xlsx'.format(self.path))
        return df
    def get_concact_data(self):
        '''
        获取合并数据
        '''
        df=pd.read_excel(r'{}\同花顺人气原始数据\同花顺人气原始数据.xlsx'.format(self.path),dtype='object')
        try:
            del df['Unnamed: 0']
        except:
            pass
        stock_list=df['代码'].tolist()
        price_list=[]
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            try:
                df1=self.bond_cov_data.get_cov_bond_spot(stock=stock)
                price=df1['最新价']
                price_list.append(price)
            except:
                price_list.append(None)
        df['最新价']=price_list
        df.to_excel(r'{}\合并数据\合并数据.xlsx'.format(self.path))
        return df
    def select_cov_bond_data(self):
        '''
        选择股票
        '''
        with open(r'{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        max_price=text['价格上限']
        min_price=text['价格下限']
        max_spot_zdf=text['实时涨跌幅上限']
        min_spot_zdf=text['实时涨跌幅下限']
        df=pd.read_excel(r'{}\合并数据\合并数据.xlsx'.format(self.path),dtype='object')
        try:
            del df['Unnamed: 0']
        except:
            pass
        df1=df[df['最新价']<=max_price]
        df2=df1[df1['最新价']>=min_price]
        df3=df2[df2['涨跌幅']<=max_spot_zdf]
        df4=df3[df3['涨跌幅']>=min_spot_zdf]
        df4.to_excel(r'{}\选择可转债\选择可转债.xlsx'.format(self.path))
        return df4
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
    def get_stock_mean_line_retuen_analysis(self):
        '''
        可转债均线收益分析
        '''
        with open(r'{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
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
        df=pd.read_excel(r'{}\选择可转债\选择可转债.xlsx'.format(self.path),dtype='object')
        try:
            df['Unnamed: 0']
        except:
            pass
        stock_list=df['代码'].tolist()
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
                max_down.append(None)
        df['均线得分']=mean_sorce_list
        df['最近{}天收益'.format(n)]=zdf_list
        df['最近天{}最大回撤'.format(n)]=max_down_list
        df.to_excel(r'{}\分析原始数据\分析原始数据.xlsx'.format(self.path))
        df1=df[df['均线得分']>=min_secore]
        df2=df1[df1['最近{}天收益'.format(n)]>=min_return]
        df3=df2[df2['最近{}天收益'.format(n)]<=max_retuen]
        df4=df3[df3['最近天{}最大回撤'.format(n)]>=max_down]
        df4.to_excel(r'{}\交易股票池\交易股票池.xlsx'.format(self.path))
        return df4
    def get_stock_daily_return_analysis(self):
        '''
        正股今天收益率分析
        '''
        with open(r'{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        max_zdf=text['正股涨跌幅上限']
        min_zdf=text['正股涨跌幅下限']
        df=pd.read_excel(r'{}\交易股票池\交易股票池.xlsx'.format(self.path),dtype='object')
        try:
            del df['Unnamed: 0']
        except:
            pass
        stock_list=df['代码'].tolist()
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
        df2.to_excel(r'{}\交易股票池\交易股票池.xlsx'.format(self.path))
        return df2
    def get_del_qzsh_data(self):
        '''
        剔除强制赎回
        '''
        with open('{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        del_select=text['是否剔除强制赎回']
        n=text['距离强制赎回天数']
        df=self.bond_cov_data.bank_cov_qz()
        df.to_excel(r'{}\强制赎回\强制赎回.xlsx'.format(self.path))
        if del_select=='是':
            df1=df[df['cell.redeem_real_days']<=n]
            def select_bond_cov(x):
                '''
                选择可转债
                '''
                if '临近到期' in x or '已满足强赎条件' in x:
                    return '是'
                else:
                    return '不是'
            df1['选择']=df1['cell.redeem_count'].apply(select_bond_cov)
            df2=df1[df1['选择']=='不是']
            df2.to_excel(r'{}\非强制赎回\非强制赎回.xlsx'.format(self.path))
            return df2
        else:
            df.to_excel(r'{}\非强制赎回\非强制赎回.xlsx'.format(self.path))
            return df
    def get_buy_sell_stock(self):
        '''
        获取买卖数据
        '''
        with open('{}/可转债人气模型交易配置.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        buy_num=text['买入前N']
        hold_limit=text['持有限制']
        hold_rank=text['持有人气排行前N']
        df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
        df1=df[df['可用余额']>=10]
        hold_stock_list=df['证券代码'].tolist()
        def select_stock(x):
            '''
            选择股票
            '''
            if x in hold_stock_list:
                return '持股'
            else:
                return "持股不足"
        try:
            del df['Unnamed: 0']
        except:
            pass
        trader_df=pd.read_excel(r'{}\交易股票池\交易股票池.xlsx'.format(self.path),dtype='object')
        print('交易股票池*********************************')
        print(trader_df)
        trader_df['选择']=trader_df['代码'].apply(select_stock)
        trader_df=trader_df[trader_df['选择']=='持股不足']
        try:
            del trader_df['Unnamed: 0']
        except:
            pass
        rank_data=pd.read_excel(r'{}\同花顺人气原始数据\同花顺人气原始数据.xlsx'.format(self.path),dtype='object')
        try:
            del rank_data['Unnamed: 0']
        except:
            pass
        if df1.shape[0]>0:
            hold_rank_data=rank_data[:hold_rank]
            #卖出列表
            sell_list=[]
            #持股列表
            hold_stock_list=df['证券代码'].tolist()
            #排名列表
            rank_stock_list=hold_rank_data['代码'].tolist()
            for stock in hold_stock_list:
                if stock in rank_stock_list:
                    pass
                else:
                    sell_list.append(stock)
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
                av_buy_num+sell_df.shape[0]
                buy_df=trader_df[:av_buy_num]
            else:
                buy_df=trader_df[:buy_num]
            buy_df['交易状态']='未买'
            buy_df['证券代码']=buy_df['代码']
            print('买入可转债*************')
            print(buy_df)
            buy_df.to_excel(r'买入股票\买入股票.xlsx')
            return buy_df
        else:
            buy_df=trader_df[:buy_num]
            buy_df['证券代码']=buy_df['代码']
            buy_df['交易状态']='未买'
            print('买入可转债*************')
            print(buy_df)
            buy_df.to_excel(r'买入股票\买入股票.xlsx')
            return buy_df
    def updata_all_data(self):
        '''
        更新全部数据
        '''
        self.save_position()
        self.save_balance()
        self.get_ths_rq_data()
        self.get_concact_data()
        self.select_cov_bond_data()
        self.get_stock_mean_line_retuen_analysis()
        self.get_stock_daily_return_analysis()
        self.get_del_qzsh_data()
        self.get_buy_sell_stock()
    def updata_all_data_1(self):
        '''
        更新全部数据
        '''
        self.save_position_1()
        self.save_balance()
        self.get_ths_rq_data()
        self.get_concact_data()
        self.select_cov_bond_data()
        self.get_stock_mean_line_retuen_analysis()
        self.get_stock_daily_return_analysis()
        self.get_del_qzsh_data()
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
    def get_mi_pulse_trader_analysis(self,n=10,x1=1,x2=-2,stock='111007'):
        '''
        分钟脉冲分析     
        '''
        df=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        n=20*n
        zdf_list=df['涨跌幅'].tolist()[-n:]
        zdf=zdf_list[-1]-zdf_list[0]
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
        #实时交易数据
        df1=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        n=20*mi
        zdf_list=df1['涨跌幅'].tolist()[-n:]
        spot_zdf=zdf_list[-1]-zdf_list[0]
        sell_zdf=zdf*x
        buy_zdf=zdf*x1
        if spot_zdf>sell_zdf:
            return 'sell'
        elif spot_zdf<=buy_zdf:
            return 'buy'
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