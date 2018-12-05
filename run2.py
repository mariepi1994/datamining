import sqlite3

conn = sqlite3.connect('employee.db')



def test(folder):
    count = 0
    with zipfile.ZipFile(folder) as myzip:
        print(myzip.filelist)
        for mf in myzip.filelist:
            with myzip.open(mf.filename) as myfile:
                mc = myfile.read()
                c = csv.StringIO(mc.decode())
                for row in c:
                    count += 1
                    #print(count)
                    #print(row)
    print(count)
