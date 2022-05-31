import sqlite3
import datetime
import sys

print('————————插入患者数据————————')
conn = sqlite3.connect(sys.path[0] + '/../db.sqlite3')
cursor = conn.cursor()
with open(sys.path[0] + '/../doc/patients.txt',encoding="utf-8") as patients:
    for patient in patients:
        details = patient.split('\t')
        patient_id = details[0]
        name = details[1]
        sex_char = details[2].replace('\n','')
        sex = 'Male' if sex_char == '男' else 'Female'
        data = (patient_id,name,sex,1,True,datetime.datetime.now())
        sql = 'insert into BoneAge_patient(Patient_Id,name,sex,modify_user_id,active,modify_date) values(?,?,?,?,?,?)'
        cursor.execute(sql,data)
conn.commit()
conn.close()
print('————————插入完成————————')