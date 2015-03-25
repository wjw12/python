import numpy as np
import matplotlib.pyplot as p

p.xkcd()
ax = p.subplot(111)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.set_ylim([0,70])
ax.xaxis.set_ticks_position('bottom')
ax.set_xticks([1,2,3,4,5,6])
ax.set_xlim([.5,6.5])
p.yticks([])
p.annotate('THIS IS WHERE I AM NOW',xy=(4,16),
	arrowprops=dict(arrowstyle='->'),xytext=(1,20),size='large')
data = np.linspace(0,7,200)
ax.plot(data,np.exp2(data))
ax.plot(data,70-np.exp2(data),color='green')
ax.plot([4,4],[0,100],'--',color='grey')
p.xlabel('weeks since the semester begins',size='large')
ax.text(5.7,50,'amount of\nhomework',color='blue',size='large')
ax.text(4,53,'leisure time',color='green',size='large')
p.show()
