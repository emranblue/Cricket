import sqlite3 as sql
from collections import Counter as count
class Game:
    def __init__(self,game_name='socks',num_player=4,T_over=2):
        self.game_name=game_name
        self.num_player=num_player
        self.T_over=T_over  
        self.db=sql.connect('{}.db'.format('Tournament'))
        self.db2=sql.connect('{}.db'.format('Tournament'))
        self.cur=self.db.cursor()    
        self.cur2=self.db2.cursor()  
    def create_table(self):
        try:
            self.cur.execute("create table {}(player_name text,run int,six int,four int)".format(self.game_name))
            self.cur2.execute("create table {}(bowl int,run int,out int)".format(self.game_name+'_run'))
            self.db.commit()
            self.db2.commit()
        except:
            print('game already played,start another new game')
    def gen_player():
        return [[input('player name:'),[]],[input('player name:'),[]]]    
    def new_player():
        return [input('player name:'),[]]  
    def update_score(self,bowl,run,out):
        self.cur2.execute("insert into {}(bowl,run,out) values(?,?,?)".format(self.game_name+'_run'),(bowl,run,out))
        self.db2.commit()  
    def score_card_update(self,x,y):
        n=count(x)
        self.cur.execute("update {} set run=?,six=?,four=? where player_name=?".format(self.game_name),(sum(x),n[6],n[4],y))
        self.db.commit()  
    def out_info(self,x,y,total_out):
        n=count(y)
        print('{} is out run({}) four({}) six({})'.format(x,sum(y),n[4],n[6]))
        total_out+=1
        return total_out
    def insert_ran_chart(self,x,y):
        n=count(y)
        self.cur.execute("insert into {}(player_name,run,six,four) values(?,?,?,?)".format(self.game_name),(x,sum(y),n[6],n[4]))
        self.db.commit()
    def insert_run(self,bowl,run,out):
        self.cur2.execute("insert into {}(bowl,run,out) values(?,?,?)".format(self.game_name+'_run'),(bowl,run,out))
        self.db2.commit() 
    def swap(x):
        x[0],x[1]=x[1],x[0]
    def insert_new_player(self,x,y):
        n=count(y)
        self.cur.execute("insert into {}(player_name,run,six,four) values(?,?,?,?)".format(self.game_name),(x,sum(y),n[6],n[4]))
        self.db.commit() 
    def fetch_run(self):
        self.cur2.execute("select bowl,run,out from {}".format(self.game_name+'_run'))
        return self.cur.fetchall()  
    def close(self):
        self.cur.close()
        self.db.close()
        self.cur2.close()
        self.db2.close()  
    def del_record(self,run):
        self.cur.execute('''
                    delete from {}
                     where run={}
                    '''.format(self.game_name+'_run',run))       
        self.db.commit()  
    def winner_check(self,table):
        self.cur2.execute("select run from {} order by run desc".format(table+'_run'))
        return self.cur2.fetchone()      
    def play(self,innings,table):
        player=Game.gen_player()
        total_out=0
        stat='0'
        strick=[0,1]
        run=0
        bowl=0
        over=0
        self.insert_ran_chart(player[strick[0]][0],player[strick[0]][1])
        self.insert_ran_chart(player[strick[1]][0],player[strick[1]][1])
        self.insert_run(bowl,run,total_out)
        while (over+1<=self.T_over and total_out<self.num_player):
            if innings==1:
                if bowl==0:
                    check=self.winner_check(table)[0]            
                if run==check:
                    print("Score level")
                elif run>check:
                    print('{} wins'.format(self.game_name))  
                    break  
                stat=input('Need {} from {}.{} to win {}/{} over:{}.{} event:({}):: '.format((check-run),(self.T_over-over),((self.T_over*6-bowl)%6),run,total_out,over,bowl%6,player[strick[0]][0]))
            else:        
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
                if len(total):
                    cut=total.pop()  
                    if cut%2==0:
                        player[strick[0]][1].pop()
                    else:
                        player[strick[1]][1].pop()  
                        Game.swap(strick)  
                    self.del_record(run)
                    run-=cut
                    bowl-=1
                else:
                    print(":)")    
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
                pass  
        self.insert_run(bowl,run,total_out)      
        print('{}/{} over:{}'.format(run,total_out,over))       
    def show_data(self):
        print("\n\n")
        self.cur.execute("select * from {}".format(self.game_name))
        return self.cur.fetchall() 
     
    def graph_data(self):
        self.cur2.execute("select bowl,run,out from {}".format(self.game_name+'_run'))
        return self.cur2.fetchall()       
    