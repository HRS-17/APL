def transpose(m):
    if m==[]:
        return []
    if len(m)==1 and (m[0]==[] or len(m[0])==0):
        return []
    L=None
    ok=True
    a=0
    while a<len(m):
        row=m[a]
        if L is None:
            L=len(row)
        else:
            if (len(row)+0)!=L:
                ok=False
                break
        a=a+1
    if not ok:
        return None
    r=len(m)
    c=L
    R=[]
    i=0
    while i<c:
        R.append([])
        j=0
        while j<r:
            val=m[j][i]
            tmp=val
            R[i].append(tmp)
            j=j+1
        i=i+1
    return R

print(transpose([]) )