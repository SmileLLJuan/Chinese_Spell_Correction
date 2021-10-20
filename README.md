# Chinese_Spell_Correction
中文拼写纠错-文本纠错
1、edict_distance
    - words_distance 主要思想:
    （1）中文分词 对文本中的词语进行遍历， 
    （2）如果词语不属于特殊符号&词语没有出现在常见词的词典中则：（常见词词典地址:../../data/words_info/token_freq_pos_jieba.txt,保存词语 & 词频）
    根据错误词语中字符与词典中的词语的编辑距离得出正确词语的候选集和；
    （3）选择候选词语中频率最大的作为正确的词语作为纠错结果
   
1、 计算字符之间的相似度
- data
    char_meta.txt中保存 IDS中文笔画和拼音数据，全部的字符数据:https://github.com/Aragron-moon/FASPell-EasyUsing
- code
    char_similarity.py 根据 char_meta.txt 计算字符比划和拼音上的相似度

2、soft masked bert文本纠错 复现
- code 代码
   - softMaskBert  softMaskedBert 算法复现
   
   
参考：
[1]基于规则 https://github.com/hiyoung123/YoungCorrector
[2] FASPell CSC
[3] 
