import numpy as np
import matplotlib.pyplot as plt


N = 7
menMeans   = (4, 7, 15, 40, 50, 41, 4)
ind = np.arange(N)    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence
plt.figure(figsize=(12,5))

p1 = plt.bar(ind, menMeans, width, color=('r','r','r','r','r','#FF8533','#FF8533'))

plt.ylabel('# of publications', fontsize=15)
plt.title('Peer-reviewed articles based on data delivered by the NSC', fontsize=20, weight='bold')
plt.xticks(ind+width/2., ('2009', '2010', '2011', '2012', '2013', '2014', '2015'), fontsize=15 )
plt.yticks(np.arange(0,55,5))



#plt.show()
#plt.savefig('papers_per_year_2015_02_report.png',dpi=200)

