mystr1 = '冠寓 北京望京北路店 青春阳光开间C'
mystr2 = '整租 · 泰禾中央广场 2室2厅 复式'
rental = ''
if '· ' in mystr1:
    mystr1 = mystr1.replace('· ', '')
    mystr1 = mystr1.split(' ', 1)
    print(mystr1)
else:
    a = mystr1.split(' ', 1)[1]
    print(a)

