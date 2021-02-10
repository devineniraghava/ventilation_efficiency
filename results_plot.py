# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 15:32:00 2020

@author: Devineni
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from uncertainties import ufloat_fromstr
from uncertainties import ufloat

import xlrd

import pymysql
from sqlalchemy import create_engine

def prRed(skk): print("\033[31;1;m {}\033[00m" .format(skk)) 
import datetime as dt

c = ['#179C7D','#F29400','#1F82C0','#E2001A','#B1C800']
# c = ['#179C7D','#F29400','#1F82C0']*4
#%%
import datetime
import matplotlib.dates as mdates

import matplotlib.units as munits
from pylab import rcParams
rcParams['figure.figsize'] = 7,4.5
plt.rcParams["font.family"] = "calibri"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["font.size"] = 10

font = {'family': 'calibri',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }
df = pd.read_excel("C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/results/results_final.xlsx", sheet_name="plotting")
df1 = df.iloc[:8]  
df2 = df.iloc[8:]
  

#%%
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.0f}%'.format(round(height,0)),
                    xy=(rect.get_x() + rect.get_width() / 4, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        

bdf = pd.read_excel("C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/results/results_final.xlsx", sheet_name="barplot")
bdf1 = bdf.iloc[:8]  
bdf2 = bdf.iloc[8:]
ktbdf = bdf.loc[16:]
rbdf = bdf.loc[0:15]


#%% Ea Bar plot
from matplotlib.lines import Line2D

fig, ax = plt.subplots()
for i in range(0,len(rbdf),4):
    rects1 = ax.bar(rbdf["Measurement"].to_numpy()[i:i+2], rbdf["Ea%"].to_numpy()[i:i+2],yerr=rbdf["std%"].to_numpy()[i:i+2],align='center',color = ['#1F77B4','#FF7F0E'],ecolor='black',capsize=10, edgecolor = c[4])
    rects2 = ax.bar(rbdf["Measurement"].to_numpy()[i+2:i+4], rbdf["Ea%"].to_numpy()[i+2:i+4],yerr=rbdf["std%"].to_numpy()[i+2:i+4],align='center',color = ['#1F77B4','#FF7F0E'],ecolor='black',capsize=10)
    autolabel(rects1)
    autolabel(rects2)

rects3 = ax.bar(ktbdf["Measurement"].to_numpy()[0:2], ktbdf["Ea%"].to_numpy()[0:2],yerr=ktbdf["std%"].to_numpy()[0:2],align='center',color = '#FF7F0E',ecolor='black',capsize=10, edgecolor = c[4])
rects4 = ax.bar(ktbdf["Measurement"].to_numpy()[2:4], ktbdf["Ea%"].to_numpy()[2:4],yerr=ktbdf["std%"].to_numpy()[2:4],align='center',color = '#FF7F0E',ecolor='black',capsize=10)
autolabel(rects3)
autolabel(rects4)


legend_elements = [Line2D([0], [0], marker='o', color='w', label='Balanced case',markerfacecolor='#1F77B4', markersize=10),
                   Line2D([0], [0], marker='o', color='w', label='Exhaust case',markerfacecolor='#FF7F0E', markersize=10),
                   Line2D([0], [0],  color=c[4], label='summer',markerfacecolor='#FF7F0E', markersize=10),
     
                   ]

ax.legend(handles=legend_elements, loc='upper right',  labelspacing = 1)


ax.set_ylabel('Global Air Exchange Efficiency ea')
ax.set_xticks(bdf["Measurement"].to_numpy())
ax.set_xticklabels(bdf["Measurement"].to_numpy(), rotation='vertical')
ax.set_title('ESHL ea comparison for Summer and Winter (All Sensors)')
# ax.yaxis.grid(b=True, color='#C0C0C0', linestyle='-')

ax.axhline(y=50, color = c[0], linestyle='dashed')

fig = plt.gcf() # get current figure
# fig.set_size_inches(22, 9)
# when saving, specify the DPI
plt.tight_layout()
plt.savefig("myplot.png", dpi = 100)

# Save the figure and show
plt.tight_layout()
        

plt.show()    
  
# path = "C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/python_files/plots/Ea_plots/"
# plt.savefig(path+"Ea_bar_plot.png", dpi = 300, bbox_inches='tight')






    
    
      
         
        
#%% Temperature effect on Ea

from uncertainties import unumpy
fig, ax = plt.subplots()

for line in range(0,df1.shape[0]):
        ax.text((df1["Delta T"][line]+0.025), (df1["Ea"][line]), df1["Measurement"][line], horizontalalignment='center', size=12, color='black', weight='normal')      
  
        
df1.plot.scatter("Delta T","Ea",  ax = ax)
        
for i in range(4):
    plt.errorbar(df1.iloc[[i,i+4],:]["Delta T"].to_numpy(), df1.iloc[[i,i+4],:]["Ea"].to_numpy(),df1.iloc[[i,i+4],:]["std"].to_numpy(), capsize = 4, label = df1.iloc[i]["Measurement"][2:6])
plt.ylim(0.2,0.8)
ax.axhline(0.5,color = c[0], linestyle='dashed')

plt.legend()

plt.show() 
 
# path = "C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/python_files/plots/Ea_plots/"
# plt.savefig(path+"del_T_vs_Ea_Herdern.png", dpi = 300, bbox_inches='tight')


   #%%%
fig, ax = plt.subplots()

for line in range(0,df2.shape[0]):
        ax.text((df2.iloc[line,:]["Delta T"]+0.025), (df2.iloc[line,:]["Ea"]), df2.iloc[line,:]["Measurement"], horizontalalignment='center', size=12, color='black', weight='normal')      
  
        
df2.plot.scatter("Delta T","Ea",  ax = ax)
        
for i in range(6):
    plt.errorbar(df2.iloc[[i,i+6],:]["Delta T"].to_numpy(), df2.iloc[[i,i+6],:]["Ea"].to_numpy(), df2.iloc[[i,i+6],:]["std"].to_numpy(), capsize =4, label = df2.iloc[i]["Measurement"][2:6])
plt.ylim(0.2,0.8)
plt.xlim(-25,15)
plt.legend()
plt.show()   


# path = "C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/python_files/plots/Ea_plots/"
# plt.savefig(path+"del_T_vs_Ea_ESHL.png", dpi = 300, bbox_inches='tight')        


#%% 1) NTC vs Air age Herdern
fig, ax = plt.subplots()
ax.plot(np.array([0,5]),np.array([0,5]), color = c[0] , label = "Mixed ventilation", linestyle='dashed')


for i in range(len(df1)):
    if "W_" in df1.iloc[i,:]["Measurement"]:
        plt.scatter(df1.iloc[[i],:]["NTC"].to_numpy(), df1.iloc[[i],:]["tau"].to_numpy(), color = df1.iloc[i,:]["color"] , marker=(5, 2), label = "winter")
    else:
        plt.scatter(df1.iloc[[i],:]["NTC"].to_numpy(), df1.iloc[[i],:]["tau"].to_numpy(), color = df1.iloc[i,:]["color"] , label = "summer")

# syntax to not repeat lables
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# path = "C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/python_files/plots/Ea_plots/"
# plt.savefig(path+"NTC_vs_tau_herdern.png", dpi = 300, bbox_inches='tight')

#%% 2) NTC vs Air age ESHL
fig, ax = plt.subplots()
ax.plot(np.array([0,5]),np.array([0,5]), color = c[0] , label = "Mixed ventilation", linestyle='dashed')


for i in range(len(df2)):
    if "W_" in df2.iloc[i,:]["Measurement"]:
        plt.scatter(df2.iloc[[i],:]["NTC"].to_numpy(), df2.iloc[[i],:]["tau"].to_numpy(), color = df2.iloc[i,:]["color"] , marker=(5, 2), label = "winter")
    else:
        plt.scatter(df2.iloc[[i],:]["NTC"].to_numpy(), df2.iloc[[i],:]["tau"].to_numpy(), color = df2.iloc[i,:]["color"] , label = "summer")

# syntax to not repeat lables
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# path = "C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/python_files/plots/Ea_plots/"
# plt.savefig(path+"NTC_vs_tau_ESHL.png", dpi = 300, bbox_inches='tight')

#%% 3) ACH vs Air age Herdern and ESHL
#%%% curve plot
fig, ax = plt.subplots()
x = np.linspace(0.15,2.75,100)

y = 1/(x)
y1 = 1/(2*x)
ax.plot(x,y1, color = c[3], linestyle='dashed')

ax.plot(x,y, color = c[0], linestyle='dashed')


ax.axvline(0.6, color = 'silver', linestyle='dotted', label = "DIN EN 15251")
ax.axvline(0.42, color = '#1F82C0', linestyle='dotted', label = "Herdern DIN 1946-6" )
ax.axvline(0.48, color = '#002060', linestyle='dotted', label = "ESHL DIN 1946-6")


for i in range(len(df)):
    if "Herdern" in df.iloc[i,:]["Measurement"]:
        if "W_" in df.iloc[i,:]["Measurement"]:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["tau"].to_numpy(), color = df.iloc[i,:]["color"] , marker=(5, 2), label = "Herdern winter")
        else:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["tau"].to_numpy(), color = df.iloc[i,:]["color"] , label = "Herdern summer")
    else:
        if "W_" in df.iloc[i,:]["Measurement"]:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["tau"].to_numpy(), color = df.iloc[i,:]["color"] , marker=(5, 2), label = "ESHL winter")
        else:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["tau"].to_numpy(), color = df.iloc[i,:]["color"] , label = "ESHL summer")
# for line in range(0,df.shape[0]):
#         ax.text((df["ACH"][line]), (df["tau"][line]), df["Measurement"][line], horizontalalignment='center', size=12, color='black', weight='normal')      
 

# syntax to not repeat lables
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# path = "C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/python_files/plots/Ea_plots/"
# plt.savefig(path+"ACH_vs_tau_herdern_eshl.png", dpi = 300, bbox_inches='tight')

#%%% log - plot
fig, ax = plt.subplots()
x = np.linspace(0.15,2.75,100)

y = 1/(x)
y1 = 1/(2*x)
ax.plot(x,y1, color = c[3], linestyle='dashed')

ax.plot(x,y, color = c[0], linestyle='dashed')

ax.axvline(0.2, color = 'silver')
ax.axvline(0.4, color = 'silver')
ax.axvline(0.6, color = 'silver', linestyle='dotted', label = "DIN EN 15251")
ax.axvline(0.42, color = '#1F82C0', linestyle='dotted', label = "Herdern DIN 1946-6" )
ax.axvline(0.48, color = '#002060', linestyle='dotted', label = "ESHL DIN 1946-6")
ax.axvline(0.8, color = 'silver')
ax.axvline(1, color = 'silver')
ax.axvline(2, color = 'silver')
ax.axvline(3, color = 'silver')

plt.yscale('log')
plt.xscale('log')
for i in range(len(df)):
    if "Herdern" in df.iloc[i,:]["Measurement"]:
        if "W_" in df.iloc[i,:]["Measurement"]:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["tau"].to_numpy(), color = df.iloc[i,:]["color"] , marker=(5, 2), label = "Herdern winter")
        else:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["tau"].to_numpy(), color = df.iloc[i,:]["color"] , label = "Herdern summer")
    else:
        if "W_" in df.iloc[i,:]["Measurement"]:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["tau"].to_numpy(), color = df.iloc[i,:]["color"] , marker=(5, 2), label = "ESHL winter")
        else:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["tau"].to_numpy(), color = df.iloc[i,:]["color"] , label = "ESHL summer")
# syntax to not repeat lables
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc = "lower left")

# path = "C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/python_files/plots/Ea_plots/"
# plt.savefig(path+"ACH_vs_tau_log.png", dpi = 300, bbox_inches='tight')





#%% ACH vs EAi

fig, ax = plt.subplots()

ax.axvline(0.6, color = 'silver', linestyle='dotted', label = "DIN EN 15251")
ax.axvline(0.42, color = '#1F82C0', linestyle='dotted', label = "Herdern DIN 1946-6" )
ax.axvline(0.48, color = '#002060', linestyle='dotted', label = "ESHL DIN 1946-6")
ax.axhline(50,color = c[0], linestyle='dashed')


for i in range(len(df)):
    if "Herdern" in df.iloc[i,:]["Measurement"]:
        if "W_" in df.iloc[i,:]["Measurement"]:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["Ea%"].to_numpy(), color = df.iloc[i,:]["color"] , marker=(5, 2), label = "Herdern winter")
        else:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["Ea%"].to_numpy(), color = df.iloc[i,:]["color"] , label = "Herdern summer")
    else:
        if "W_" in df.iloc[i,:]["Measurement"]:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["Ea%"].to_numpy(), color = df.iloc[i,:]["color"] , marker=(5, 2), label = "ESHL winter")
        else:
            plt.scatter(df.iloc[[i],:]["ACH"].to_numpy(), df.iloc[[i],:]["Ea%"].to_numpy(), color = df.iloc[i,:]["color"] , label = "ESHL summer")



from scipy.optimize import curve_fit
spl_data = df.loc[:,["Measurement","ACH","Ea"]]
spl_data1 = spl_data.iloc[:8]  
spl_data2 = spl_data.iloc[8:]
spl_data1 = spl_data1.sort_values(by=['ACH'])
spl_data2 = spl_data2.sort_values(by=['ACH'])

def func(x, a, b):
    return a * pow(x,-b) 
xdata  = spl_data1["ACH"].to_numpy()
ydata  = spl_data1["Ea"].to_numpy()

popt, pcov = curve_fit(func, xdata, ydata)
x = np.linspace(0.15,2.75,100)
y = popt[0]*pow(x,-popt[1])

plt.plot(x, y*100, '#1F82C0', label = r'$\mathrm{\varepsilon}^{\mathrm{a}}$' +" Herdern")


xdata  = spl_data2["ACH"].to_numpy()
ydata  = spl_data2["Ea"].to_numpy()


popt, pcov = curve_fit(func, xdata, ydata)
x = np.linspace(0.15,2.75,100)
y = popt[0]*pow(x,-popt[1])

plt.plot(x, y*100, '#002060')





plt.ylim(0,100)
# syntax to not repeat lables
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# path = "C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/python_files/plots/Ea_plots/"
# plt.savefig(path+"ACH_vs_Eai.png", dpi = 300, bbox_inches='tight')



#%%
#%% Temperature effect on Ea













#%%











       