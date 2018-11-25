# 作业2综述
Assignment 2采取在线competition形式，任务为中文命名实体识别，任务要求使用自然语言处理、机器学习方法识别出test集中的命名实体。Competition期间可在线提交预测结果，leaderbord会实时更新排名。Competition结束后需要在两天内将代码和说明文档提交至ftp服务器，我们会根据leaderboard排名和大家提交的文档来确定作业2的最终成绩。

# 背景介绍
NER（Named Entity Recognition，命名实体识别）又称作专名识别，是自然语言处理中常见的一项任务，使用的范围非常广。命名实体通常指的是文本中具有特别意义或者指代性非常强的实体，通常包括人名、地名、机构名、时间、专有名词等。NER系统就是从非结构化的文本中抽取出上述实体，并且可以按照业务需求识别出更多类别的实体，比如产品名称、型号、价格等。因此实体这个概念可以很广，只要是业务需要的特殊文本片段都可以称为实体。
在本次作业中，我们的任务就是从已经分好词的中文文本中识别出人名（PERSON）、地点（LOCATION）、时间（TIME）及机构名（ORGANIZATION）。

# 数据格式
举例来说，训练数据中的第一条为"他/O 说/O :/O 中国/B-ORGANIZATION 政府/O-ORGANIZATION 对/O 目前/B-TIME 南亚/B-LOCATION 出现/O 的/O 核军备/O 竞赛/O 的/O 局势/O 深感/O 忧虑/O 和/O 不安/O 。/O 我们/O 郑重/O 呼吁/O 南亚/B-LOCATION 有关/O 国家/O 保持/O 最/O 大/O 限度/O 的/O 克制/O ,/O 立即/O 放弃/O 核武器/O 发展/O 计划/O ,/O 避免/O 局势/O 进一步/O 恶化/O ,/O 以利/O 南亚/B-LOCATION 地区/O-LOCATION 的/O 和平/O 与/O 稳定/O 。/O" 其中，各个单元以空格分隔开来，每个单元以“/"分隔出文本内容及对应的标签。在本例中出现了地点实体：“南亚/B-LOCATION ”及南亚/B-LOCATION 地区/O-LOCATION、机构实体“中国/B-ORGANIZATION 政府/O-ORGANIZATION”和时间实体“目前/B-TIME”。

# 标注体系
本次作业的数据集采用了“BIO”标注体系，对于一个实体（一个文本片段）而言，“B-”表示该实体的开始，“O-”表示该实体的结束，“I-”表示该实体的中间部分，如“中国/B-ORGANIZATION 政府/O-ORGANIZATION”、“包头/B-ORGANIZATION 二/I-ORGANIZATION 院/O-ORGANIZATION”。如果单个词语构成一个实体，则只有以“B-”开始的标注信息，如：“南亚/B-LOCATION”。单独的“O”标签表示该词非实体，如“保持/O 最/O 大/O 限度/O”。

# 评分计算方式
在实体识别任务中，我们采用micro F1-score作为评分依据。由于实体识别中，标签具有相关性，因此我们的评分是基于实体片段进行，而非单个词语的标签。
举例来说，对于一个真实标签为["O", "B-ORGANIZATION", "I-ORGANIZATION", "O-ORGANIZATION", "O", "O", "B-TIME", "B-PERSON", "O-PERSON", "O", "O"]的句子序列，我们将其转换为文本片段的标签，即为[("ORGANIZATION", (1, 3)), ("TIME", (6, 6)), ("PERSON", (7, 8))]。如果对应的预测标签序列为["O", "B-ORGANIZATION", "O-ORGANIZATION", "O", "B-TIME", "O-TIME", "B-TIME", "B-PERSON", "O-PERSON", "O", "O"]，我们将其转换为文本片段的标签，即为[("ORGANIZATION", (1, 2)), ("TIME", (4, 5)), ("TIME", (6, 6)), ("PERSON", (7, 8))]。
之后基于文本片段（实体）的标签计算得分：
 - 对于机构类实体（ORGANIZATION），真实值为[(1, 3)]，预测值为[(1, 2)]，因此TP=0，FP=1，FN=1；
 - 对于时间类实体（TIME），真实值为[(6, 6)]，预测值为[(4, 5), (6, 6)]，因此TP=1，FP=1，FN=0；
 - 对于人名类实体（PERSON），真实值为[(7, 8)]，预测值为[(7, 8)]，因此TP=1，FP=0，FN=0。
 
| 实体类型 | ORGANIZATION | TIME | PERSON | 总数 |
|:------:| :------:| :------: | :------: | :------: |
|TP| 0 | 1 | 1 | 2 |
|FP| 1 | 1 | 0 | 2 |
|FN| 1 | 0 | 0 | 1 |
因此上述总体的precision=TP/(TP+FP)=2/(2+2)=1/2，recall=TP/(TP+FN)=2/(2+1)=2/3，micro F1-score=2\*precision\*recall/(precision+recall)=0.5714。

具体计算逻辑可以参见脚本metrics.py。

# 提交格式
提交的预测结果中每行对应测试数据中相应行数的测试样例。每行预测中的标签和测试数据中的各个词相对应，并用一个半角空格隔开，提交数目不对应则提交无效。
提交样例文件参见sample.test.prediction.txt，对应sample.test.content.txt的预测结果。

# Competition提交地址
http://114.212.189.62:12345/

# Competition截止日期
2018-12-02 23:59:59

# FTP提交地址
ftp://114.212.190.181/, username和password为nlp2018

# FTP截止日期
2018-12-04 23:59:59

