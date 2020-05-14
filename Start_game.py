#!/usr/bin/env python3
import cricket as cr
import sys
import matplotlib.pyplot as plt
if len(sys.argv)<2:
    print('provide game name')
elif len(sys.argv)==2:    
    game=cr.Game(sys.argv[1])
    game.create_table()
    game.play()
    i=1
    for name,run,six,four in game.show_data():
        print('{}.{}  {}  {}  {}'.format(i,name,run,six,four))
        i+=1
    x=[]
    y=[]
    b=[]
    p=[]
    i=1
    plt.style.use('fivethirtyeight')
    for bowl,run,out in game.graph_data():
        x.append(bowl)
        y.append(run)
        
        if out==i:
            b.append(bowl)
            p.append(run)
            i+=1
	    
    plt.plot(x,y) 
    plt.scatter(b,p,color='red',s=100)
    plt.xlabel('bowl')
    plt.ylabel('run')
    plt.title('{}'.format(sys.argv[1]))  
    plt.savefig('{}_match_info.png'.format(sys.argv[1]))
    plt.show()	

    game.close()
else:
    print('inappropiate argument provided')	
