from datetime import datetime
import os

def mark_attendance(name, file_path='Attendance.csv'):
    # Create file with header if it does not exist

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.writelines('Name,Time')

    with open(file_path, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]

        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')
            print(f'Logged: {name}')