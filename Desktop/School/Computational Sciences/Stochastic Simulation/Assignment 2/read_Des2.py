import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

import scipy.stats as stats
from statsmodels.graphics.gofplots import qqplot


location = r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results2\DES_results_1.csv'
location2 =  r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results2\DES_results_2.csv'
location3 =  r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results2\DES_results_3.csv'




def main():
    df = pd.read_csv(location)
    df2 = pd.read_csv(location2)
    df3 = pd.read_csv(location3)


    
    for lambd in [5,8,9,9.5, 9.9]:
        x = 1
        #tests(df, df2, lambd, 1)
        #df3 = df2.loc[df2['lambda'] == lambd]
        
        #df3 = df3.loc[df3['n_clients'] ==  300000]
        #print('lambd = ', lambd, ': ', stats.shapiro(df3['times']))


     
    
    #make_fig1(df, df2)
    #make_fig2(df, df2)
    #make_fig3(df2)
    
    #plot_std_2(df3)

def make_fig3(df, a1, a2):
  
    fig, axes = plt.subplots(1,2, figsize=(15,5), sharey = False) 
    print(df)
    a1 = axes[0]
    a2 = axes[1]
    
    plot_st(1, df, fig, a1, a2)

def make_fig2(df, df2):
    
    fig, axes = plt.subplots(3,3, figsize=(17,17), sharey = False) 
    a1 = axes[0, 0]
    a2 = axes[0,1]
    a3 = axes[0,2]
    
    a4 = axes[1,0]
    a5 = axes[1,1]
    a6 = axes[1,2]
    
    a7 = axes[2,0]
    a8 = axes[2,1]
    a9 = axes[2,2]
    
    serv = 1

    
    distr(df, 8, serv, fig, a1, y_label = True)
    distr(df, 9.5, serv, fig, a2 )
    distr(df, 9.9, serv, fig, a3)
    
    serv = 2
    
    distr(df, 8, serv, fig, a4, y_label = True)
    distr(df, 9.5, serv, fig, a5 )
    distr(df, 9.9, serv, fig, a6)
    
    serv = 1
    
    distr(df2, 8, serv, fig, a7, text = False, x_label = True, y_label = True)
    distr(df2, 9.5, serv, fig, a8, text = False, x_label  = True )
    distr(df2, 9.9, serv, fig, a9, text = False, x_label = True)
    
    
    plt.show()
    
    
def distr(df, lambd, serv, fig, ax, text = True, x_label = False, y_label = False):
    sns.set_color_codes(palette='deep')
    val = 300000
    df2 = df.loc[df['n_clients'].isin([5000, val])]
    df2 = df2.loc[df2['servers'] == serv]
    df2 = df2.loc[df2['lambda'] == lambd]
    if text == True:
        ax.text(0.8, 0.75, 'FIFO, {} server(s)'.format(serv), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize = '13')
        ax.text(0.8, 0.7, '$\\rho$ = {}'.format(lambd/10), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize = '13')
    else: 
        ax.text(0.8, 0.75, 'Shortest job first', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize = '13')
        ax.text(0.8, 0.7, '1 server'.format(lambd/10), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize = '13')
        ax.text(0.8, 0.65, '$\\rho$ = {}'.format(lambd/10), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize = '13')
    #ax2.text(0.9, 0.5, 'End text', horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)
    

    

        
    ax.tick_params(axis='both', which='major', labelsize=14)
        
    ax1 = sns.histplot(df2, x = 'times', hue = 'n_clients', kde = True ,palette = 'deep', bins = 40, ax = ax, legend = False)

    if x_label == True:
        ax1.set_xlabel('Average waiting times', fontsize = 17)
    else:
        ax1.set_xlabel('')  
        
    if y_label == True:
        ax.set_ylabel('Count', fontsize = 17)
    else:
        ax1.set_ylabel('') 
        
    
def tests(df, df_shortest,  lambd, serv):
    val = 300000
    
    times = []
    print('lambd= ', lambd)
    for i in [1,2,4]:
        df2 = df.loc[df['n_clients'] ==  val]
        df2 = df2.loc[df2['servers'] == i]
        df3 = df2.loc[df2['lambda'] == lambd]
        times.append(df3)
        #print('serv = ', i, ': ', stats.shapiro(df3['times']))
    #sns.displot(df2, x = 'times', hue = 'n_clients', palette = 'deep', bins = 30)
    t1 = (times[0]['times'])
    t2 =  (times[1]['times'])
    t3 = (times[2]['times'])
    print()
    #print('Levenes test')
    
    #print('1 and 2 servers', stats.levene(t1, t2))
    #print('1 and 4 servers',  stats.levene(t1, t3))
    #print('2 and 4 servers',  stats.levene(t2, t3))
    
    print('Welchs t test')
    #print('1 and 2 servers', stats.ttest_ind(t1, t2))
    print('1 and 4 servers',  stats.ttest_ind(t1, t3))
    #print('2 and 4 servers',  stats.ttest_ind(t2, t3))
    
    df_2 = df_shortest.loc[df_shortest['n_clients'] == val]
    df_2 = df_2.loc[df_2['lambda'] == lambd]
    
    print('1 and shortest job first', stats.ttest_ind(t1, df_2['times']))
 
    
def make_fig1(df, df2):
    fig, axes = plt.subplots(3,2, figsize=(18,18), sharey = False) 

    a1 = axes[0, 0]
    a2 = axes[0,1]
    
    a3 = axes[1,0]
    a4 = axes[1,1]
    
    a5 = axes[2,0]
    a6 = axes[2,1]
    
    #ax7 = axes[3, 0]
    #ax8 = axes[3,1]

    
    plot_st(1, df, fig, a1, a2)
    
    plot_st(2, df, fig, a3, a4)
    plot_st(4, df, fig, a5, a6)
    
    
        
    #plot_st(1, df2, fig, ax7, ax8)
    #ax7.set_title('Shortest job first, 1 server', loc = 'left')

    plt.savefig(r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\line_plot2.pdf')
    plt.show()
    #plot_st(1, df)
    #plot_st(2, df)
    #plot_st(4, df)
    
    df2 = df.loc[df['servers'] == 1]
    df2 = df2.loc[df2['lambda'] == 9.9]
    df2 = df2.loc[np.logical_or(df.n_clients == 5000, df.n_clients == 300000)]
    
    
    
def plot_st(server, df, fig, ax1, ax2):


    
    stdevs = {}
    x_axis = [100, 1000, 5000, 10000, 25000, 50000, 100000, 200000, 300000]
    
 
    
    for lambd in  [5, 8, 9, 9.5, 9.9]:
        devs = []
        for cl in [100, 1000, 5000, 10000, 25000, 50000, 100000, 200000, 300000]:
            
            df1 = df.loc[df['n_clients'] == cl]
            df1 = df1.loc[df1['servers'] == server]
            df1 = df1.loc[df1['lambda'] == lambd]
            devs.append( np.std(df1['times']))
            
            #sns.displot(df1, x="times")
            # plt.title('Rho {}, N_clients {} server {}'.format(lambd/10, cl, server))
            #plt.show()
            
        stdevs['{}'.format( lambd)] = devs
        
    for lambd in [5, 8, 9, 9.5, 9.9]:
        ax2.plot(x_axis[2:], stdevs['{}'.format(lambd)][2:], label = '$\\rho$ = {}'.format(lambd/10))
        
    
    
    ax1.set_title('Number of servers = {}'.format(server), loc = 'left', fontsize = 16)
    ax2.set_xlabel('Number of clients', fontsize = 16)
    ax2.set_ylabel('Standard deviation', fontsize = 16)
    ax2.legend(fontsize = 16)
    
    ax1.tick_params(axis='both', which='major', labelsize=13)
    ax2.tick_params(axis='both', which='major', labelsize=13)
    
    
    ax1= sns.lineplot(data=df.loc[df['servers'] ==server], x="n_clients", y="times", hue = 'lambda', palette=[sns.color_palette("hls", 8)[5], 'orange', 'green', 'red',  'purple'],  legend = None, ax=ax1)
    ax1.set_xlabel('Number of clients', fontsize = 16)
    ax1.set_ylabel('Average waiting times', fontsize = 16)
    
def plot_std_2(df):
  
    fig, axes = plt.subplots(3,3, figsize=(23,15), sharey = False, sharex = False) 

    a1 = axes[0, 0]
    a2 = axes[0,1]
    a22 = axes[0,2]
    
    a3 = axes[1,0]
    a4 = axes[1,1]
    a23 = axes[1,2]
    
    a5 = axes[2,0]
    a6 = axes[2,1]
    a24 = axes[2,2]
    
    
    plot3(1, df, fig, a1, a2)
    plot3(2, df, fig, a3, a4)
    plot3(4, df, fig, a5, a6)
    
    distr(df, 9, 1, fig, a22, text = True)
    distr(df, 9, 2, fig, a23)
    distr(df, 9, 4, fig, a24)
    

    plt.show()
    
def plot3(serv, df, fig, ax1 ,ax2):
    stdevs = {}
    x_axis =  [100, 500, 1000, 5000, 10000, 50000, 100000, 200000]
    
    
    for distr in [3, 4]:
        devs = []
        for cl in  [100, 500, 1000, 5000, 10000, 50000, 100000, 200000]:
            
            df1 = df.loc[df['n_clients'] == cl]
            df1 = df1.loc[df1['servers'] == serv]    
            df1 = df1.loc[df1['distr'] == distr]    
            devs.append( np.std(df1['times']))

            
        stdevs['{}'.format(distr)] = devs
        
    
    for distr in [3, 4]:
        if distr == 3:
            ax2.plot(x_axis[2:], stdevs['{}'.format(distr)][2:], label = 'M/D/{}'.format(serv))
        else:
            ax2.plot(x_axis[2:], stdevs['{}'.format(distr)][2:], label = 'M/HE/{}'.format(serv))
    ax2.legend(fontsize =16)
    
    ax1.text(0.8, 0.75, 'FIFO, {} server(s)'.format(serv), horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes, fontsize = '15')
    ax1.text(0.8, 0.7, '$\\rho$ = {}'.format(9/10), horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes, fontsize = '15')

    #ax1.set_title('Number of servers = {}'.format(server), loc = 'left')
    ax2.set_xlabel('Number of clients', fontsize =16)
    ax2.set_ylabel('Standard deviation', fontsize = 16)

    ax2.legend(fontsize= 16)
    
    #ax1= sns.lineplot(data=df.loc[df['servers'] ==server], x="n_clients", y="times", hue = 'lambda', palette=[sns.color_palette("hls", 8)[5], 'orange', 'green', 'red',  'purple'],  legend = None, ax=ax1)
    ax1.set_xlabel('Number of clients', fontsize = 16)
    ax1.set_ylabel('Average waiting times', fontsize = 16)
    
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax2.tick_params(axis='both', which='major', labelsize=14)
    
    ax1.locator_params(axis='x', nbins=5)
    ax2.locator_params(axis='x', nbins=5)
    
     
    #print(df)
  
    ax1 = sns.lineplot(data=df.loc[df['servers'] == serv], x="n_clients", y="times",  palette = [ sns.color_palette()[0], sns.color_palette()[1]], hue = 'distr',  legend = None, ax = ax1)

 
    



    
    

    

if __name__ == '__main__':
    main()