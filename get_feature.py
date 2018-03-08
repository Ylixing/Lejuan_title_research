
#从原始数据中得到文本标题，筹款成功率,，文本目标值（成功为1，不成功为0）,文本小标题:file_name,sucess_rate,goal,title_list
import os
import file_path
import re
import pandas as pd

#打开无关标题匹配表
title_reg_del=[line.rstrip() for line in open(file_path.stop_w_path, errors='ignore', encoding='gbk')]

#打开标题应去除的符号表  ##删除
stop_symbol=[line.rstrip() for line in open(file_path.stop_symbol_path, errors='ignore', encoding='gbk')]
reg=re.compile('//|<|>|（|）|/(|/)|:|：|，|,|h3|br|。|“|”')

#打开转义字符表
change_symbol=pd.read_excel(file_path.change_symbol_path)
patt=change_symbol.iloc[:,0]
repl=change_symbol.iloc[:,1]

def reg_word():
    pass

def txt_sub(txt,patt=patt,repl=repl):
    """

    :param txt: 文本
    :param patt: 转义字符匹配字符
    :param repl: 转义字符替换字符
    :return: 转义字符替换后的文本
    """
    for index,item in enumerate(repl):
        if item==' ':txt=re.sub(patt[index],'',txt)
        else:txt=re.sub(patt[index],item,txt)
    return txt


def title_sub(title_list,title_reg_del=title_reg_del,reg=reg):
    """

    :param title_list: 一个文本小标题列表
    :param title_reg_del: 需要删除的小标题列表
    :param reg: 无关符号的正则表达
    :return: 删除无关字符、无关小标题后的一个文本小标题列表
    """
    title_list_new=[]
    for index,title in enumerate(title_list):
        p=0
        #去除无关符号
        title=re.sub(reg,'',title)
        # 如果title里包含一些删除条件的关键词
        for i in title_reg_del:
            #如果包含那些词（我们，项目……）
            if re.search(i,title):
                #print('yes')
                p=1
           # break
        #print(p)
        if p==0:title_list_new.append(title)

    return title_list_new



def get_goal(sucess_rate,threshold_value=0.8):
    """

    :param sucess_rate: 所有文本筹款成功率
    :param threshold_value: 将成功率离散为0，1的阈值
    :return: 返回离散目标值（"1"为成功，"2"为不成功）
    """
    for i in sucess_rate:
        if float(i)>threshold_value:goal=1
        else:goal=0
        yield goal


def get_title(txtpath,reg='h3>.{3,20}?</h3>'):
    """

    :param txtpath: 所有文本路径
    :param reg: 小标题的正则表达
    :return: 所有文本的小标题列表
    """
    for i in txtpath:
        with open(i) as f:
            txt=f.read()
        #将转义字符还原
        txt=txt_sub(txt)
        #找到标题
        title_list = re.findall(reg, txt)
        #删除不符合的标题，替换一些关键词
        title_list=title_sub(title_list)
        yield title_list




if __name__ == '__main__':
    #修改文件名
    res,txtpath=file_path.sucessRate_txtpath(base_path=file_path.base_path,sucessRate_fileName='sucessRate_table\\helpSick_suceessRate.csv',project_name='疾病救助')
    #修改阈值，得到0，1目标值
    goal=pd.Series(get_goal(sucess_rate= res.iloc[:, 2],threshold_value=0.3))
    #得到每个文本的小标题列表
    title_list_all=pd.Series(get_title(txtpath))
    #合并数据
    table=pd.concat([res.iloc[:,1:],title_list_all,goal],axis=1)
    #修改文件名
    pat=file_path.feature_table_path+'\\'+'helpSick_feature.csv'
    table.to_csv(pat,header=['file_name','sucess_rate','title_list','goal'])



