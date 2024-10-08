---
layout: post
title: python|练习统计出现最多的十个词
categories: [python]
description: python练习统计出现最多的十个词，用到列表，字典
keywords: python, top10词统计
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---
从文件中找出出现频次最多的10个词

## 1、问题描述

这是一道python面试题：

“一个可读文件，有一万行，一行只有一个单词，单词可以重复的，求出这一万行中出现频繁次数最多的前10个单词”

## 2、解题思路

 先读取文件变为列表，再用集合去重得到一个参照的列表，逆排序取前10（最大即最多的的10个元素），再用参照列表中的每个元素从文件中去统计，把参照列表中的元素作为键，统计到的结果为值，放入字典，打印出来。

## 3、代码示例

```python
#!/usr/bin/python
#coding:utf-8
all_C = []
with open("words.txt",'r') as f:
    for line in f.readlines():
        all_C.append(line)
#获取无重复元素
all_set=set(sorted(all_C))
#统计为字典
counts={}
for key in all_set:
     counts[key] = all_C.count(key)
#获取前10个元素的个数变为列表
tens = sorted(counts.values(),reverse=True)[0:11]
print tens
#统计最终前十的元素及出现次数
tendict = {}
for k in counts.keys():
    if counts[k] in tens:
        tendict.setdefault(counts[k],k.strip("\n"))
print("出现最多的10个词为:%s \n") %tendict
```

另存脚本为:tens.py,执行如图：

![202407230601.png](/images/202407230601.png)

练习的文件类似 如下10001行，以文件的方式读取还是很快的：

![202407230602.png](/images/202407230602.png)

## 5、示例代码二

```python
#!/usr/bin/python
#coding:utf-8
result= {}
with open("words.txt",'r') as fopen:
    fopen.seek(0,2)
    all = fopen.tell()
    fopen.seek(0,0)
    while fopen.tell() < all:
        lines = fopen.readline().strip()
        if lines in result:
            result[lines] += 1
        else:
            result[lines] = 1
print(sorted(result.items(),key=lambda k:k[1],reverse=True)[:11])
```

以上代码执行效果：

![202407230603.png](/images/202407230603.png)

## 6、总结

示例代码一为自己写的，完全用于练习python学习，有点lower，方法二相对高大上！还有更好的方法吗？
