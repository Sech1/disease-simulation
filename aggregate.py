import pandas
import matplotlib.pyplot as plt
import pylab as pl

def main():
    networks = ["rc-","er-","ba-"]
    immuneStrats = ["none-","random-","bc-","friend-","hd-"]
    simTypes = ["-sis.csv","-sir.csv"]


    for network in networks:
        for strat in immuneStrats:
                aggregateValuesSis(network,strat)
                aggregateValuesSir(network,strat)

def aggregateValuesSis(network, immuneStrat):
        
        for x in range(1,11):
            print("results/"+network+immuneStrat+str(x)+"-sis.csv")
            data = pandas.read_csv("results/"+network+immuneStrat+str(x)+"-sis.csv")
            ax = plt.gca()
            data.plot(kind='line',color='red', y='Current infected count',lw=1.3, ax=ax)
            data.plot(kind='line',color='blue', y='Total Immune', lw=1.3, ax=ax)
            data.plot(kind='line',color='orange', y='Newly infected count', lw=1.3, ax=ax)
            data.plot(kind='line',color='green', y='Newly Susceptible', lw=1.3, ax=ax)
            pl.suptitle(network+immuneStrat+str(x)+"-sis")
            plt.savefig("plots/"+network+immuneStrat+str(x)+"-sis.png")
            plt.close()

def aggregateValuesSir(network, immuneStrat):
        for x in range(1,11):
            print("results/"+network+immuneStrat+str(x)+"-sir.csv")
            data = pandas.read_csv("results/"+network+immuneStrat+str(x)+"-sir.csv")
            ax = plt.gca()
            data.plot(kind='line',color='red', y='Current infected count',lw=1.3, ax=ax)
            data.plot(kind='line',color='blue', y='Total Immune Count', lw=1.3, ax=ax)
            data.plot(kind='line',color='purple', y='Recovered', lw=1.3, ax=ax)
            data.plot(kind='line',color='yellow', y='Newly infected count', lw=1.3, ax=ax)
            pl.suptitle(network+immuneStrat+str(x)+"-sir")
            plt.savefig("plots/"+network+immuneStrat+str(x)+"-sir.png")
            plt.close()

if __name__ == '__main__':
    main()  
