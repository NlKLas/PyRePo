
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
# round
# errors
# constants
# imports ?
# info and print
# 


# In[2]:

import numpy as np
import os
# later hopefully replaced by sympy
get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt


# In[14]:

# theoretical functions

def gauss(x,μ,σ):
    return (2 * σ**2)**-0.5 * np.exp((x - μ)**2 / (2 * σ**2))

def poly(x,*k):
    print(k)
    return sum ([ k[i] * x**i for i in k ] )

def lin(x,m,b):
    return m * x + b


# In[286]:

#poly(5,1,1,1,1)


# In[387]:

# scientifically display numbers

def __convert_unit(unit,sep=r'\;',size=r'\small',textrm=True):
    unit = unit.split()
    bottom = []
    top = []
    if textrm:
        rm1 = r'\textrm{'
        rm2 = '}'
    else:
        rm1 = rm2 = ''
    for u in unit:
        if u.startswith('-'):
            bottom.append(u.strip('-'))
        else:
            top.append(u)
    if not bottom:
        s = ''
        for t in top:
            if t.startswith('10') and t[2:].strip('+').strip('-').isdigit():
                if int(t[2:].strip('+').strip('-')) == 0:
                    continue
                s = '10^{' + t[2:].replace('+','') + '}' + s
                continue
            elif t[0].isdigit():
                t = t + rm2 + '^{'
                while t[0].isdigit():
                    t = t[1:] + t[0]
                t = rm1 + t + '}'
            else:
                t = rm1 + t + rm2
            s = s + t + sep
        s = ('?' + s).strip(sep).strip('?')
    else:
        s = r'\frac{'
        for t in top:
            if t.startswith('10') and t[2:].strip('+').strip('-').isdigit():
                if int(t[2:].strip('+').strip('-')) == 0:
                    continue
                s = '10^{' + t[2:].replace('+','') + '}' + s
                continue
            elif t[0].isdigit():
                t = t + rm2 + '^{'
                while t[0].isdigit():
                    t = t[1:] + t[0]
                t = rm1 + t + '}'
            else:
                t = rm1 + t + rm2
            s = s + t + sep
        s = ('?' + s).strip(sep).strip('?')
        s = s + '}{'
        for b in bottom:
            if b[0].isdigit():
                b = b + rm2 + '^{'
                while b[0].isdigit():
                    b = b[1:] + b[0]
                b = rm1 + b + '}'
            else:
                b = rm1 + b + rm2
            s = s + b + sep
        s = ('?' + s).strip(sep).strip('?')
        s = s + '}'
                
    return '$' + size + ' ' + s + '$'


# error types: (), pm, seperate
def sc(data,Δdata='none',unit='',n=3,errortype='()',fixed_unit=False,max_dim_diff=4):
    data = np.array(data)
    # without errors
    if Δdata == 'none':
        # powers of 10
        dims = np.floor(np.log10(data))
        # one factor for all
        if max(dims)-min(dims) <= max_dim_diff:
            # powers of *3 are not prefered
            if fixed_unit:
                # keep dimensions
                if all(dims <= 2) and all(dims >= 0):
                    ch_dims = 0
                # change dimensions
                else:
                    ch_dims = -min(dims)
            # powers of *3 are prefered
            else:
                print(dims - (min(dims)+1)//3*3)
                # *3 dimensions
                if all(dims - min(dims)//3*3 <= 3):
                    ch_dims = -min(dims)//3*3
                elif all(dims - (min(dims)+1)//3*3 <= 2):
                    ch_dims = -(min(dims)+1)//3*3
                # not *3 dimensions
                else:
                    ch_dims = -min(dims)
        # seperate factors (implicitly fixed unit)
        else:
            ch_dims = dims * ((dims > 2) + (dims < 0))
    # with errors
    else:
        Δdata = np.array(Δdata)
        
                    
    return(ch_dims)
            
            
    
    
    
    
dats = [0.001234678,0.3443342123,3,9.234,324.934893476,234234.56]
#dats = [3.356,12.2345,123.45,4.678,0.34]
print(sc(dats,fixed_unit=0,max_dim_diff=4))
    
#unit = '10-3 nm 2s -K'    
#print('\n',__convert_unit(unit))
#ax = plt.axes([0,0,0.01,0.01])
#ax.set_xticks([])
#ax.set_yticks([])
#plt.text(0.3,0.4,__convert_unit(unit,size='',textrm=0),size=30)


# In[ ]:




# In[8]:

# reading data files

# private
def __read_data(file,sep='\t',decimal_point=True):
    arr = []
    text_arr = []
    data_arr = []
    text_dict = {}
    for line in open(file):
        if not decimal_point:
            arr.append(line.replace(',','.').strip().split(sep))
        else:
            arr.append(line.strip().split(sep))
        try:
            for j in range(len(arr[-1])):
                arr[-1][j] = float(arr[-1][j])
            data_arr.append(arr[-1])
        except ValueError:
            text_arr.append([el.strip('\n').strip() for el in arr[-1]])
            if len(arr[-1]) == 2:
                try:
                    arr[-1][-1] = float(arr[-1][-1])
                    key = arr[-1][0].strip(':').strip()
                    value = arr[-1][-1]
                    if key in text_dict:
                        if type(text_dict[key]) is list:
                            text_dict[key].append(value)
                        else:
                            text_dict[key] = [text_dict[key], value]
                    else:
                        text_dict[key] = value
                except ValueError:
                    pass
    return data_arr,text_arr,text_dict


def import_data(path='Data',sep='\t',decimal_point=True):
    for root, directories, files in os.walk(path):
        n = 0
        ignored_files = []
        data_files = {}
        data = []
        notes = []
        conditions = []
        for file in files:
            if len(file.split('.')) != 1:
                if file.split('.')[-1].lower() not in ['txt','csv','asc','tka']:
                    ignored_files.append(file)
                    continue

            data_arr, text_arr, text_dict = __read_data(path+'/'+file, sep = sep, decimal_point = decimal_point)
            data.append(np.rollaxis(np.array(data_arr),1))
            notes.append(text_arr)
            conditions.append(text_dict)
            data_files['data[%d]'%n] = file
            n += 1

        print('From '+str(root)+' the following files were imported:\n')
        print("{:9} {:11} {:20} {:10} {:10} {:^50.50}\n".format('varname','','filename','shape','conditions','notes'))
        keylist = sorted(data_files.keys())
        n = 0
        for key, value in sorted(data_files.items(), key = lambda key_val: int(key_val[0].strip(']').split('[')[-1])):
            print("{:9} {:11} {:19} {:15} {:6} {:50.50}".format(key, ':', value,
                                                   str(np.shape(data[n])[0])+' x '+str(np.shape(data[n])[1]),
                                                           str(len(conditions[n])),
                                                           ';  '.join([str(note) for note in np.squeeze(notes[n])])))
            n += 1
        print('\nThe following subfolders have been ignored:\n')
        for folder in directories:
            print(folder)
        print('\nThe following files have been ignored:\n')
        for file in ignored_files:
            print(file)
        break
    return data, notes, conditions


# In[ ]:




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
            
            
# imports


# In[96]:

t = Table([[1,2],[3,4]],['test table','v1','v2'],['m1','m2'])
t.create()
t.save('test')


# In[ ]:



