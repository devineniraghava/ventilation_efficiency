# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 10:11:42 2020
TO load all the data related to Vdot and organise in such a way that the final Vdot 
vlaue fot main evaluation is evaluated

There is also a previous version of this code which works fine with ESHL data
For reference u can see this code too
@author: Devineni
"""
import pandas as pd
import numpy as np
from statistics import mean
import time
import datetime as dt
import matplotlib.pyplot as plt
from tabulate import tabulate

# import mysql.connector
import os
import pymysql
from sqlalchemy import create_engine

from easygui import *
import sys

def prRed(skk): print("\033[31;1;m {}\033[00m" .format(skk)) 


from uncertainties import ufloat
engine = create_engine("mysql+pymysql://root:Password123@localhost/",pool_pre_ping=True)

#%% Selection Message box
'''
This section deals with taking input selection of the experiment
easygui module was used to create the dialogue boxes for easy input
this is just a more visual way for experiment selection
'''

msg ="Please select a Location/Season you like to analyze"
title = "Season selection"
choices = ["ESHL_summer", "ESHL_winter", "CBo_summer", "CBo_winter"]
database = choicebox(msg, title, choices)


times = pd.read_excel('C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/excel_files/Times_thesis.xlsx', sheet_name= database)

msg ="Please select an experiment you would like to analyse in {database}".format(database = str(database))
title = "Experiment selection"
choices = list(times['short name'])
experiment = choicebox(msg, title, choices)


z = int(times[times['short name'] == experiment].index.values)
Vdot_sheets = {"ESHL_summer":"ESHL_Vdot", "ESHL_winter":"ESHL_Vdot", "CBo_summer":"CBo_Vdot", "CBo_winter":"CBo_Vdot"}


t0 = times.loc[z,"Start"]
tn = times.loc[z,"End"]
#%%
'''
This code extracts the correct value of Vdot volume in m3 hr-1 required for 
the experiment based on svens paper reference to be updated
for now this is only for intensive ventilation. This is to be further automated
for entire selection
'''
if Vdot_sheets[database] == "ESHL_Vdot":

    Vdot = pd.read_excel("C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/excel_files/Vdot_results.xlsx", sheet_name = Vdot_sheets[database])
    
    Kü_20_sup = ufloat(Vdot.at[0,'Vdot_sup'], Vdot.at[0,'Vdot_sup_uncertainity'])
    
    d = {}
    
    for i in range(len(Vdot)):
        d[Vdot.loc[i,"Level"] + "_sup"] = ufloat(Vdot.at[i,'Vdot_sup'], Vdot.at[i,'Vdot_sup_uncertainity'])
        d[Vdot.loc[i,"Level"] + "_exh"] = ufloat(-Vdot.at[i,'Vdot_exh'], Vdot.at[i,'Vdot_exh_uncertainity'])
    
    x = pd.DataFrame(d, index=["Vdot"])
    x = x.transpose()
    
    '''
    Form the results excel sheet, the Vdot required for out experiment is calculated below
    '''
    
    
    i = z
    
    wz = int(times.at[i,'Volume flow (SZ, WZ)'])
    bd = int(times.at[i,'Volume flow (BD)'])
    ku = int(times.at[i,'Volume flow (Kü)'])
    ku_ex = int(times.at[i,'Volume flow (Kü_exhaust)'])
    print(times.at[i,'Name'])
    
    
    a = max(x.at['SZ02_'+ str(wz) +'_sup','Vdot'] + x.at['WZ_'+ str(wz) +'_sup','Vdot'] + x.at['BD_'+ str(bd) +'_sup','Vdot'], x.at['SZ01_'+ str(wz) +'_exh','Vdot'] + x.at['Kü_'+ str(ku) +'_exh','Vdot'] + x.at['BD_'+ str(bd) +'_exh','Vdot'] + x.at['Kü_Ex_'+ str(ku_ex) +'_exh','Vdot']) #
    
    b = max(x.at['SZ02_'+ str(wz) +'_exh','Vdot'] + x.at['WZ_'+ str(wz) +'_exh','Vdot'] + x.at['BD_'+ str(bd) +'_exh','Vdot'] + x.at['Kü_Ex_'+ str(ku_ex) +'_exh','Vdot'], x.at['SZ01_'+ str(wz) +'_sup','Vdot'] + x.at['Kü_'+ str(ku) +'_sup','Vdot'] + x.at['BD_'+ str(bd) +'_sup','Vdot'])
    
    Vdot_imported = (a+b)/2
    
    print(f"Vdot = {Vdot_imported}\n")
    level = "wz={wz}_ku={ku}_bd={bd}_kuexh={ku_ex}".format(wz=wz,ku=ku,bd=bd,ku_ex=ku_ex)

else:
    print(times.at[z,'Name'])
    Vdot = pd.read_excel("C:/Users/Devineni/OneDrive - bwedu/MA_Raghavakrishna/1_Evaluation/excel_files/Vdot_results.xlsx", sheet_name = Vdot_sheets[database])

    d = {}

    for i in range(len(Vdot)):
        d[Vdot.loc[i,"Level"] + "_sup"] = ufloat(Vdot.at[i,'Vdot_sup'], Vdot.at[i,'Vdot_sup_uncertainity'])
        d[Vdot.loc[i,"Level"] + "_exh"] = ufloat(-Vdot.at[i,'Vdot_exh'], Vdot.at[i,'Vdot_exh_uncertainity'])
    
    x = pd.DataFrame(d, index=["Vdot"])
    x = x.transpose()
    
    sz = times.at[z,'Volume flow (SZ)']
    k1 = times.at[z,'Volume flow (K1)']
    k2 = times.at[z,'Volume flow (K2)']
    ex = int(times.at[z,'Volume flow (BD)'])
    
    x.loc["BD_0_exh", "Vdot"] = ufloat(0,0)
    x.loc["BD_100_exh", "Vdot"] = ufloat(47.4,12) # data given from sven uncertainity is selected as average of uncertainities of other sensors
    
    
    
    a = max(x.at['K1_'+ str(k1) +'_sup','Vdot'] + x.at['K2_'+ str(k2) +'_sup','Vdot'], x.at['SZ_'+ str(sz) +'_exh','Vdot'] + x.at['BD_'+ str(ex) +'_exh','Vdot']) #
    
    b = max(x.at['K1_'+ str(k1) +'_exh','Vdot'] + x.at['K2_'+ str(k2) +'_exh','Vdot'] + x.at['BD_'+ str(ex) +'_exh','Vdot'], x.at['SZ_'+ str(sz) +'_sup','Vdot'] )
    
    
    Vdot_imported = (a+b)/2
    level = times.loc[z,"short name"]
    print(f"Vdot = {Vdot_imported}\n")
#%%


























