from trader_tool.unification_data import unification_data
from trader_tool.trader_frame import trader_frame
from trader_tool.analysis_models import analysis_models
from trader_tool.shape_analysis import shape_analysis
from user_def_models import user_def_models
import pandas as pd
from tqdm import tqdm
import numpy as np
import time
import json
from datetime import datetime
import schedule
import yagmail
from trader_tool.base_func import base_func
class trader_strategy:
    def __init__(self,trader_tool='ths',exe='C:/同花顺软件/同花顺/xiadan.exe',tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qq='1029762153@qq.com',open_set='否',qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',qmt_account_type='STOCK'):
        '''
        参数配置
        '''
        self.exe=exe
        self.tesseract_cmd=tesseract_cmd
        self.qq=qq
        self.trader_tool=trader_tool
        self.open_set=open_set
        self.qmt_path=qmt_path
        self.qmt_account=qmt_account
        self.qmt_account_type=qmt_account_type
        self.user_def_models=user_def_models(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        order_frame=trader_frame(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        self.trader=order_frame.get_trader_frame()
        data=unification_data(trader_tool=self.trader_tool)
        self.data=data.get_unification_data()
        self.analysis_models=analysis_models()
        self.shape_analysis=shape_analysis()
        self.base_func=base_func()
    def connact(self):
        '''
        链接同花顺
        '''
        try:
            self.trader.connect()
            print('{}成功'.format(self.trader_tool))
            return True
        except:
            print('{}连接失败'.format(self.trader_tool))
            return False
    def adjust_hold_data(self,stock='603918',trader_type='sell',price=12,amount=100):
        '''
        模拟持股数据
        '''
        price=float(price)
        amount=float(amount)
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
                available_balance+=float(amount)
            elif trader_type=='sell':
                available_balance-=float(amount)
                stock_balance-=float(amount)
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
            df2=pd.DataFrame()
            df2['明细']=['0']
            df2['证券代码']=[stock]
            df2['证券名称']=['0']
            df2['股票余额']=[amount]
            df2['可用余额']=[amount]
            df2['冻结数量']=[0]
            df2['成本价']=[price]
            df2['市价']=[price]
            df2['盈亏']=[0]
            df2['盈亏比(%)']=[0]
            df2['市值']=[amount*price]
            df2['当日买入']=[0]
            df2['当日卖出']=[0]
            df2['交易市场']=[0]
            df2['持股天数']=[0]
            data=pd.concat([df,df2],ignore_index=True)
            data.to_excel(r'持股数据\持股数据.xlsx')
            print('持股数据调整成功')													
            print('{}没有持股'.format(stock))
    def adjust_account_cash(self,stock='128036',trader_type='buy',price=123,amount=10):
        '''
        调整账户资金
        '''
        price=float(price)
        amount=float(amount)
        df=pd.read_excel(r'账户数据\账户数据.xlsx',dtype='object')
        try:
            del df['Unnamed: 0']
        except:
            pass
        value=price*amount
        #可用余额
        av_user_cash=float(df['可用金额'].tolist()[-1])
        if trader_type=='buy':
            av_user_cash-=value
        elif trader_type=='sell':
            av_user_cash+=value
        else:
            av_user_cash=av_user_cash
        df['可用金额']=[av_user_cash]
        df.to_excel(r'账户数据\账户数据.xlsx')
        print('账户资金调整完成')
        return df
    def check_cov_bond_av_trader(self,stock='128106'):
        '''
        检查可转债是否可以交易
        '''
        with open(r'分析配置.json',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        del_stock=text['黑名单']
        if stock in del_stock:
            print('{}黑名单'.format(stock))
            return False
        else:
            return True
    def check_stock_is_av_buy(self,stock='128036',price='156.700',amount=10):
        '''
        检查是否可以买入
        '''
        price=float(price)
        amount=float(amount)
        with open(r'分析配置.json',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        hold_limit=text['持股限制']
        stats=self.trader.check_stock_is_av_buy(stock=stock,price=price,amount=amount,hold_limit=hold_limit)
        return stats
    def check_stock_is_av_sell(self,stock='128036',amount=10):
        '''
        检查是否可以卖出
        '''
        stats=self.trader.check_stock_is_av_sell(stock=stock,amount=amount)
        return stats
    def check_av_target_tarder(self,stock='600031',price=2.475,trader_type='buy'):
        '''
        检查目标交易
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        data_type=text['交易模式']
        value=text['固定交易资金']
        limit_value=text['持有金额限制']
        amount1=text['固定交易数量']
        limit_amount=text['持股限制']
        trader_type_1,buy_sell_amount,price=self.trader.check_av_target_trader(data_type=data_type,trader_type=trader_type,
                                           amount=amount1,limit_volume=limit_amount,
                value=value,limit_value=limit_value,stock=stock,price=price)
        return trader_type_1,buy_sell_amount,price
    def seed_emial_qq(self,text='交易完成'):

        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text1=json.loads(com)
        try:
            password=text1['qq掩码']
            seed_qq=text1['发送qq']
            yag = yagmail.SMTP(user='{}'.format(seed_qq), password=password, host='smtp.qq.com')
            m = text1['接收qq']
            text = text
            yag.send(to=m, contents=text, subject='邮件')
            print('邮箱发生成功')
        except:
            print('qq发送失败可能用的人多')
    def check_is_trader_date(self):
        '''
        检测是不是交易时间
        '''
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        #利用通用时间，不考虑中午不交易
        is_trader=''
        wo=loc.tm_wday
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        trader_time=text['交易时间段']
        start_date=text['交易开始时间']
        end_date=text['交易结束时间']
        if wo<=trader_time:
            if (tm_hour>=start_date) and (tm_hour<=end_date):
                is_trader=True
                return True
            else:
                is_trader=False
                return False
        else:
            print('周末')
            return False
    def check_is_trader_date_1(self):
        '''
        检测是不是交易时间
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        trader_time=text['交易时间段']
        start_date=text['交易开始时间']
        end_date=text['交易结束时间']
        start_mi=text['开始交易分钟']
        jhjj=text['是否参加集合竞价']
        if jhjj=='是':
            jhjj_time=15
        else:
            jhjj_time=30
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        wo=loc.tm_wday
        if wo<=trader_time:
            if tm_hour>=start_date and tm_hour<=end_date:
                if tm_hour==9 and tm_min<jhjj_time:
                    return False
                elif tm_min>=start_mi:
                    return True
                else:
                    return False
            else:
                return False    
        else:
            print('周末')
            return False
    def run_stock_trader_buy(self):
        '''
        运行交易策略 可转债,买入
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            stop=text['停止程序']
            max_zdf=text['买入时间的涨跌幅上限']
            min_zdf=text['买入时间的涨跌幅下限']
            data_source=text['买卖数据源']
            name=text['策略名称']
            trader_stats=[]
            if stop=='真':
                print('程序停止')
            else:
                if data_source=='默认':
                    df=pd.read_excel(r'买入股票\买入股票.xlsx',dtype='object')
                    try:
                        del df['Unnamed: 0']
                    except:
                        pass
                else:
                    df=pd.read_excel(r'自定义买入\自定义买入.xlsx',dtype='object')
                    try:
                        del df['Unnamed: 0']
                    except:
                        pass
                if df.shape[0]>0:
                    for stock,stats in zip(df['证券代码'].tolist(),df['交易状态'].tolist()):
                        if stats=='未买':
                            amount=text['固定交易数量']
                            #检查是不是强制赎回
                            try:
                                if self.check_cov_bond_av_trader(stock=stock):
                                    spot_data=self.data.get_spot_data(stock=stock)
                                    #价格
                                    price=spot_data['最新价']
                                    #实时涨跌幅
                                    zdf=spot_data['涨跌幅']
                                    #检查是不是可以买入
                                    if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                        if zdf<=max_zdf and zdf>=min_zdf:
                                            trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price)
                                            if trader_type=='buy':
                                                self.trader.buy(security=stock,price=price,amount=amount)
                                                text1='买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                                text1='可转债,买入'+name+text1
                                                print(text1)
                                                if seed=='真':
                                                    self.seed_emial_qq(text=text1)
                                                else:
                                                    pass
                                                #标记状态
                                                trader_stats.append('已买')
                                                #调整持股
                                                self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                                #调整账户资金
                                                self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                            else:
                                                trader_stats.append('已买')
                                        else:
                                            print('时间{} 代码{} 涨跌幅{}不在涨跌幅范围'.format(datetime.now(),stock,zdf))
                                            trader_stats.append('未买')
                                    else:
                                        trader_stats.append('未买')
                            except:
                                print('循环买入{}有问题'.format(stock))
                                trader_stats.append('未买')
                        else:
                            print('{}循环买入{}已经买入'.format(datetime.now(),stock))
                            trader_stats.append(stats)
                    df['交易状态']=trader_stats
                    if data_source=='默认':
                        df.to_excel(r'买入股票\买入股票.xlsx')
                    else:
                        df.to_excel(r'自定义买入\自定义买入.xlsx')  
                else:
                    print('买入可转债为空')

        else:
            print('{}目前不是交易时间'.format(datetime.now()))
    def run_stock_tail_platetrader_buy(self):
        '''
        运行交易策略 可转债,尾盘买入
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            stop=text['停止程序']
            max_zdf=text['尾盘建仓涨跌幅上限']
            min_zdf=text['尾盘建仓涨跌幅下限']
            data_source=text['买卖数据源']
            hold_limit=text['持股限制']
            name=text['策略名称']
            trader_stats=[]
            if stop=='真':
                print('程序停止')
            else:
                if data_source=='默认':
                    df=pd.read_excel(r'买入股票\买入股票.xlsx',dtype='object')
                    try:
                        del df['Unnamed: 0']
                    except:
                        pass
                else:
                    df=pd.read_excel(r'自定义买入\自定义买入.xlsx',dtype='object')
                    try:
                        del df['Unnamed: 0']
                    except:
                        pass
                if df.shape[0]>0:
                    for stock,stats in zip(df['证券代码'].tolist(),df['交易状态'].tolist()):
                        if stats=='未买':
                            amount=text['固定交易数量']
                            #检查是不是强制赎回
                            try:
                                if self.check_cov_bond_av_trader(stock=stock):
                                    spot_data=self.data.get_spot_data(stock=stock)
                                    #价格
                                    price=spot_data['最新价']
                                    #实时涨跌幅
                                    zdf=spot_data['涨跌幅']
                                    #检查是不是可以买入
                                    if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                        if zdf<=max_zdf and zdf>=min_zdf:
                                            trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price)
                                            if trader_type=='buy':
                                                self.trader.buy(security=stock,price=price,amount=amount)
                                                text1='买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                                text1='可转债,买入'+name+text1
                                                print(text1)
                                                if seed=='真':
                                                    self.seed_emial_qq(text=text1)
                                                else:
                                                    pass
                                                #标记状态
                                                hold_num=df[df['证券代码']==stock]
                                                if hold_num.shape[0]>0:
                                                    hold_num=hold_num['可用余额'].tolist()[-1]
                                                    if hold_num<hold_limit:
                                                        trader_stats.append('已买')
                                                    else:
                                                        trader_stats.append('到达持股限制')
                                                    #调整持股
                                                    self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                                    #调整账户资金
                                                    self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                            else:
                                                trader_stats.append('已买')
                                        else:
                                            print('时间{} 代码{} 涨跌幅{}不在涨跌幅范围'.format(datetime.now(),stock,zdf))
                                            trader_stats.append('未买')
                                    else:
                                        trader_stats.append('未买')
                            except:
                                print('可转债,尾盘买入{}有问题'.format(stock))
                                trader_stats.append('未买')
                        else:
                            print('{}循环卖出{}已经卖出'.format(datetime.now(),stock))
                            trader_stats.append(stats)
                    df['交易状态']=trader_stats
                    if data_source=='默认':
                        df.to_excel(r'买入股票\买入股票.xlsx')
                    else:
                        df.to_excel(r'自定义买入\自定义买入.xlsx')  
                else:
                    print('买入可转债为空')
        else:
            print('{}目前不是交易时间'.format(datetime.now()))
    def run_stock_trader_sell(self):
        '''
        运行交易策略 股票,策略卖出
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            stop=text['停止程序']
            data_source=text['买卖数据源']
            name=text['策略名称']
            stats_list=[]
            if stop=='真':
                print('程序停止')
            else:
                if data_source=='默认':
                    df=pd.read_excel(r'卖出股票\卖出股票.xlsx',dtype='object')
                else:
                    df=pd.read_excel(r'自定义卖出\自定义卖出.xlsx',dtype='object')
                try:
                    del df['Unnamed: 0']
                except:
                    pass
                if df.shape[0]>0:
                    for stock,stats in zip(df['证券代码'].tolist(),df['交易状态'].tolist()):
                        if stats=='未卖':
                            amount=text['固定交易数量']
                            #检查是否可以卖出
                            try:
                                if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                    #获取实时数据
                                    spot_data=self.data.get_spot_data(stock=stock)
                                    #价格
                                    price=spot_data['最新价']
                                    stock=str(stock)
                                    trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                    if trader_type=='sell':
                                        self.trader.sell(security=stock,price=price,amount=amount)
                                        text1='策略卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                        text1=name+text1
                                        print(text1)
                                        if seed=='真':
                                            self.seed_emial_qq(text=text1)
                                        else:
                                            pass
                                        #标记状态
                                        hold_data=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
                                        hold_data['证券代码']=hold_data['证券代码'].astype(str)
                                        stock=str(stock)
                                        try:
                                            del hold_data['Unnamed: 0']
                                        except:
                                            pass
                                        hold_num=hold_data[hold_data['证券代码']==stock]
                                        if hold_num.shape[0]>0:
                                            hold_num=hold_num['可用余额'].tolist()[-1]
                                            if hold_num>=10:
                                                stats_list.append('未卖')
                                            else:
                                                stats_list.append('已卖')
                                            #调整持股
                                            self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                            #调整账户资金
                                            self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                                    else:
                                        stats_list.append('已卖')
                                else:
                                    stats_list.append('未卖')
                            except:
                                print('循环卖出{}有问题'.format(stock))
                                stats_list.append('未卖')
                        else:
                            print("不是卖出状态")
                            stats_list.append(stats)
                    df['交易状态']=stats_list
                    if data_source=='默认':
                        df.to_excel(r'卖出股票\卖出股票.xlsx')
                    else:
                        df.to_excel(r'自定义卖出\自定义卖出.xlsx')  
                else:
                    print('没有卖出的可转债')
        else:
            print('{}目前不是交易时间'.format(datetime.now()))
    def run_stock_trader_sell_1(self):
        '''
        运行交易策略 股票,策略卖出,尾盘清仓
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            stop=text['停止程序']
            data_source=text['买卖数据源']
            name=text['策略名称']
            stats_list=[]
            if stop=='真':
                print('程序停止')
            else:
                if data_source=='默认':
                    df=pd.read_excel(r'卖出股票\卖出股票.xlsx',dtype='object')
                else:
                    df=pd.read_excel(r'自定义卖出\自定义卖出.xlsx',dtype='object')
                try:
                    del df['Unnamed: 0']
                except:
                    pass
                if df.shape[0]>0:
                    for stock,stats in zip(df['证券代码'].tolist(),df['交易状态'].tolist()):
                        if stats=='未卖':
                            amount=df[df['证券代码']==stock]
                            try:
                                if amount.shape[0].shape>0:
                                    amount=amount['可用余额'].tolist()[-1]
                                    #检查是否可以卖出
                                    if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                        #获取实时数据
                                        spot_data=self.data.get_spot_data(stock=stock)
                                        #价格
                                        price=spot_data['最新价']
                                        stock=str(stock)
                                        trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                        if trader_type=='sell':
                                            self.trader.sell(security=stock,price=price,amount=amount)
                                            text1='策略卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                            text1=name+text1
                                            print(text1)
                                            if seed=='真':
                                                self.seed_emial_qq(text=text1)
                                            else:
                                                pass
                                            #标记状态
                                            hold_data=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
                                            hold_data['证券代码']=hold_data['证券代码'].astype(str)

                                            stock=str(stock)
                                            try:
                                                del hold_data['Unnamed: 0']
                                            except:
                                                pass
                                            hold_num=hold_data[hold_data['证券代码']==stock]
                                            if hold_num.shape[0]>0:
                                                hold_num=hold_num['可用余额'].tolist()[-1]
                                                if hold_num>=10:
                                                    stats_list.append('未卖')
                                                else:
                                                    stats_list.append('已卖')
                                                #调整持股
                                                self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                                #调整账户资金
                                                self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                                        else:
                                            stats_list.append('已卖')
                                    else:
                                        stats_list.append('未卖')
                            except:
                                print('策略卖出,尾盘清仓{}有问题'.format(stock))
                                stats_list.append('未卖')
                        else:
                            print("不是卖出状态")
                            stats_list.append(stats)
                    df['交易状态']=stats_list
                    if data_source=='默认':
                        df.to_excel(r'卖出股票\卖出股票.xlsx')
                    else:
                        df.to_excel(r'自定义卖出\自定义卖出.xlsx')  
                else:
                    print('没有卖出的可转债')
        else:
            print('{}目前不是交易时间'.format(datetime.now()))
    def get_sell_not_in_analaysis_models_in_close(self):
        '''
        卖出不在分析模型的可转债
        '''
        if self.check_is_trader_date_1()==True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            #amount=text['固定交易数量']
            seed=text['发送通知']
            stop=text['停止程序']
            stop_profit=text['当日止盈']
            stop_loss=text['当日止损']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            if df.shape[0]>0:
                stock_list=df['证券代码'].tolist()
                for stock in stock_list:
                    try:
                        hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                        if sell_all=='是':
                            amount=hold_num
                        else:
                            amount=text['固定交易数量']
                        if self.trader_tool=='ths':
                            hist_df=self.data.get_hist_data_em(stock=stock)
                            shape=shape_analysis_ths(df=hist_df)
                        else:
                            hist_df=self.data.get_hist_data_em(stock=stock)
                            shape=shape_analysis_qmt(df=hist_df)
                        if shape.get_down_mean_line_sell()=='是' or shape.get_over_lining_sell()=='是' or shape.get_del_qzsh_cov_bond()=='是':
                            #获取实时数据
                            spot_data=self.data.get_spot_data(stock=stock)
                            #价格
                            price=spot_data['最新价']
                            stock=str(stock)
                            self.trader.sell(security=stock,price=price,amount=amount)
                            text1='尾盘卖出不符合 策略卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                            text1=name+text1
                            print(text1)
                            if seed=='真':
                                self.seed_emial_qq(text=text1)
                            else:
                                pass
                            #调整持股
                            self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                            #调整账户资金
                            self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                    except:
                        print('形态卖出有问题{}'.format(stock))
            else:
                print('没有持股')
        else:
            print('尾盘卖出不符合',datetime.now(),'不是交易时间')
    def daily_dynamic_stop_profit_stop_loss(self):
        '''
        当日止盈止损
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            #amount=text['固定交易数量']
            seed=text['发送通知']
            stop=text['停止程序']
            stop_profit=text['当日止盈']
            stop_loss=text['当日止损']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            if stop=='真':
                print('程序停止')
            else:
                df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
                try:
                    del df['Unnamed: 0']
                except:
                    pass
                if df.shape[0]>0:
                    stock_list=df['证券代码'].tolist()
                    for stock in stock_list:
                        #检查是否可以交易
                        try:
                            if self.check_cov_bond_av_trader(stock=stock):
                                #持有数量
                                hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                                if sell_all=='是':
                                    amount=hold_num
                                else:
                                    amount=text['固定交易数量']
                                #检查是否可以卖出
                                if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                    spot_data=self.data.get_spot_data(stock=stock)
                                    cost_price=df[df['证券代码']==stock]['成本价'].tolist()[-1]
                                    #价格
                                    price=spot_data['最新价']
                                    #实时涨跌幅
                                    zdf=((price-cost_price)/cost_price)*100
                                    if zdf>=stop_profit:
                                        stock=str(stock)
                                        trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                        if trader_type=='sell':
                                            self.trader.sell(security=stock,price=price,amount=amount)
                                            text1='当日止盈卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                            text1=name+text1
                                            print(text1)
                                            if seed=='真':
                                                self.seed_emial_qq(text=text1)
                                            else:
                                                pass
                                            #调整持股
                                            self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                            #调整账户资金
                                            self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                                    elif zdf<=stop_loss:
                                        stock=str(stock)
                                        trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                        if trader_type=='sell':
                                            self.trader.sell(security=stock,price=price,amount=amount)
                                            text1='当日止损卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                            text1=name+text1
                                            print(text1)
                                            if seed=='真':
                                                self.seed_emial_qq(text=text1)
                                            else:
                                                pass
                                            #调整持股
                                            self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                            #调整账户资金
                                            self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                                    else:
                                        print('{} {}不符合当日止盈止损条件'.format(stock,datetime.now()))
                                else:
                                    print('{} {}当日止盈不可以卖出'.format(stock,datetime.now()))
                            else:
                                print('{}当日止盈不可以交易'.format(datetime.now()))
                        except:
                            print('{}当日止盈有问题'.format(stock))
                else:
                    print('{}当日止盈没有持股'.format(datetime.now()))
        else:
            print('{}当日止盈不是交易时间'.format(datetime.now()))
    def dynamic_stop_profit_stop_loss(self):
        '''
        动态/账户止盈止损
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            #amount=text['固定交易数量']
            seed=text['发送通知']
            stop=text['停止程序']
            stop_profit=text['账户止盈']
            stop_loss=text['账户止损']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            if stop=='真':
                print('程序停止')
            else:
                df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
                try:
                    del df['Unnamed: 0']
                except:
                    pass
                if df.shape[0]>0:
                    stock_list=df['证券代码'].tolist()
                    for stock in stock_list:
                        #检查是否可以交易
                        try:
                            if self.check_cov_bond_av_trader(stock=stock):
                                #持有数量
                                hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                                cost_price=df[df['证券代码']==stock]['成本价'].tolist()[-1]
                                if sell_all=='是':
                                    amount=hold_num
                                else:
                                    amount=text['固定交易数量']
                                #检查是否可以卖出
                                if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                    spot_data=self.data.get_spot_data(stock=stock)
                                    #价格
                                    price=spot_data['最新价']
                                    #实时涨跌幅
                                    zdf=((price-cost_price)/cost_price)*100
                                    if zdf>=stop_profit:
                                        stock=str(stock)
                                        trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                        if trader_type=='sell':
                                            self.trader.sell(security=stock,price=price,amount=amount)
                                            text1='账户止盈卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                            text1=name+text1
                                            print(text1)
                                            if seed=='真':
                                                self.seed_emial_qq(text=text1)
                                            else:
                                                pass
                                            #调整持股
                                            self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                            #调整账户资金
                                            self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                                    elif zdf<=stop_loss:
                                        stock=str(stock)
                                        trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                        if trader_type=='sell':
                                            self.trader.sell(security=stock,price=price,amount=amount)
                                            text1='账户止损卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                            text1=name+text1
                                            print(text1)
                                            if seed=='真':
                                                self.seed_emial_qq(text=text1)
                                            else:
                                                pass
                                            #调整持股
                                            self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                            #调整账户资金
                                            self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                                    else:
                                        print('{} {}不符合账户止盈止损条件'.format(stock,datetime.now()))
                                else:
                                    print('{} {}账户止盈不可以卖出'.format(stock,datetime.now()))
                            else:
                                print('{}账户止盈不可以交易'.format(datetime.now()))
                        except:
                            print('{}账户止盈有问题'.format(stock))
                else:
                    print('{}账户止盈没有持股'.format(datetime.now()))
        else:
            print('{}账户止盈止损不是交易时间'.format(datetime.now()))
    def surge_and_fall_overfall_rebound_func(self):
        '''
        冲高回落---超跌反弹
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            #amount=text['固定交易数量']
            seed=text['发送通知']
            min_return=text['冲高最低收益']
            max_down=text['从高回落幅度']
            max_df=text['超跌幅度']
            ft_return=text['超跌反弹收益']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            df['可用余额']=df['可用余额'].astype(float)
            #股票不能T0
            #df1=df[df['可用余额']>=10]
            df1=df
            if df1.shape[0]>0:
                stock_list=df1['证券代码'].tolist()
                for stock in stock_list:
                    #持有数量
                    try:
                        hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                        if sell_all=='是':
                            amount=hold_num
                        else:
                            amount=text['固定交易数量']
                        trader_type,select,text1=self.analysis_models.surge_and_fall_overfall_rebound(stock=stock,
                            min_return=min_return,max_down=max_down,max_df=max_df,ft_return=ft_return
                        )
                        #冲高回落卖出
                        if trader_type=='冲高回落' and select==True:
                            #检查是否可以卖出
                            if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                #获取实时数据
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                stock=str(stock)
                                trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                if trader_type=='sell':
                                    self.trader.sell(security=stock,price=price,amount=amount)
                                    #text1='卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                    text1=name+text1
                                    print(text1)
                                    if seed=='真':
                                        self.seed_emial_qq(text=text1)
                                    else:
                                        pass
                                    #调整持股
                                    self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                    #调整账户资金
                                    self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                            else:
                                print('{}  {} 冲高回落 不可以卖出'.format(stock,datetime.now()))
                        #超跌反弹买入
                        elif trader_type=='超跌反弹' and select==True:
                            #检查是不是强制赎回
                            if self.check_cov_bond_av_trader(stock=stock):
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                #实时涨跌幅
                                zdf=spot_data['涨跌幅']
                                #检查是不是可以买入
                                if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                    trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                    if trader_type=='buy':
                                        self.trader.buy(security=stock,price=price,amount=amount)
                                        #text1='买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                        text1=name+text1
                                        print(text1)
                                        if seed=='真':
                                            self.seed_emial_qq(text=text1)
                                        else:
                                            pass
                                        #调整持股
                                        self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                        #调整账户资金
                                        self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                else:
                                    print('{} {}冲高回落超跌反弹不可以买入'.format(stock,datetime.now()))
                            else:
                                print('{} {}冲高回落超跌反弹不交易'.format(stock,datetime.now()))
                        else:
                            print('{} {}不符合冲高回落超跌反弹'.format(stock,datetime.now()))
                    except:
                        print('{}冲高回落超跌反弹有问题'.format(stock))
            else:
                print('{}冲高回落超跌反弹没有持股'.format(datetime.now()))
        else:
            print('{}冲高回落超跌反弹不是交易时间'.format(datetime.now()))
    def get_mi_pulse_trader(self):
        '''
        分钟脉冲分析
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            pulse_time=text['分钟脉冲时间']
            max_pulse=text['分钟脉冲上涨']
            min_pulse=text['分钟脉冲下跌']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            select=text['分钟脉冲是否时间增强']
            h=text['分钟脉冲增强小时']
            mi=text['分钟脉冲增强分钟']
            num=text['分钟脉冲增强倍数']
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            df['可用余额']=df['可用余额'].astype(float)
            #股票不能T0
            #df1=df[df['可用余额']>=10]
            df1=df
            if df1.shape[0]>0:
                stock_list=df1['证券代码'].tolist()
                for stock in stock_list:
                    try:
                        hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                        if sell_all=='是':
                            amount=hold_num
                        else:
                            amount=text['固定交易数量']
                        #脉冲
                        try:
                            pulse=self.analysis_models.get_mi_pulse_trader_analysis(n=pulse_time,x1=max_pulse,
                            x2=min_pulse,stock=stock,select=select,h=h,mi=mi,num=num)
                        except:
                            print('分钟脉冲分析{}有问题'.format(stock))
                            pulse=False
                        #脉冲卖出
                        if pulse=='sell':
                            #检查是否可以卖出
                            if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                #获取实时数据
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                stock=str(stock)
                                trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                if trader_type=='sell':
                                    self.trader.sell(security=stock,price=price,amount=amount)
                                    text1='分钟向上脉冲卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                    text1=name+text1
                                    print(text1)
                                    if seed=='真':
                                        self.seed_emial_qq(text=text1)
                                    else:
                                        pass
                                    #调整持股
                                    self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                    #调整账户资金
                                    self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                            else:
                                print('分钟脉冲{} {} 不可以卖出'.format(stock,datetime.now()))
                        elif pulse=='buy':
                            #检查是不是强制赎回
                            if self.check_cov_bond_av_trader(stock=stock):
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                #实时涨跌幅
                                zdf=spot_data['涨跌幅']
                                #检查是不是可以买入
                                if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                    trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='buy')
                                    if trader_type=='buy':
                                        self.trader.buy(security=stock,price=price,amount=amount)
                                        text1='分钟向下脉冲买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                        text1=name+text1
                                        print(text1)
                                        if seed=='真':
                                            self.seed_emial_qq(text=text1)
                                        else:
                                            pass
                                        #调整持股
                                        self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                        #调整账户资金
                                        self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                else:
                                    print('分钟脉冲{} {} 不可以买入'.format(stock,datetime.now()))
                            else:
                                print('分钟脉冲{} {} 强制赎回不可以交易'.format(stock,datetime.now()))
                        else:
                            print('分钟脉冲{} {} 不符合买入要求'.format(stock,datetime.now()))
                    except:
                        print('{}分钟脉冲反弹有问题'.format(stock))
            else:
                print('分钟脉冲{} 没有持股'.format(datetime.now()))
        else:
            print('分钟脉冲{} 不是交易时间'.format(datetime.now()))
    def get_dynamicmi_pulse_trader(self):
        '''
        动态脉冲分钟交易
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            daily=text['动态脉冲天数']
            mi=text['动态脉冲时间']
            up_ratio=text['动态脉冲上涨比例']
            down_ratio=text['动态脉冲下跌比例']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            df['可用余额']=df['可用余额'].astype(float)
            #股票不能T0
            #df1=df[df['可用余额']>=10]
            df1=df
            if df1.shape[0]>0:
                stock_list=df1['证券代码'].tolist()
                for stock in stock_list:
                    try:
                        hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                        if sell_all=='是':
                            amount=hold_num
                        else:
                            amount=text['固定交易数量']
                        #脉冲
                        try:
                            pulse=self.analysis_models.get_dynamic_trader_analysis(daily=daily,mi=mi,x=up_ratio,x1=down_ratio)
                        except:
                            print('动态脉冲分钟交易{}有问题'.format(stock))
                            pulse=False
                        #脉冲卖出
                        if pulse=='sell':
                            #检查是否可以卖出
                            if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                #获取实时数据
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                stock=str(stock)
                                trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                if trader_type=='sell':
                                    self.trader.sell(security=stock,price=price,amount=amount)
                                    text1='动态脉冲分钟交易卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                    text1=name+text1
                                    print(text1)
                                    if seed=='真':
                                        self.seed_emial_qq(text=text1)
                                    else:
                                        pass
                                    #调整持股
                                    self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                    #调整账户资金
                                    self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                            else:
                                print('动态脉冲分钟交易{} {} 不可以卖出'.format(stock,datetime.now()))
                        elif pulse=='buy':
                            #检查是不是强制赎回
                            if self.check_cov_bond_av_trader(stock=stock):
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                #实时涨跌幅
                                zdf=spot_data['涨跌幅']
                                #检查是不是可以买入
                                if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                    trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                    if trader_type=='sell':
                                        self.trader.buy(security=stock,price=price,amount=amount)
                                        text1='动态脉冲买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                        text1=name+text1
                                        print(text1)
                                        if seed=='真':
                                            self.seed_emial_qq(text=text1)
                                        else:
                                            pass
                                        #调整持股
                                        self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                        #调整账户资金
                                        self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                else:
                                    print('动态脉冲分钟交易{} {} 不可以买入'.format(stock,datetime.now()))
                            else:
                                print('动态脉冲分钟交易{} {} 强制赎回不可以交易'.format(stock,datetime.now()))
                        else:
                            print('动态脉冲分钟交易{} {} 不符合买入要求'.format(stock,datetime.now()))
                    except:
                        print('动态脉冲分钟{}有问题'.format(stock))
            else:
                print('动态脉冲分钟交易{} 没有持股'.format(datetime.now()))
        else:
            print('动态脉冲分钟交易{} 不是交易时间'.format(datetime.now()))
    def get_hour_pulse_trader(self):
        '''
        小时趋势
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            pulse_time=text['小时趋势时间']
            max_pulse=text['小时趋势上涨']
            min_pulse=text['小时趋势下跌']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            df['可用余额']=df['可用余额'].astype(float)
            #股票不能T0
            #df1=df[df['可用余额']>=10]
            df1=df
            if df1.shape[0]>0:
                stock_list=df1['证券代码'].tolist()
                for stock in stock_list:
                    try:
                        hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                        if sell_all=='是':
                            amount=hold_num
                        else:
                            amount=text['固定交易数量']
                        #脉冲
                        pulse=self.analysis_models.get_hour_pulse_trader_analysis(hour=pulse_time*60,x1=max_pulse,x2=min_pulse,stock=stock)
                        #脉冲卖出
                        if pulse=='sell':
                            #检查是否可以卖出
                            if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                #获取实时数据
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                stock=str(stock)
                                trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                if trader_type=='sell':
                                    self.trader.sell(security=stock,price=price,amount=amount)
                                    text1='小时趋势卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                    text1=name+text1
                                    print(text1)
                                    if seed=='真':
                                        self.seed_emial_qq(text=text1)
                                    else:
                                        pass
                                    #调整持股
                                    self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                    #调整账户资金
                                    self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                            else:
                                print('小时趋势{} {} 不可以卖出'.format(stock,datetime.now()))
                        elif pulse=='buy':
                            #检查是不是强制赎回
                            if self.check_cov_bond_av_trader(stock=stock):
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                #实时涨跌幅
                                zdf=spot_data['涨跌幅']
                                #检查是不是可以买入
                                if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                    trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                    if trader_type=='buy':
                                        self.trader.buy(security=stock,price=price,amount=amount)
                                        text1='小时趋势买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                        text1=name+text1
                                        print(text1)
                                        if seed=='真':
                                            self.seed_emial_qq(text=text1)
                                        else:
                                            pass
                                        #调整持股
                                        self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                        #调整账户资金
                                        self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                else:
                                    print('小时趋势{} {} 不可以买入'.format(stock,datetime.now()))
                            else:
                                print('小时趋势{} {} 强制赎回不可以交易'.format(stock,datetime.now()))
                        else:
                            print('小时趋势{} {} 不符合买入要求'.format(stock,datetime.now()))
                    except:
                        print('小时趋势{}有问题'.format(stock))
            else:
                print('小时趋势{} 没有持股'.format(datetime.now()))
        else:
            print('小时趋势{} 不是交易时间'.format(datetime.now()))
    def get_mean_line_trade(self):
        '''
        参考均线交易
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            update_time=text['盘中均线刷新时间']
            data_type=text['盘中参考数据周期']
            n=text['盘中窗口']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            df['可用余额']=df['可用余额'].astype(float)
            #股票不能T0
            #df1=df[df['可用余额']>=10]
            df1=df
            if df1.shape[0]>0:
                stock_list=df1['证券代码'].tolist()
                for stock in stock_list:
                    try:
                        hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                        if sell_all=='是':
                            amount=hold_num
                        else:
                            amount=text['固定交易数量']
                        #参考均线交易
                        try:
                            pulse=self.analysis_models.get_trader_mean_line_analysis(stock=stock,n=data_type,mean_line=n)
                        except:
                            print('参考均线{}有问题'.format(stock))
                            pulse=False
                        #参考均线交易卖出
                        if pulse=='sell':
                            #检查是否可以卖出
                            if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                #获取实时数据
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                stock=str(stock)
                                trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                if trader_type=='sell':
                                    self.trader.sell(security=stock,price=price,amount=amount)
                                    text1='参考均线交易卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                    text1=name+text1
                                    print(text1)
                                    if seed=='真':
                                        self.seed_emial_qq(text=text1)
                                    else:
                                        pass
                                    #调整持股
                                    self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                    #调整账户资金
                                    self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                            else:
                                print('参考均线交易趋势{} {} 不可以卖出'.format(stock,datetime.now()))
                        elif pulse=='buy':
                            #检查是不是强制赎回
                            if self.check_cov_bond_av_trader(stock=stock):
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                #实时涨跌幅
                                zdf=spot_data['涨跌幅']
                                #检查是不是可以买入
                                if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                    trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                    if trader_type=='buy':
                                        self.trader.buy(security=stock,price=price,amount=amount)
                                        text1='参考均线交易买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                        text1=name+text1
                                        print(text1)
                                        if seed=='真':
                                            self.seed_emial_qq(text=text1)
                                        else:
                                            pass
                                        #调整持股
                                        self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                        #调整账户资金
                                        self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                else:
                                    print('参考均线交易{} {} 不可以买入'.format(stock,datetime.now()))
                            else:
                                print('参考均线交易{} {} 强制赎回不可以交易'.format(stock,datetime.now()))
                        else:
                            print('参考均线交易{} {} 不符合买入要求'.format(stock,datetime.now()))
                    except:
                        print('参考均线{}有问题'.format(stock))
            else:
                print('参考均线交易{} 没有持股'.format(datetime.now()))
        else:
            print('参考均线交易{} 不是交易时间'.format(datetime.now()))

    def get_zig_trader(self):
        '''
        之子转向
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            x=text['zig转向点']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            df['可用余额']=df['可用余额'].astype(float)
            #股票不能T0
            #df1=df[df['可用余额']>=10]
            df1=df
            if df1.shape[0]>0:
                stock_list=df1['证券代码'].tolist()
                for stock in stock_list:
                    try:
                        hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                        if sell_all=='是':
                            amount=hold_num
                        else:
                            amount=text['固定交易数量']
                        try:
                            zig=self.analysis_models.cacal_zig_data(stock=stock,x=x)
                            stats=zig['买卖点'].tolist()[-1]
                        except:
                            print('zig{}有问题'.format(stock))
                            stats=False
                        if stats=='sell':
                            #检查是否可以卖出
                            if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                #获取实时数据
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                stock=str(stock)
                                trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                if trader_type=='sell':
                                    self.trader.sell(security=stock,price=price,amount=amount)
                                    text1='之子转向卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                    text1=name+text1
                                    print(text1)
                                    if seed=='真':
                                        self.seed_emial_qq(text=text1)
                                    else:
                                        pass
                                    #调整持股
                                    self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                    #调整账户资金
                                    self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                            else:
                                print('之子转向{} {} 不可以卖出'.format(stock,datetime.now()))
                        elif stats=='buy':
                            #检查是不是强制赎回
                            if self.check_cov_bond_av_trader(stock=stock):
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                #实时涨跌幅
                                zdf=spot_data['涨跌幅']
                                #检查是不是可以买入
                                if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                    trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell')
                                    if trader_type=='sell':
                                        self.trader.buy(security=stock,price=price,amount=amount)
                                        text1='之子转向买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                        text1=name+text1
                                        print(text1)
                                        if seed=='真':
                                            self.seed_emial_qq(text=text1)
                                        else:
                                            pass
                                        #调整持股
                                        self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                        #调整账户资金
                                        self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                else:
                                    print('之子转向{} {} 不可以买入'.format(stock,datetime.now()))
                            else:
                                print('之子转向{} {} 强制赎回不可以交易'.format(stock,datetime.now()))
                        else:
                            print('之子转向{} {} 不符合买入要求'.format(stock,datetime.now()))
                    except:
                        print('之子转向{}有问题'.format(stock))
                    
            else:
                print('之子转向{} 没有持股'.format(datetime.now()))
        else:
            print('之子转向{} 不是交易时间'.format(datetime.now()))
    def save_account_data(self):
        '''
        保持账户数据
        '''
        #if self.check_is_trader_date_1()==True:
        if True:
            #持股
            try:
                position=self.trader.position()
                position['标的类型']=position['证券代码'].apply(self.base_func.select_data_type)
                with open('分析配置.json','r+',encoding='utf-8') as f:
                    com=f.read()
                text=json.loads(com)
                trader_type=text['交易品种']
                if trader_type=='全部':
                    position.to_excel(r'持股数据\持股数据.xlsx')
                else:
                    position=position[position['标的类型']==trader_type]
                print('账户数据获取成功')
                print(position)
            except:
                print('获取持股失败')
            #账户
            try:
                account=self.trader.balance()
                account.to_excel(r'账户数据\账户数据.xlsx')
                print('获取账户成功')
                print(account)
            except:
                print('获取账户失败')
        else:
            self.connact()
            print('{} 目前不是交易时间'.format(datetime.now()))
    def save_account_data_1(self):
        '''
        保持账户数据
        '''
        #if self.check_is_trader_date_1()==True:
        #持股
        if True:
            try:
                position=self.trader.position()
                position.to_excel(r'持股数据\持股数据.xlsx')
                print('账户数据获取成功')
            except:
                print('获取持股失败')
            #账户
            try:
                account=self.trader.balance()
                account.to_excel(r'账户数据\账户数据.xlsx')
                print('获取账户成功')
            except:
                print('获取账户失败')
        else:
            self.connact()
            print('{} 目前不是交易时间'.format(datetime.now()))
    def seed_qq_email(self):
        #self.connact()
        #self.trader.refresh()
        if self.check_is_trader_date()==True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            name=text['策略名称']
        #if True:
            if self.connact()==True:
                now=str(datetime.now())
                text1=name+now+'程序连接正常'
                print(text1)
                with open('分析配置.json','r+',encoding='utf-8') as f:
                    com=f.read()
                text=json.loads(com)
                seed=text['发送通知']
                if seed=='真':
                    self.seed_emial_qq(text=text1)
                else:
                    pass
            else:
                self.connact()
        else:
            self.connact()
            print('{} 目前不是交易时间'.format(datetime.now()))
    def get_dt_grid_trade(self):
        '''
        动态网格交易
        '''
        if self.check_is_trader_date_1()==True:
        #if True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            seed=text['发送通知']
            daily=text['网格最近N天']
            n=text['网格数量']
            tiem_size=text['网格时间大小']
            q=text['买卖分位数']
            entiy_select=text['网格单元格小于']
            bs=text['增强倍数']
            stop=text['跌破最后一个网格是否全部卖出']
            if stop=='True':
                stop=True
            else:
                stop=False
            stop_line=text['网格止损线']
            sell_all=text['一次性卖出']
            name=text['策略名称']
            df=pd.read_excel(r'持股数据\持股数据.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except:
                pass
            df['可用余额']=df['可用余额'].astype(float)
            #股票不能T0
            #df1=df[df['可用余额']>=10]
            df1=df
            if df1.shape[0]>0:
                stock_list=df1['证券代码'].tolist()
                for stock in stock_list:
                    try:
                        hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                        if sell_all=='是':
                            amount=hold_num
                        else:
                            amount=text['固定交易数量']
                        # 动态网格交易
                        #try:
                            pulse,text1=self.analysis_models.get_grid_analysis(stock=stock,daily=daily,n=n,time_size=tiem_size,
                            buy_sell_dot=q,stop=stop,stop_line=stop_line,entiy_select=entiy_select,bs=bs)
                        #except:
                            #print('动态网格交易{}有问题'.format(stock))
                            #pulse=False
                        # 动态网格交易
                        if pulse in ['sell','all_sell','sell_up']:
                            #'sell_down'不卖出
                            #检查是否可以卖出
                            if self.check_stock_is_av_sell(stock=stock,amount=amount):
                                #获取实时数据
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                stock=str(stock)
                                if pulse=='all_sell':
                                    hold_num=df[df['证券代码']==stock]['可用余额'].tolist()[-1]
                                    amount=amount
                                else:
                                    amount
                                self.trader.sell(security=stock,price=price,amount=amount)
                                #text1=' 动态网格交易卖出 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                text1=name+text1
                                print(text1)
                                if seed=='真':
                                    self.seed_emial_qq(text=text1)
                                else:
                                    pass
                                #调整持股
                                self.adjust_hold_data(stock=stock,trader_type='sell',price=price,amount=amount)
                                #调整账户资金
                                self.adjust_account_cash(stock=stock,trader_type='sell',price=price,amount=amount)
                            else:
                                print(' 动态网格交易{} {} 不可以卖出'.format(stock,datetime.now()))
                        elif pulse=='buy':
                            #检查是不是强制赎回
                            if self.check_cov_bond_av_trader(stock=stock):
                                spot_data=self.data.get_spot_data(stock=stock)
                                #价格
                                price=spot_data['最新价']
                                #实时涨跌幅
                                zdf=spot_data['涨跌幅']
                                #检查是不是可以买入
                                if self.check_stock_is_av_buy(stock=stock,price=price,amount=amount):
                                    self.trader.buy(security=stock,price=price,amount=amount)
                                    #text1=' 动态网格交易买入 时间{} 代码{} 价格{} 数量{}'.format(datetime.now(),stock,price,amount)
                                    text1=name+text1
                                    print(text1)
                                    if seed=='真':
                                        self.seed_emial_qq(text=text1)
                                    else:
                                        pass
                                    #调整持股
                                    self.adjust_hold_data(stock=stock,trader_type='buy',price=price,amount=amount)
                                    #调整账户资金
                                    self.adjust_account_cash(stock=stock,trader_type='buy',price=price,amount=amount)
                                else:
                                    print('动态网格交易{} {} 不可以买入'.format(stock,datetime.now()))
                            else:
                                print('动态网格交易{} {} 强制赎回不可以交易'.format(stock,datetime.now()))
                        else:
                            print('动态网格交易{} {} 不符合买入要求'.format(stock,datetime.now()))
                    except:
                        print('动态网格交易{}有问题'.format(stock))
            else:
                print('动态网格交易{} 没有持股'.format(datetime.now()))
        else:
            print('动态网格交易{} 不是交易时间'.format(datetime.now()))
    def run_user_def_trader_models(self):
        '''
        运行自定义交易模型
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        if True:
            user_def_type=text['自定义函数运行类型']
            user_def_time=text['自定义函数模块运行时间']
            user_def_func=text['自定义函数']

            for def_type,def_time,def_func in zip(user_def_type,user_def_time,user_def_func):
                func='self.user_def_models.{}'.format(def_func)
                if def_type=='定时':
                    schedule.every().day.at('{}'.format(def_time)).do(eval(func))
                    print('{}运行自定义分析模型{}函数在{}'.format(def_type,def_func,def_time))
                else:
                    schedule.every(def_time).minutes.do(eval(func))
                    print('{}运行自定义分析模型{}函数每{}分钟'.format(def_type,def_func,def_time))


if __name__=='__main__':
    '''
    交易策略
    '''
    with open('分析配置.json','r+',encoding='utf-8') as f:
        com=f.read()
    text=json.loads(com)
    trader_tool=text['交易系统']
    exe=text['同花顺下单路径']
    tesseract_cmd=text['识别软件安装位置']
    print(tesseract_cmd)
    qq=text['发送qq']
    test=text['测试']
    open_set=text['是否开启特殊证券公司交易设置']
    qmt_path=text['qmt路径']
    qmt_account=text['qmt账户']
    qmt_account_type=text['qmt账户类型']
    trader=trader_strategy(trader_tool=trader_tool
    ,exe=exe,tesseract_cmd=tesseract_cmd,qq=qq,
                           open_set=open_set,qmt_path=qmt_path,qmt_account=qmt_account,
                           qmt_account_type=qmt_account_type)
    trader.connact()
    #运行就更新账户数据
    trader.save_account_data()
    if test=='真':
        trader.seed_qq_email()
        trader.save_account_data()
        #trader.updata_all_data()
        trader.run_stock_trader_buy()
        trader.run_stock_trader_sell()
        trader.daily_dynamic_stop_profit_stop_loss()
        trader.dynamic_stop_profit_stop_loss()
        trader.surge_and_fall_overfall_rebound_func()
        trader.get_mi_pulse_trader()
        trader.get_dynamicmi_pulse_trader
        trader.get_hour_pulse_trader()
        trader.get_zig_trader()
        trader.get_mean_line_trade()
        trader.get_dynamicmi_pulse_trader()
        trader.get_dt_grid_trade()
        trader.get_sell_not_in_analaysis_models_in_close()
    else:
        #交易前先保存数据
        user_def_select=text['是否开启自定义函数模块']
        user_def_type=text['自定义函数运行类型']
        user_def_time=text['自定义函数模块运行时间']
        user_def_func=text['自定义函数']
        if user_def_select=='是':
            print('开启自定义函数模块')
            trader.run_user_def_trader_models()
        else:
            print('不开启自定义函数模块')
        #建仓
        buy_time=text['买入时间']
        schedule.every().day.at('{}'.format(buy_time)).do(trader.run_stock_trader_buy)
        #卖出
        sell_time=text['卖出时间']
        schedule.every().day.at('{}'.format(sell_time)).do(trader.run_stock_trader_sell)
        #循环买入
        cycle_buy_select=text['是否循环买入设置']
        if cycle_buy_select=='是':
            print('循环买入启动')
            cycle_buy_time=text['循环买入刷新时间']
            schedule.every(cycle_buy_time).minutes.do(trader.run_stock_trader_buy)
        else:
            print('不启动循环买入程序')
        #循环卖出
        cycle_sell_select=text['是否循环卖出']
        if cycle_sell_select=='是':
            print('循环卖出启动')
            cycle_sell_time=text['循环卖出刷新时间']
            schedule.every(cycle_sell_time).minutes.do(trader.run_stock_trader_sell)
        else:
            print('不启动循环卖出程序')
        #当日止盈止损
        daily_zyzs_select=text['是否当日止盈止损']
        if daily_zyzs_select=='是':
            print('当日止盈止损启动')
            daily_zyzs_time=text['当日止盈止损刷新时间']
            schedule.every(daily_zyzs_time).minutes.do(trader.daily_dynamic_stop_profit_stop_loss)
        else:
            print('不启动止盈止损')
        #账户止盈止损
        account_zyzs_select=text['是否账户止盈止损']
        if account_zyzs_select=='是':
            print('启动账户止盈止损')
            account_zyzs_time=text['账户止盈止损刷新时间']
            schedule.every(account_zyzs_time).minutes.do(trader.dynamic_stop_profit_stop_loss)
        else:
            print('不启动账户止盈止损')
        #冲高回落模块--超跌反弹
        cghl_zdft_select=text['是否冲高回落模块--超跌反弹']
        if cghl_zdft_select=='是':
            print('启动冲高回落模块--超跌反弹')
            cghl_zdft_time=text['冲高回落模块--超跌反弹刷新时间']
            schedule.every(cghl_zdft_time).minutes.do(trader.surge_and_fall_overfall_rebound_func)
        else:
            print('不启动启动冲高回落模块--超跌反弹')
        #分钟脉冲设置
        fzmc_select=text['是否分钟脉冲']
        if fzmc_select=='是':
            print('启动分钟脉冲')
            fzmc_time=text['分钟脉冲刷新时间']
            schedule.every(fzmc_time).minutes.do(trader.get_mi_pulse_trader)
        else:
            print('不启动分钟脉冲')
        #小时趋势
        xsqs_select=text['是否小时趋势']
        if xsqs_select=='是':
            print('启动小时趋势')
            xsqs_time=text['小时趋势刷新时间']
            xsqs_time=xsqs_time
            schedule.every(xsqs_time).minutes.do(trader.get_hour_pulse_trader)
        else:
            print('不启动小时趋势')
        #动态分钟脉冲
        dt_mi_select=text['是否动态脉冲']
        if dt_mi_select=='是':
            print('启动动态脉冲')
            dt_mi_time=text['动态脉冲刷新时间']
            schedule.every(dt_mi_time).minutes.do(trader.get_dynamicmi_pulse_trader)
        else:
            print('不启动动态脉冲')
        #之子转向
        zig_select=text['是否zig']
        if zig_select=='是':
            print('启动zig')
            zig_time=text['zig刷新时间']
            schedule.every(zig_time).minutes.do(trader.get_zig_trader)
        else:
            print('不启动zig')
        #盘中均线刷新时间
        mean_select=text['是否盘中参考均线']
        if mean_select=='是':
            print("启动盘中参考均线")
            trader_mean_line_update_time=text['盘中均线刷新时间']
            schedule.every(trader_mean_line_update_time).minutes.do(trader.get_mean_line_trade)
        else:
            print("不启动盘中参考均线")
        #发qq
        schedule.every(10).minutes.do(trader.seed_qq_email)
        #盘中换股
        #同步手动下单数据
        tb_select=text['是否同步数据']
        tb_time=text['同步周期']
        if tb_select=='是':
            print('启动同步数据')
            schedule.every(tb_time).minutes.do(trader.save_account_data)
        else:
            print('不启动同步数据')
        #是否开启动态网格
        dt_grid_select=text['是否开启动态网格']
        dt_grid_time=text['自定义网格刷新时间']
        if dt_grid_select=='是':
            print('开启动态网格')
            schedule.every(dt_grid_time).minutes.do(trader.get_dt_grid_trade)
        else:
            print('不开启动态网格')
    while True:
        schedule.run_pending()
        time.sleep(1)




        

