def mv(s):

    s=s.strip()
    s=s.replace(' ','').replace('-','')
    if len(s)==10 and s.isdigit() and s[0] in '6789':
        return True
    if len(s)==12 and s[:2]=='91' and s.isdigit() and s[3] in '6789':
        return True
    if len(s)==11 and s[0]=='0' and s.isdigit() and s[1] in '6789':
        return True
    if len(s)==13 and s[:3]=='+91' and s[3:].isdigit() and s[4] in '6789':
        return True
    return False

for i in ['9876543210','919876543210','09876543210','+919876543210','1234567890','98765 43210','98765-43210','+9 19876543210','98765 43210 1','+91-1234567890']:
    print(i,mv(i))