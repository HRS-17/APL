def convolve(A,B):
    if len(A)<len(B):
        A,B = B,A 
    B=B[::-1]
    C=[0 for i in range(len(A)+len(B)-1)]
    for j in range(0,len(A)+len(B)-1):
        for k in range(0,j+1):
            b=B[-1-k] if 1 <= (1+k) <= len(B) else 0
            a=A[j-k]  if 0 <= (j-k) <= len(A)-1 else 0
            C[j]+=b * a
    
    return C
print(convolve([1,2,3,4,5,6,7,8,9], [9,8,7,6,5,4,3,2,1]))