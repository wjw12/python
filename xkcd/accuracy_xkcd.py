import numpy as np
import matplotlib.pyplot as p

sigma = 2
labels = ['-7$\sigma$','-3$\sigma$','-$\sigma$','$\sigma$','3$\sigma$','7$\sigma$']
xticks = [-5*sigma,-2*sigma,-0.8*sigma,0.8*sigma,2*sigma,5*sigma]

def norm(x):
	return 1/(np.sqrt(2*np.pi)*sigma)*np.exp(-x**2/sigma**2)

p.xkcd()
ax = p.subplot(111)
#set ticks and spines and limits
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['top'].set_color('none')
ax.set_xticks([])
ax.set_yticks([])
p.xticks(xticks,labels)
ax.set_xlim([-5.1*sigma,5.1*sigma])
ax.set_ylim([0,0.24])
#plot
x = np.linspace(-7,7,500)
y = norm(x)
ax.plot(x,y,color='black')
#fill color
x = np.linspace(-0.8*sigma,0.8*sigma,100)
xarray = np.hstack((x,[0.8*sigma,-0.8*sigma]))
yarray = np.hstack((norm(x),[0,0]))
ax.fill(xarray,yarray,'r',alpha=0.45)
x = np.linspace(-2*sigma,2*sigma,200)
xarray = np.hstack((x,[2*sigma,-2*sigma]))
yarray = np.hstack((norm(x),[0,0]))
ax.fill(xarray,yarray,'b',alpha=0.22)
#text and annotate
astyle = dict(arrowstyle = '->')
ax.annotate('biology',xy=(0,0.15),xytext=(1.5,0.18),size='large',
	arrowprops=astyle)
ax.text(-1.2,0.21,'physics',size='large')
ax.annotate('',xy=(-2*sigma,0.21),xytext=(-1.2,0.21),arrowprops=astyle)
ax.annotate('',xy=(2*sigma,0.21),xytext=(1.4,0.21),arrowprops=astyle)
ax.plot([-2*sigma]*2,[0,0.21],'--',color='grey')
ax.plot([2*sigma]*2,[0,0.21],'--',color='grey')
p.xlabel('<--------------------particle physics-------------------->',size='large')
p.title('accuracy',size='large')
p.show()
