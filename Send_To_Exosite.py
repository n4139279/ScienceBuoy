from pyonep import onep

o = onep.OnepV1()

cik = '455954b2b6e787bc71fad187e4471f51700fb191'
dataport_alias = 'Internal_temperature'
val_to_write = 5

testvar = o.write(cik,{"alias": dataport_alias},val_to_write,{})

isok, response = o.read(cik,
{'alias': dataport_alias},
{'limit': 1, 'sort': 'desc', 'selection': 'all'})

if isok:
    # expect Read back [[1374522992, 1]]
    print("Read back %s" % response)
else:
    print("Read failed: %s" % response)

print testvar
