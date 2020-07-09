#!/usr/bin/env python3
import cricbase as cr
import sys
import matplotlib.pyplot as plt
if len(sys.argv)<5:
    print('Read the manual file and provide appropiate argument')
elif len(sys.argv)==5:  
    game_name=input('game name:')
    toss=input('Toss:')
    if toss==sys.argv[1]:
        pass
    else:
        sys.argv[1],sys.argv[2]=sys.argv[2],sys.argv[1]
    plt.style.use('fivethirtyeight')
    plt.xlabel('bowl')
    plt.ylabel('run')
    #fig,ax=plt.subplots()
    print('1st innings')
    for num in range(2):  
        game=cr.Game(sys.argv[num+1],sys.argv[-2],sys.argv[-1])
        game.create_table()
        game.play(num,sys.argv[1])
        i=1
        for name,run,six,four in game.show_data():
            print('{}.{}  {}  6({})  4({})'.format(i,name,run,six,four))
            i+=1
        x=[]
        y=[]
        b=[]
        p=[]
        i=1
        for bowl,run,out in game.graph_data():
            x.append(bowl)
            y.append(run)
            if out==i:
                b.append(bowl)
                p.append(run)
                i+=1 
		             
        plt.scatter(b,p,color='red',s=100)  
        label=sys.argv[num+1] 
        if num==0:
            color='#E3F20D'
            aplha=0.5
            linewidth=1.5
            
        else:
            color='green'
            aplha=0.5
            linewidth=1.5   
        plt.plot(x,y,color=color,alpha=aplha,linewidth=linewidth,label=label) 
        if num<1:
            print('\n\n\n\n')
            print('2nd innings')
        game.close()
    plt.title('{}'.format(game_name))
    plt.legend()
    plt.tight_layout()  
    plt.savefig('{}_match_info.png'.format(game_name))
    plt.show()	
else:
    print('inappropiate argument provided')	
