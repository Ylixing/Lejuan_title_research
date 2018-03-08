#得到小标题的个数与目标值的相关系数（较相关），得到更容易获得成功的标题个数和标题结构
import get_feature
import jieba
import os
import jieba.posseg as pseg
import titletxt_classify
import file_path
import pandas as pd
from sklearn.feature_selection import SelectKBest,chi2,mutual_info_classif
import re

def partofspeech_tagging(titlelist_list,reg='\[|\'|\]'):
    """

    :param titlelist_list: 所有文本小标题列表
    :param reg: 去除符号的正则表达
    :return:所有文本小标题词性结构
    """
    for titlelist in titlelist_list:
        titlelist=re.sub(reg,'',titlelist)  #str
        #print(titlelist)
        titlelist= titlelist.split(',')
        title_cut_list=[]
        for title in titlelist:

            title_flag=''
            for words,flag in pseg.cut(title):
                if flag=='x':continue
                else:title_flag=title_flag+flag+'_'
            #if title_flag=='v_r_r_n_':print(title)
           # print(title_flag)
            title_cut_list.append(title_flag)
           # title_cut_list_str=' '.join(title_cut_list)
        yield title_cut_list

def title_len(title_list_all):
    """

    :param title_list_all: 所有文本小标题列表
    :return: 所有文本小标题个数
    """
    for titlelist in title_list_all:
        titlelist= titlelist.split(',')
        yield len(titlelist)

def word_count(word_list,target):
    """

    :param word_list: 文本词性变化结构列表
    :param target: 目标值（0或者1）
    :return: 成功样本的文本词性变化个数列表，失败样本的文本词性变化个数列表，成功样本的文本词性变化频率列表，失败样本的文本词性变化频率列表
    """
    sucess_word = []
    fail_word = []
    for index, item in enumerate(target):
        if float(item) > 0.5:
            sucess_word = sucess_word + word_list[index]
        else:
            fail_word = fail_word + word_list[index]
    sucess_word_count = pd.Series(sucess_word).value_counts()
    fail_word_count = pd.Series(fail_word).value_counts()
    sucess_word_countRate = sucess_word_count.apply(lambda x: x / sucess_word_count.sum())
    fail_word_countRate= fail_word_count.apply(lambda x: x / fail_word_count.sum())
    return sucess_word_count,fail_word_count,sucess_word_countRate,fail_word_countRate

def title_structure(sucess_word_countRate,fail_word_countRate):
    """

    :param sucess_word_countRate: 成功样本的文本词性变化频率列表(由高到低）
    :param fail_word_countRate: 失败样本的文本词性变化频率列表(由高到低）
    :return: 筛选后的最佳文本词性变化列表
    """
    fail_word_list=list(fail_word_countRate.index)
    sucess_word_list=list(sucess_word_countRate.index)
    structure=[]
    for i in sucess_word_list:
        if i not in fail_word_list:

            structure.append(i)
    return structure


def pearson_(col1,col2,col=0,threshold_value=3):
    """

    :param col1: 相关系数比较的第一个属性
    :param col2: 相关系数比较的第二个属性
    :param col: 筛选条件的属性列，一般为属性名为""title_len_",即标题长度
    :param threshold_value: 筛选条件的阈值，这里是标题长度
    :return: col1和col2合并后的dataFrame，col1和col2相关系数
    """
    df=pd.concat([col1,col2],axis=1)
    df=df.loc[df.loc[:,col]>threshold_value,:]
    return df,df.corr()


if __name__ == '__main__':
    data = titletxt_classify.open_data(base_path=file_path.base_path, project_name='feature_table\\data.csv')
    target = data['goal']
    # 得到标题长度
    title_len_ = pd.Series(title_len(data['title_list']))
    #得到标题长度与目标值合并的dataframe，以及他们的相关系数
    df, df_corr = pearson_(col1=title_len_, col2=target)
    print(df_corr)
    # 最适合小标题个数  ##4
    title_count_best = df.loc[df.iloc[:, 1] == 1, 0].value_counts()
    print(title_count_best.index[0])
    #相当与分词后词矩阵
    title_stru_list=list(partofspeech_tagging(data['title_list']))
    sucess_word_count, fail_word_count, sucess_word_countRate, fail_word_countRate=word_count(title_stru_list, target)
    #得到小标题的编写结构  ##['r_p_v_r_', 'r_uj_n_', 'eng_uj_n_', 'v_r_r_n_']
    title_stru=title_structure(sucess_word_countRate[:8], fail_word_countRate[:8])
    print(title_stru)




