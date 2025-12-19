def csc_row_to_header(header,row):
    
    h=header.strip()
    r=row.strip()
    
    h_list=h.split(',')
    h_list=[i.strip() for i in h_list]
    r_list=r.split(',')
    r_list=[i.strip() for i in r_list]

    if len(h_list)!=len(r_list):
        return None
    d=zip(h_list,r_list)
    return dict(d)

print(csc_row_to_header(' row',','))

    
        
            
            
        
    

