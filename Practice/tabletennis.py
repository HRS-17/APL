def convert_to_raindrops(number):
    op=''
    if number % 3==0:
        op+='Pling'
    if number %5==0:
        op+='Plang'
    if number %7==0:
        op+="Plong"
    if op=='':
        op+=str(number)
    return op
for i in [3,5,15,21,35,105,34,1,0,-3,-34]:
    print (convert_to_raindrops(i))