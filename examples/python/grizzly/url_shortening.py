import json
import numpy as np
import pandas as pd
import seaborn as sb

path = 'data/usagov_bitly_data2013-05-17-1368810603.txt'
records = [json.loads(line) for line in open(path)]

frame = pd.DataFrame(records)

cframe = frame[frame.a.notnull()]
cframe['tz'] = cframe['tz'].fillna('Missing')
cframe['tz'][cframe['tz'] == ''] = 'Unknown'
cframe['os'] = np.where(cframe['a'].str.contains('Windows'),
                        'Windows', 'Not Windows')

by_tz_os = cframe.groupby(['tz', 'os'])
agg_counts = by_tz_os.size().unstack().fillna(0)

indexer = agg_counts.sum(1).argsort()
agg_counts = agg_counts.take(indexer[-10:])
agg_counts = agg_counts.stack()
agg_counts.name = 'total'
agg_counts = agg_counts.reset_index()

def norm_total(group):
    group['normed_total'] = group.total / group.total.sum()
    return group

results = agg_counts.groupby('tz').apply(norm_total)

sb.barplot(x='normed_total', y='tz', hue='os',  data=results)
sb.plt.show()
