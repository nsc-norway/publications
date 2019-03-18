import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import calendar
import pubdb

data = pubdb.get_number_per_year()
num_publications = [d[1] for d in data]
for y, p in data:
    print str(y) + "\t" + str(p)
years = [d[0] for d in data]
N = len(data)
today = date.today()

if today.month < 3:
    show_orange_n_years = 2
else:
    show_orange_n_years = 1

ind = np.arange(N)    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence
figsize = (12, 5.5)
plt.figure(figsize=figsize)

p1 = plt.bar(ind, num_publications, width, color=(
    ('r',) * (N - show_orange_n_years) + ('#FF8533', '#FF8533')))

plt.ylabel('# of publications', fontsize=15)
plt.title('Peer-reviewed articles based on data delivered by the NSC',
          fontsize=20, weight='bold')

if str(today.year) == years[-1]:
    if today.month < 12:
        years[-1] += "\n(until " + calendar.month_name[today.month] + ")"

plt.xticks(ind + width / 2. - 0.3, years, fontsize=15)
plt.yticks(np.arange(0, 110, 5))
plt.ylim((0, 110))


# Labels above the bar
for rect in p1:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., height + 1,'%d' % int(height), ha='center', va='bottom')


# based on number of pixels we want
dpi = max(719 / figsize[0], 333 / figsize[1])
#plt.savefig('papers_per_year_{:%Y_%m_%d}.png'.format(today), dpi=dpi)
plt.savefig('papers_per_year.png', dpi=dpi, transparent=True)
plt.show()
