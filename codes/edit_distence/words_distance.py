#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 14:30
# @Author  : lilijuan
# @File    : words_distance.py
import sys
import pinyin
import jieba
import string
import re,os
from collections import Counter

FILE_PATH = os.path.abspath("../../data/words_info/token_freq_pos_jieba.txt")
PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += "。，？：；｛｝［］‘“”《》／！％……（）\\n、 "
print(PUNCTUATION_LIST)
# 创建词频字典
def create_frequent_dict(dir_path):
    words=[]
    for file_name in os.listdir(dir_path):
        if file_name.find(".txt") != -1:
            file_path = "/".join([dir_path, file_name])
            with open(file_path, "r") as f:
                lines=f.readlines()
                for line in lines:
                    words.extend([w for w in jieba.cut(line) if w not in PUNCTUATION_LIST])
    print(len(words),words[:10])
    words_dict=Counter(words)
    del words
    print(len(words_dict),words_dict)

# 读取 词语 词频 字典
def construct_dict(file_path):
    word_freq = {}
    with open(file_path, "r") as f:
        for line in f:
            info = line.split()
            word = info[0]
            frequency = info[1]
            word_freq[word] = frequency
    return word_freq


def load_cn_words_dict(file_path):
    cn_words_dict = ""
    with open(file_path, "r") as f:
        for word in f:
            cn_words_dict += word.strip()
    return cn_words_dict


def edits1(phrase, cn_words_dict):
    "All edits that are one edit away from `phrase`."
    splits = [(phrase[:i], phrase[i:]) for i in range(len(phrase) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in cn_words_dict]
    inserts = [L + c + R for L, R in splits for c in cn_words_dict]
    return set(deletes + transposes + replaces + inserts)


def known(phrases):
    return set(phrase for phrase in phrases if phrase in phrase_freq)


def get_candidates(error_phrase):
    candidates_1st_order = []
    candidates_2nd_order = []
    candidates_3nd_order = []
    error_pinyin = pinyin.get(error_phrase, format="strip", delimiter="/")
    cn_words_dict = load_cn_words_dict("../../data/words_info/cn_dict.txt")
    candidate_phrases = list(known(edits1(error_phrase, cn_words_dict)))
    for candidate_phrase in candidate_phrases:
        candidate_pinyin = pinyin.get(candidate_phrase, format="strip", delimiter="/")
        if candidate_pinyin == error_pinyin:
            candidates_1st_order.append(candidate_phrase)
        elif candidate_pinyin.split("/")[0] == error_pinyin.split("/")[0]:
            candidates_2nd_order.append(candidate_phrase)
        else:
            candidates_3nd_order.append(candidate_phrase)

    return candidates_1st_order, candidates_2nd_order, candidates_3nd_order


def auto_correct(error_phrase):
    c1_order, c2_order, c3_order = get_candidates(error_phrase)
    if c1_order:
        return max(c1_order, key=phrase_freq.get)
    elif c2_order:
        return max(c2_order, key=phrase_freq.get)
    else:
        return max(c3_order, key=phrase_freq.get)

def auto_correct_sentence(error_sentence, verbose=True):
    jieba_cut = jieba.cut(error_sentence, cut_all=False)
    seg_list = "\t".join(jieba_cut).split("\t")
    print("分词结果:{}".format(seg_list))

    correct_sentence = ""

    for phrase in seg_list:

        correct_phrase = phrase
        # check if item is a punctuation
        if phrase not in PUNCTUATION_LIST:
            # check if the phrase in our dict, if not then it is a misspelled phrase
            if phrase not in phrase_freq.keys():
                correct_phrase = auto_correct(phrase)
                if verbose:
                    print("错误词汇信息:",phrase, correct_phrase)

        correct_sentence += correct_phrase

    return correct_sentence


phrase_freq = construct_dict(FILE_PATH)

'''简单的中文文本纠错：
思想：首先对文本进行分词，分词后的词语不在词典中则这个词可能是错误的
根据拼音对词语换个词语词典提取候选词语
根据phrase_freq（语料中词语出现的频率）取频率最高的同音词语作为纠错的词语
'''
def test():
    texts=["机七学习是人工智能领遇最能体现智能的一个分知！",'杭洲是中国的八大古都之一，因风景锈丽，享有"人间天棠"的美誉！',
           "请帮我打开四好屏幕"]
    for text in texts:
        correct_sent = auto_correct_sentence(text)
        print(text,correct_sent)
def main():
    create_frequent_dict("../../data/cn_texts")
if __name__ == "__main__":
    main()