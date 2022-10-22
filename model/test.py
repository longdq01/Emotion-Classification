import re
s="%@^%@^"
s = re.sub("[%^@]", 'A', s)
print(s)