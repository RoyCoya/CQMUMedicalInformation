import sqlite3
import datetime
import sys

print('————————转换开始————————')
conn = sqlite3.connect(sys.path[0] + '/../db.sqlite3')
cursor = conn.cursor()

patients_chinese_name_dic = {}
with open(sys.path[0] + '/../doc/patients.txt',encoding="utf-8") as patients:
    for patient in patients:
        details = patient.split('\t')
        patient_id = details[0]
        name = details[1]
        patients_chinese_name_dic[patient_id] = name
sql = 'select Patient_Id,name from BoneAge_patient'
cursor.execute(sql)
patients_exited = cursor.fetchall()
for patient in patients_exited:
    id = patient[0]
    try: 
        name = patients_chinese_name_dic[id].replace('\n','')
        data = (name, id)
        sql = 'update BoneAge_patient set name=? where Patient_ID=?'
        cursor.execute(sql, data)
    except: continue

conn.commit()
conn.close()
print('————————转换完成————————')