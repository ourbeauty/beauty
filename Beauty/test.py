import json

c = '{"ky": 2, "key": 1, "k4": 2, "i": 3}'
c=json.loads(c)
y=list(c)
for x in y:
    del c[x]
print(c)

c
