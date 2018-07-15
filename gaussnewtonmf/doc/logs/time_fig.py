
# coding: utf-8

# In[1]:

import  matplotlib
from matplotlib import pyplot as plt
import matplotlib.lines as mlines


# In[2]:

matplotlib.rcParams.update({'font.size': 16})


'''
datas = ['a9a', 'news20', 'webspam']
dataname = {'a9a':'a9a', 'webspam': 'webspam', 'yahoojp':'yahoojp',
            'kddb':'kddb', 'url':'url', 'rcv1':'rcv1', 'news20':'news20',
            'ijcnn1': 'ijcnn', 'avazu-site':'avazu-site', 'criteo':'criteo', 'avazu-app':'avazu-app'}
methods= ['ant', 'sg']
'''
datas = ['ml', 'nf']
dataname = {'ml':'MovieLens', 'nf': 'Netflix'}
methods= ['acg', 'als','apcg','g','pg']
method_label = {'acg':'ANT', 'apcg':'P-ANT','g':'GN','pg':"P-GN", 'als':'ALS'}

showTime={'ml':'1e+4', 'nf': '1e+5'}

nr_threads = [1]
color_map = {'acg':'red', 'als':'blue', 'apcg':'yellow', 'g':'green', 'pg':'black'}
color_sequence = ['#1f77b4', 'orange', 'magenta', '#ffbb78', 'green',
                                    '#98df8a', '#d62728', '#ff9896', 'blue', '#c5b0d5',
                                    '#8c564b', '#c49c94', 'orange', '#f7b6d2', '#7f7f7f',
                                    '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

color_sequence1 = ['#1f77b4', '#8856a7', '#98df8a', '#d62728', '#ff9896', 'magenta', '#8c564b', 'orange', '#c49c94']
marker_map = {128: ('^', 'x'), 1:('s', 'd'), 1/128.0:('p', '*'), 1:('o', '>')}
ant_base = {}
sgd_base = {}



def load_obj_data(file_name):
    ant_x = []
    ant_y = []
    for id,i in enumerate(open(file_name)):
        i=i.split()
        if id==0:
            time_idx=i.index('time')
            obj_idx=i.index('obj')
            continue
        ant_x.append(float(i[time_idx]))
        ant_y.append(round(float(i[obj_idx]),3))
    return ant_x, ant_y

def load_va_data(file_name):
    ant_x = []
    ant_y = []
    for id,i in enumerate(open(file_name)):
        i=i.split()
        if id==0:
            time_idx=i.index('time')
            va_rmse_idx=i.index('va_rmse')
            continue
        ant_x.append(float(i[time_idx]))
        ant_y.append(float(i[va_rmse_idx]))
    return ant_x, ant_y

data_optima = {}
for data in datas:
    y = []
    for method in methods:
        base = '{0}.{1}'.format(data, method)
        print base
        ant_x, ant_y = load_obj_data(base)
        y+= ant_y
    data_optima[data] = min(y)
print data_optima


x_BOUND={'ml':10000,'nf':100000}
def time_upper(time_list, time_upper):
    for i,x in enumerate(time_list):
        if x > time_upper:
            return i


font = {'size': 12}
matplotlib.rc('font', **font)
for data in datas:
    print data
    plt.xlabel('Time:'+showTime[data], fontsize=12)
    plt.ylabel('Difference to Opt. Fun. Value', fontsize=12)
    ant_y = []
    ant_x = []
    line2ds = []
    for method in methods:
        base = '{0}.{1}'.format(data, method)
        ant_x, ant_y = load_obj_data(base)
        optima = data_optima[data]
        upper_idx = time_upper(ant_x, x_BOUND[data])
        ant_x = [x/float(showTime[data]) for x in ant_x[:upper_idx]]
        ant_y = [abs(i-optima)/optima for i in ant_y[:upper_idx]]
        line = mlines.Line2D([], [], ls='-', color=color_map[method], markersize=8, marker=marker_map[1][0],
                             label=method_label[method], linewidth=2.0, markeredgewidth=0.0)
        line2ds.append(line)
        plt.semilogy(ant_x, ant_y, '-', color=color_map[method], linewidth=2.0, marker=marker_map[1][0],
                     markeredgewidth=0.0, markersize=8, markevery=4)

    plt.legend(handles=line2ds, fontsize=12)
    plt.savefig("{0}.obj.eps".format(data), format='eps', dpi=1000)
    plt.show()
    plt.clf()


# In[10]:

def y_bound(arr,val):
    for i,x in enumerate(arr):
        if x<=val:
            return i
def x_bound(arr,val):
    for i,x in enumerate(arr):
        if  x > val:
            return i
y_BOUND={'ml':0.89,'nf':0.96}
x_BOUND={'ml':10000,'nf':100000}
font = {'size': 12}

matplotlib.rc('font', **font)
for data in datas:
    print data
    plt.xlabel('Time:'+showTime[data], fontsize=12)
    plt.ylabel('RMSE', fontsize=12)
    ant_y = []
    ant_x = []
    line2ds = []
    for method in methods:
        base = '{0}.{1}'.format(data, method)
        ant_x, ant_y = load_va_data(base)
        idy=y_bound(ant_y,y_BOUND[data])
        idx=x_bound(ant_x,x_BOUND[data])
        ant_x=[x/float(showTime[data]) for x in ant_x [idy:idx]]
        ant_y=ant_y[idy:idx]
        line = mlines.Line2D([], [], ls='-', color=color_map[method], markersize=8, marker=marker_map[1][0],
                             label=method_label[method], linewidth=2.0, markeredgewidth=0.0)
        line2ds.append(line)
        plt.plot(ant_x, ant_y, '-', color=color_map[method], linewidth=2.0, marker=marker_map[1][0],
                     markeredgewidth=0.0, markersize=8, markevery=4)

    plt.legend(handles=line2ds, fontsize=12)
    plt.savefig("{0}.rmse.eps".format(data,), format='eps', dpi=1000)
    plt.show()
    plt.clf()



