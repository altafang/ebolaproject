#!/usr/bin/python 

import os, sys
import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar 
from matplotlib.figure import Figure 
from matplotlib.legend_handler import HandlerLine2D

def plot_output(out_noiv_file="out_noiv.csv", out_iv_file="out.csv", \
                figure_file="out.png"):
    my_matrix = np.loadtxt(out_noiv_file, delimiter = ',',skiprows=1)
    my_matrix2 = np.loadtxt(out_iv_file, delimiter = ',',skiprows=1)

    f, axarr = plt.subplots(2, 2)

    ploty = [my_matrix[:,3], my_matrix[:,5],my_matrix[:,7],my_matrix[:,9],my_matrix[:,3]+my_matrix[:,5]+my_matrix[:,7]+my_matrix[:,9]]
    plotx = [my_matrix2[:,3], my_matrix2[:,5],my_matrix2[:,7],my_matrix2[:,9],my_matrix2[:,3]+my_matrix2[:,5]+my_matrix2[:,7]+my_matrix2[:,9]]
    labels = ['E', 'I', 'H', 'F', 'Total']

    for ploty_arr, label in zip(ploty, labels):
        axarr[0, 0].plot(my_matrix[:,0], ploty_arr, label=label)
        
    for plotx_arr, label in zip(plotx, labels):	
        axarr[1, 0].plot(my_matrix2[:,0], plotx_arr, label=label)

    axarr[0, 0].set_title('Ebola Infections Reported Over Time - No Intervention')
    axarr[0, 0].set_xlabel('Time [days]')
    axarr[0, 0].set_ylabel('Number Infected')
    axarr[0,0].legend(loc=0)

    axarr[0, 1].plot(my_matrix[:,0], my_matrix[:,1],label='Suscept')
    axarr[0, 1].set_title('Ebola Susceptibilty Data - No Intervention')
    axarr[0, 1].set_xlabel('Time [days]')
    axarr[0,1].set_ylabel('Number Susceptibility')
    axarr[0,1].legend(loc=0)
        
    axarr[1, 0].set_title('Ebola Infections Reported Over Time - Optimized Interventions')
    axarr[1, 0].set_xlabel('Time [days]')
    axarr[1, 0].set_ylabel('Number Infected')
    axarr[1,0].legend(loc=0)

    axarr[1, 1].plot(my_matrix2[:,0], my_matrix2[:,1],label='Suscept')
    axarr[1, 1].set_title('Ebola Susceptibilty Data - Optimized Interventions')
    axarr[1, 1].set_xlabel('Time [days]')
    axarr[1,1].set_ylabel('Number Susceptibility')

    #figManager = plt.get_current_fig_manager()
    #figManager.window.showMaximized()
    plt.legend()
    fig = plt.gcf()
    fig.canvas.set_window_title('Ebola Data Projections For Country Chosen')
    plt.savefig(figure_file)
    plt.show()
