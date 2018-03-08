#文章小标题文本分类，训练数据为每篇文章的小标题文本，目标为是否成功（成功为1，不成功为0），训练得到模型train_model.m
import pandas as pd
import jieba
import os
import sys
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest,chi2,mutual_info_classif
from numpy import array
from scipy.stats import pearsonr
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import re
import file_path
import os
from sklearn.externals import joblib

#打开停用词表
stopwords=[line.rstrip() for line in open(file_path.stopw_path, errors='ignore', encoding='utf-8')]

def open_data(base_path=file_path.base_path,project_name='feature_table\\other_feature.csv'):
    # 修改文件名
    datapath = file_path.merge_path(file_path.base_path,project_name)
    f = open(datapath)
    data = pd.read_csv(f)
    return data

#分词
def get_cut_word(title_list_all,reg='\[|\'|\]|\,'):
    for title_str in title_list_all:
        title_str2=re.sub(reg,'',title_str)
        word_list=jieba.lcut(title_str2)
        word_str=' '.join(word_list)

        yield word_str

#特征表示
def feature_expresion(cutword_data):
    CountVec=CountVectorizer()
    TfidfTransf=TfidfTransformer()
    fre_matrix=CountVec.fit_transform(cutword_data)  #各短信的词频统计
    tfidf=TfidfTransf.fit_transform(fre_matrix)  #得到tf-idf词矩阵
    vocabulary = CountVec.get_feature_names()
    return fre_matrix,tfidf,vocabulary

# 特征选择
def feature_selection(x_matrix, target, fs, k):
    """

    :param fs: 特征选择方法
    :param k: 特征选择阈值
    :return: 特征选择后的X矩阵，特征的布尔值（去除的特征词为false，留下的特征词为true）
    """
    fea_select = SelectKBest(fs, k)
    x = fea_select.fit_transform(x_matrix, target)
    fea_bool = fea_select.get_support()
    return x, fea_bool

def adjust_param():
    pass


# 交叉验证
def model_result(clf, x, y):

    #clf.fit(x, y)
    scores = cross_val_score(clf, x, y, cv=4)
    return scores

if __name__ == '__main__':
    #修改project_name
    data=open_data(base_path=file_path.base_path,project_name='feature_table\\data.csv')

    #得到小标题分词结果
    cutword_data=list(get_cut_word(title_list_all=data['title_list']))

    # 词特征表示
    fre_matrix, tfidf_x, vocabulary = feature_expresion(cutword_data)

    target =data['goal']
    #特征选择后的x矩阵，以及筛选的特征布尔值
    x_chi, fea_bool = feature_selection(x_matrix=tfidf_x,target=target,fs=chi2, k=60)
    clf=MultinomialNB()
    #clf=svm.SVC()
   # clf = tree.DecisionTreeClassifier()
    scores = model_result(clf, x_chi, target)
    print(scores)

    #保存模型
    #clf.fit(x_chi, target)
    #joblib.dump(clf, "train_model.m")

    #筛选后的特征词
    #for index,item in enumerate(fea_bool):
     #   if item:print(vocabulary[index])