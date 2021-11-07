import db
import numpy as np 
import pandas as pd 
import json
import teammate as tm
from os import path

class prepareData:
    def __init__(self):
        self.info = db.databaseConnecter()

    """
    Irregulatiries in data:
        1. not full roster
        2. undefined values
        3. value doesn't exist
    """
    def normalizedTeamRankSum(self):
        if path.exists("file1.csv"):
            return pd.read_csv("file1.csv")
            
        rows = self.info.query("select woncount, losscount, teammates, enemies from playergame")
        
        result = pd.DataFrame(columns=['NetSum','sd1','sd2', 'wpr','lpr'], dtype=float)
        for row in rows:
            if row[0] + row[1] <= 0:
                continue
            print(row[3])
            print(row[2])
            wpr = row[0] / (row[0] + row[1])
            lpr = row[1] / (row[0] + row[1])
            if row[3] == None or row[2] == None or "undefined" in row[2] or "undefined" in row[3] or len(row[2][1:-1].split(")")) < 6 or len(row[3][1:-1].split(")")) < 6:
                continue
            print("RUNNING DATA")
            teammates = [tm.teammate(item[item.index("("):], 0) for item in row[2][1:-1].split(")")[:5]]
            enemies = [tm.teammate(item[item.index("("):], 1) for item in row[3][1:-1].split(")")[:5]]
            sum1 = 0
            sum2 = 0
            flag = False
            for item in teammates:
                sum1 += int(item.rank)
                if int(item.rank) == 0:
                    flag = True
            for item in enemies:
                sum2 += int(item.rank)
                if int(item.rank) == 0:
                    flag = True
            if sum1 == 0 or sum1 == 0 or flag:
                continue
            netSum = sum1 - sum2
            avg1 = sum1 / 5
            avg2 = sum2 / 5
            sd1 = 0
            sd2 = 0
            for item in teammates:
                sd1 += (int(item.rank) - avg1)**2
            for item in enemies:
                sd2 += (int(item.rank) - avg2)**2
            sd1 = (sd1 / 5)**0.5
            sd2 = (sd2 / 5)**0.5
            result = result.append(pd.DataFrame([[netSum,sd1,sd2,wpr,lpr]], columns=['NetSum','sd1','sd2', 'wpr','lpr']), ignore_index=True)

        result.to_csv("file1.csv")
        return result
            
