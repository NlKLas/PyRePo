
# coding: utf-8

# This is gonna be a module providing basic evaluation techniques, also as script?
# 
# Name: DataAnalysis ?

# In[ ]:

# ToDo
#
# functions
# fits
# read data files
# create tables
# create plots
# constants
# imports ?
# 


# In[1]:

import numpy as np


# In[14]:

# theoretical functions

def gauss(x,μ,σ):
    return (2 * σ**2)**-0.5 * np.exp((x - μ)**2 / (2 * σ**2))

def poly(x,*k):
    print(k)
    return sum ([ k[i] * x**i for i in k ] )

def lin(x,m,b):
    return m * x + b


# In[16]:

#poly(5,1,1,1,1)


# In[95]:

# creating LaTeX table

import sys

table_count = 0

class Table:
    
    def __init__(self,data,rownames,columnnames,caption=''):
        self.data = data
        self.rownames = rownames
        self.columnnames = columnnames
        self.caption = caption
        sys.modules[__name__].table_count += 1
        self.__table_number = sys.modules[__name__].table_count
    
    def create(self,scale=1,colsep='12pt',rowsep='1.2',color='gray!12'):
        code = r'''	\setlength{\tabcolsep}{'''+ colsep + r'''}
	\renewcommand{\arraystretch}{''' + rowsep + r'''}
	\begin{table}[ht]
		\rowcolors{2}{''' + color + r'''}{''' + color + r'''}
		\centering
		\scalebox{''' + str(scale) + r'''}{
		\begin{tabular}{>{\cellcolor[gray]{0.83}}r@{\hskip 3pt}|*{''' + str(len(self.data[0])) + r'''}{c!{\color{gray!25}\vrule width 0.1mm}}}
			\rowcolor[gray]{0.83}
			''' + self.rownames[0]
        for j in range(len(self.columnnames)):
            code = code + ' & ' + self.columnnames[j]
        code = code + r''' \\         
			\hline
			'''
        for i in range(len(self.data)-1):
            code = code + self.rownames[i + 1]
            for j in range(len(self.data[0])):
                code = code + ' & ' + str(self.data[i][j])
            code = code + r''' \\             
			\noalign{\color{gray!25}\hrule height 0.1mm}
			'''
        code = code + self.rownames[len(self.data)]
        for j in range(len(self.data[len(self.data)-1])):
            code = code + ' & ' + str(self.data[len(self.data)-1][j])
        code = code + r''' \\         
		\end{tabular}}
		\caption{''' + self.caption + '''}
	\end{table}'''
        self.table = code
        
    def save(self,filename):
        with open('table' + str(self.__table_number) + '_' + filename + '.tex', 'w') as f:
            f.write(self.table)
            f.close()


# In[96]:

t = Table([[1,2],[3,4]],['test table','v1','v2'],['m1','m2'])
t.create()
t.save('test')


# In[ ]:



