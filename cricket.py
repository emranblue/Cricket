import sqlite3 as sql
from collections import Counter as count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fn
class Game:
    def __init__(self,db_name='player',game_name='socks',num_player=4,T_over=2):
        self.game_name=game_name
        self.num_player=num_player
        self.T_over=T_over
        self.db=sql.connect('{}.db'.format(db_name))
        self.cur=self.db.cursor()    
    def create_table(self):
        try:
            self.cur.execute("create table {}(player_name text,run int,six int,four int)".format(self.game_name))
            self.cur.execute("create table {}(run int)".format(self.game_name+'_run'))
            self.cur.execute("insert into {}(run) values(?)",(0))
            self.db.commit()
        except:
            print('game already played,start another new game')
    def gen_player():
        return [[input('player name:'),[]],[input('player name:'),[]]]    
    def new_player():
        return [input('player name:'),[]]  
    def play(self):
        player=Game.gen_player()
        total_out=0
        stat='0'
        strick=0
        non_strick=1
        run=0
        temp=0
        bowl=0
        over=0
        while (over+1<=self.T_over and total_out<self.num_player):
            stat=input('{}/{} over:{}.{} event:({}):: '.format(run,total_out,over,bowl%6,player[strick][0])) 
            if stat=='wd':
                run+=1
                self.cur.execute("update {} set run={}".format(self.game_name+'_run',run))
                self.db.commit()
            elif stat=='nb':
                run+=1  
                self.cur.execute("update {} set run={}".format(self.game_name+'_run',run))
                self.db.commit() 
            elif stat=='4wd' or stat=='4nb':
                run+=5  
                self.cur.execute("update {} set run={}".format(self.game_name+'_run',run))
                self.db.commit()      
            elif stat=='back':
                total=player[strick][1]+player[non_strick][1]
                cut=total.pop()  
                if cut%2==0:
                    player[strick][1].pop()
                else:
                    player[non_strick][1].pop()  
                    temp=non_strick
                    non_strick=strick
                    strick=temp  
                run-=cut
                self.cur.execute("update {} set run={}".format(self.game_name+'_run',run))
                self.db.commit()
                bowl-=1
            elif stat in ('0','1','2','3','4','6'):
                bowl+=1
                over=(bowl//6) 
                run+=int(stat)
                self.cur.execute("update {} set run={}".format(self.game_name+'_run',run))
                self.db.commit()
                if int(stat)%2:
                    player[strick][1].append(int(stat))
                    if bowl%6==0:
                        pass
                    else:
                        temp=non_strick
                        non_strick=strick
                        strick=temp
                elif int(stat)%2==0:
                    player[strick][1].append(int(stat)) 
                    if bowl%6==0:
                        temp=non_strick
                        non_strick=strick
                        strick=temp   
            elif stat=='out':
                bowl+=1
                over=(bowl//6) 
                if strick==0:
                    n=count(player[strick][1])
                    print('{} is out run({}) four({}) six({})'.format(player[strick][0],sum([j for j in player[strick][1]]),n[4],n[6]))
                    total_out+=1
                    self.cur.execute("insert into {}(player_name,run,six,four) values(?,?,?,?)".format(self.game_name),(player[strick][0],sum([j for j in player[strick][1]]),n[4],n[6]))
                    self.db.commit()
                    [player[strick][0],player[strick][1]]=Game.new_player()
                elif strick:
                    n=count(player[strick][1])
                    print('{} is out run({}) four({}) six({})'.format(player[strick][0],sum([j for j in player[strick][1]]),n[4],n[6]))
                    total_out+=1
                    self.cur.execute("insert into {}(player_name,run,six,four) values(?,?,?,?)".format(self.game_name),(player[strick][0],sum([j for j in player[strick][1]]),n[4],n[6]))
                    self.db.commit() 
                    [player[strick][0],player[strick][1]]=Game.new_player() 
            else:
                print('wrong input')
            n=count(player[strick][1])
            m=count(player[non_strick][1])
            self.cur.execute("update {} set run={},six={},four={}".format(self.game_name,sum([j for j in player[strick][1]]),n[4],n[6]))    
            self.cur.execute("update {} set run={},six={},four={}".format(self.game_name,sum([j for j in player[non_strick][1]]),m[4],m[6])) 
    def close(self):
        self.db.close()
    def graph(self):
        fig,ax=plt.subplots() 
        def animate(i):
            #x=[]
            y=[]
            self.cur.execute("select * from {}".format(self.game_name+'_run'))
            p=self.cur.fetchall()
            y.append(p)
            ax.clear()
            ax.plot(y)
        anim=fn(fig,animate,interval=1000)
        plt.show()    
    def show_data(self):
        self.cur.execute("select * from {}".format(self.game_name))
        return self.cur.fetchall()        
            
