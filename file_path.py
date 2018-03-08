#保存各类表的路径，文件保存路径，原数据路径
import os
import pandas as pd
base_path=os.getcwd()

#无关标题匹配表
stop_w_path=os.path.join(base_path,'stop_w.txt')
#标题停用符号表
stop_symbol_path=os.path.join(base_path,'stop_symbol.txt')
#转义字符表
change_symbol_path=os.path.join(base_path,'转义字符还原.xlsx')
#文章停用词表
stopw_path=os.path.join(base_path,'stopwords.txt')
#存储路径feature_table的路径

feature_table_path=os.path.join(base_path,'feature_table')

def merge_path(pat,project_name):
    """

    :param pat: 本地路径
    :param project_name: 项目名
    :return: 文件的具体路径
    """
    datapath=pat+'\\'+project_name
    return datapath

def sucessRate_txtpath(base_path,sucessRate_fileName,project_name):
    """

    :param base_path: 本地路径
    :param sucessRate_fileName: 文件名
    :param project_name: 项目名
    :return: 成功率表，所有文本路径列表
    """
    sucess_rate_path = os.path.join(base_path,sucessRate_fileName)
  #  datapath = os.path.join(base_path, 'data')+'\\'+project_name
    datapath =merge_path(os.path.join(base_path, 'data'), project_name)
    # 打开成功率表
    f = open(sucess_rate_path)
    res = pd.read_csv(f)
    #项目对于的文件名：descXXX.txt
    listfile = list(res.iloc[:, 1])
    txtpath = []
    for i in range(len(listfile)):
        txt_path=merge_path(datapath, listfile[i])
        txtpath.append(txt_path)
        #txtpath.append(datapath + '\\' + listfile[i])

    return res,txtpath


