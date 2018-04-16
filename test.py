string = '''December 29, 2018'''
list = string.split(' ')

year = list[2]
day = list[1][:1]
month_dic = {'January': '01','February':'02','March':'03','April':'04','May':'05','June':'06',
'July' :'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
month = month_dic[list[0]]
if len(day) == 1:
    date_str = year + '-' + month + '-0' + day
else:
    date_str = year + '-' + month + '-' + day
print(date_str)
