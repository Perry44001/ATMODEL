## ATFTdata_20240803_V1.0_flattened_cleaned.json 是所有的json clean清除不正确格式（json中不包含'instroduction'、'input'、'output'中任意一个，训练样本数12605个），并把所有json平铺为一个json的ATFT数据集。

转移到远程后，文件名变为了ATFTdata_20240803_V1.2_flattened_cleaned.json

## ATFTdata_20240804_V1.0_flattened_cleaned.json 是第1、4版和lzx版（lzx评审过的数据，训练样本数6320个），并把所有json平铺为一个json的ATFT数据集。

## ATFTdata_20240806_V1.0_flattened_cleaned.json 是原始数据（lzx评审过的数据，训练样本数436个），并把所有json平铺为一个json的ATFT数据集。

2024年8月7日，对数据集进行整编

理由：原始数据集中对问题的回答是否冗余？什么类型的数据适合gpt微调？什么样的数据适合训练？

按照问题来分，可以分为
* 水声知识相关问题 UA
* 声学工具箱问题   AT
* 代码问题        CD
* 数据集问题      DS
按照长短来分，可以分为
* 长回答 >200个字 L
* 中回答 100~200字M
* 短回答 <100字   S
按照是否有链接分
* 有链接          H
* 无链接          N
命名规则
UA_L_H.json 水声知识长有链接问题