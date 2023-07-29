import sqlite3
from datetime import datetime
import programanager as pm
import pandas as pd



def createTasks():
    conn =  sqlite3.connect('mydb.sqlite')
    cursr = conn.cursor()

    try:
        conn.execute("""create table Tasks(
            pid,
            name,
            create_time,
            current_time,
            terminated,
            event
        );""")
        for i in pm.list:
            conn.execute("""INSERT INTO Tasks (name)
                    VALUES (?)""",(str(i),))
        print('Creating base table')
    except:
        
        uf = pd.read_sql("""SELECT name FROM Tasks""", conn)['name'].tolist()
        #list insert
        for item in pm.list:
            if item not in uf:
                cursr.execute("""INSERT INTO Tasks (name)
                            VALUES (?)""",(str(item),))
       
        #list delete
        for item in uf:
            if item not in pm.list:
                cursr.execute("""DELETE FROM Tasks 
                            WHERE name = (?)""",(str(item),))

        processes = pm.get_processes_info()
        df = pm.construct_dataframe(processes)
        df.to_sql('Data', conn, if_exists='replace', )

        time_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")


        cursr.execute("""
            DELETE FROM Data 
            WHERE rowid > (
            SELECT MIN(rowid) FROM Data c  
            WHERE c.Name = Data.Name)
            """)

        cursr.execute("""UPDATE Tasks
                        SET pid = ( SELECT Data.pid
                                    FROM Data
                                    WHERE Data.name = Tasks.name),
                        create_time = (SELECT create_time
                                        FROM Data
                                        WHERE name = Tasks.name)
                        WHERE 
                        EXISTS(
                            SELECT * 
                            FROM Data
                            WHERE Tasks.name = Data.name)""")
   
        
        terminated = ['True']*len(pm.list)
        eventcreated = ['False']*len(pm.list) 
        cursr.execute('SELECT pid,name,create_time FROM Data')
        datal = cursr.fetchall()

        for count, element in enumerate(pm.list):
            for row in datal:
                if element == row[1]:
                    terminated[count] = 'False'
                    eventcreated[count] = 'False'
                    break
    
        for t,n,e in zip(terminated,pm.list,eventcreated):
            conn.execute("""UPDATE Tasks 
                            SET (current_time,terminated,event) = (?,?,?)
                            WHERE name = ?""", (time_now,t,e,n))

        print('updated')
    conn.commit()
    conn.close()

