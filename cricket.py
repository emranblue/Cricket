import sqlite3 as sql
from collections import Counter as count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fn
db=sql.connect('{}.db'.format('Tournament'))
db2=sql.connect('{}.db'.format('Tournament'))
cur=db.cursor()    
cur2=db2.cursor()
class Game:
    def __init__(self,game_name='socks',num_player=4,T_over=2):
        self.game_name=game_name
        self.num_player=num_player
        self.T_over=T_over    
    def create_table(self):
        try:
            cur.execute("create table {}(player_name text,run int,six int,four int)".format(self.game_name))
            cur2.execute("create table {}(bowl int,run int,out int)".format(self.game_name+'_run'))
            db.commit()
            db2.commit()
        except:
            print('game already played,start another new game')
    def gen_player():
        return [[input('player name:'),[]],[input('player name:'),[]]]    
    def new_player():
        return [input('player name:'),[]]  
    def update_score(self,bowl,run,out):
        cur2.execute("insert into {}(bowl,run,out) values(?,?,?)".format(self.game_name+'_run'),(bowl,run,out))
        db2.commit()  
    def score_card_update(self,x,y):
        n=count(x)
        cur.execute("update {} set run=?,six=?,four=? where player_name=?".format(self.game_name),(sum(x),n[4],n[6],y))
        db.commit()  
    def out_info(self,x,y,total_out):
        n=count(y)
        print('{} is out run({}) four({}) six({})'.format(x,sum(y),n[4],n[6]))
        total_out+=1
        return total_out
    def insert_ran_chart(self,x,y):
        n=count(y)
        cur.execute("insert into {}(player_name,run,six,four) values(?,?,?,?)".format(self.game_name),(x,sum(y),n[6],n[4]))
        db.commit()
    def insert_run(self,bowl,run,out):
        cur2.execute("insert into {}(bowl,run,out) values(?,?,?)".format(self.game_name+'_run'),(bowl,run,out))
        db2.commit() 
    def swap(x):
        x[0],x[1]=x[1],x[0]
    def insert_new_player(self,x,y):
        n=count(y)
        cur.execute("insert into {}(player_name,run,six,four) values(?,?,?,?)".format(self.game_name),(x,sum(y),n[6],n[4]))
        db.commit() 
    def fetch_run(self):
        cur2.execute("select bowl,run,out from {}".format(self.game_name+'_run'))
        return cur.fetchall()  
    def close(self):
        cur.close()
        db.close()
        cur2.close()
        db2.close()              
    def play(self):
        player=Game.gen_player()
        total_out=0
        stat='0'
        strick=[0,1]
        run=0
        temp=0
        bowl=0
        over=0
        self.insert_ran_chart(player[strick[0]][0],player[strick[0]][1])
        self.insert_ran_chart(player[strick[1]][0],player[strick[1]][1])
        self.insert_run(bowl,run,total_out)
        while (over+1<=self.T_over and total_out<self.num_player):
            stat=input('{}/{} over:{}.{} event:({}):: '.format(run,total_out,over,bowl%6,player[strick[0]][0])) 
            if stat=='wd':
                run+=1
                self.update_score(bowl,run,total_out)
            elif stat=='nb':
                run+=1  
                self.update_score(bowl,run,total_out) 
            elif stat=='4wd' or stat=='4nb':
                run+=5  
                self.update_score(bowl,run,total_out)      
            elif stat=='back':
                total=player[strick[0]][1]+player[strick[1]][1]
                cut=total.pop()  
                if cut%2==0:
                    player[strick[0]][1].pop()
                else:
                    player[strick[1]][1].pop()  
                    Game.swap(strick)  
                run-=cut
                self.update_score(bowl,run,total_out)
                bowl-=1
            elif stat in ('0','1','2','3','4','6'):
                bowl+=1
                over=(bowl//6) 
                run+=int(stat)
                self.update_score(bowl,run,total_out)
                if int(stat)%2:
                    player[strick[0]][1].append(int(stat))
                    self.score_card_update(player[strick[0]][1],player[strick[0]][0])
                    if bowl%6==0:
                        pass
                    else:
                        Game.swap(strick)
                elif int(stat)%2==0:
                    player[strick[0]][1].append(int(stat)) 
                    self.score_card_update(player[strick[0]][1],player[strick[0]][0])
                    if bowl%6==0:
                        Game.swap(strick)   
            elif stat=='out':
                bowl+=1
                over=(bowl//6) 
                if strick[0]==0:
                    total_out=self.out_info(player[strick[0]][0],player[strick[0]][1],total_out)
                    [player[strick[0]][0],player[strick[0]][1]]=Game.new_player()
                    self.insert_new_player(player[strick[0]][0],player[strick[0]][1])
                elif strick[0]:
                    total_out=self.out_info(player[strick[0]][0],player[strick[0]][1],total_out)
                    [player[strick[0]][0],player[strick[0]][1]]=Game.new_player()
                    self.insert_new_player(player[strick[0]][0],player[strick[0]][1])
            else:
                print('wrong input')     
                   
    def show_data(self):
        print("\n\n")
        cur.execute("select * from {}".format(self.game_name))
        return cur.fetchall() 
     
    def graph_data(self):
        cur2.execute("select bowl,run,out from {}".format(self.game_name+'_run'))
        return cur2.fetchall()       
