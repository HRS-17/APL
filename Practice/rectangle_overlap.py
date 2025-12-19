def rectangle_overlap(x1,y1,w1,h1,x2,y2,w2,h2):
   

    if 0<=(x1-x2 )<= w2:
        pass
    elif 0<=(x2-x1)<=w1:
        pass
    else:
        return 'Non overlapping'
    
    if 0<=(y1-y2 )<= h2:
        return 'overlap'
    elif 0<=(y2-y1)<=h1:
        return 'overlap'
    else:
        return 'Non overlapping'
    


print(rectangle_overlap(-2, -2, 1, 1, -1, -1, 1, 1))