import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


class_num = 3
iter_num = 500

# 读取文件
datafile = u'./data/k_input.xlsx'  # 文件所在位置，u为防止路径中有中文名称，此处没有，可以省略
outfile = u'./data/k_output.xlsx'  # 设置输出文件的位置
data = pd.read_excel(datafile)  # datafile是excel文件，所以用read_excel,如果是csv文件则用read_csv
d = DataFrame(data)
d.head()

# 聚类
mod = KMeans(n_clusters=class_num, n_jobs=4, max_iter=iter_num)  # 聚成3类数据,并发数为4，最大循环次数为500
mod.fit_predict(d)  # y_pred表示聚类的结果

# 聚成3类数据，统计每个聚类下的数据量，并且求出他们的中心
r1 = pd.Series(mod.labels_).value_counts()
r2 = pd.DataFrame(mod.cluster_centers_)
r = pd.concat([r2, r1], axis=1)
r.columns = list(d.columns) + [u'类别数目']
print(r)

# 给每一条数据标注上被分为哪一类
r = pd.concat([d, pd.Series(mod.labels_, index=d.index)], axis=1)
r.columns = list(d.columns) + [u'聚类类别']
print(r.head())
r.to_excel(outfile)  # 如果需要保存到本地，就写上这一列



ts = TSNE()
ts.fit_transform(r)
ts = pd.DataFrame(ts.embedding_, index=r.index)



a = ts[r[u'聚类类别'] == 0]
plt.plot(a[0], a[1], 'r.')
a = ts[r[u'聚类类别'] == 1]
plt.plot(a[0], a[1], 'go')
a = ts[r[u'聚类类别'] == 2]
plt.plot(a[0], a[1], 'b*')
plt.show()

