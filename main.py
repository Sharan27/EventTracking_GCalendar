import sqlite3
import api as a
import updateTable
import time

def main():
  while True:
    conn =  sqlite3.connect('mydb.sqlite')
    cursr = conn.cursor() 

    updateTable.createTasks()
    
    dataitems = cursr.execute(""" SELECT * FROM Tasks            
                    """).fetchall()
    
    for row in dataitems:

        if row[2] == None or row[2] == 'NULL':

          continue
        else:
          if(row[4] == 'True' and row[5]  == 'False'):

            a.addEvent(row)
            conn.execute("""UPDATE Tasks 
                  SET (event,create_time) = (?,?)
                  WHERE name = ?""", ('True','NULL',row[1]))
    print("10 sec")
    time.sleep(10)
    conn.commit()
    conn.close()



if __name__ == "__main__":
  main() 