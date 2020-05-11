import sqlite3 as sql
import os
from collections import Counter as count
class Game:
    def __init__(self,db_name,name_list_file,game_name,num_player=8,T_over=8):
        self.game_name=game_name
        self.num_player=num_player
        self.T_over=T_over
        self.db=sql.connect('{}.db'.format(db_name))
        self.cur=self.db.cursor()    
        self.name_list_file=name_list_file
        self.player=[[j.split()[0],[]] for j in open(self.name_list_file)]
    def create_table(self):
        try:
            cur.execute("create table {}(player_name text,run int,six int,four int)".format(self.game_name))
            db.commit()
        except:
            prnit('game already played,start another new game')
    def play(self):
        total_out=0
        stat='0'
        strick=0
        non_strick=1
        temp=0
        bowl=0
        over=0
        while (over<self.T_over and total_out<self.num_player):
            stat=input('event:')
            bowl+=1
            over=(bowl//6)+1
            if not stat=='out':
                if int(stat)%2:
                    self.player[strick][1].append(int(stat))
                    if bowl%6==0:
                        pass
                    else:
                        temp=non_strick
                        non_strick=strick
                        strick=temp
                elif int(stat)%2==0:
                    self.player[strick][1].append(int(stat)) 
            elif stat=='out':
                if strick==0:
                    n=count(self.player[strick][1])
                    print('{} is out {} {} {}'.format(self.player[strick][0],sum([j for j in self.player[strick][1]]),n[4],n[6]))
                    break
                elif strick:
                    n=count(self.player[non_strick][1])
                    print('{} is out {} {} {}'.format(self.player[non_strick][0],sum([j for j in self.player[non_strick][1]]),n[4],n[6]))
                    break
        #return self.player[1][1] 
        #db.commit()
    def close(self):
        db.close()
    def show_data(self):
        cur.execute("select * from {}".format(self.game_name))
        return cur.fetchall()        
            
