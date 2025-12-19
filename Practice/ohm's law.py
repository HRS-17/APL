def ohmslaw(V,I,R):
    none_val=0
    for i in [V,I,R]:
        none_val += 1 if i is None else 0
  
    if none_val >1:
        return "Error: Two parameters cannot be None"
    if none_val==0:
        return  "Error: All parameters are provided"
    
    
    # if V is not None :
    #     if not isinstance(V,(int,float)):
        
    #         raise "Error: Invalid type for voltage "  
    # if I is not None :
    #     v=str(I)
    #     v=v.replace('.','0')
    #     if not v.isdigit():
    #         raise "Error: Invalid type for current " 
    # if R is not None :
    #     v=str(R)
    #     v=v.replace('.','0')
    #     if not v.isdigit():
    #         raise "Error: Invalid type for resistance " 
        
    values=[V,I,R]
    names=['volatage','current','resistance']
    for v,n in zip(values,names):
        if v is not None and not isinstance(v,(int,float)):
            return f'Error:Invalid datatype for {n}'
    if R is None and I==0:
        return "Error: Current is zero while calculating resistance"
    
    if V is None :
        
        volt=round(float(I*R),1)
        return f'Voltage={volt}'
    elif R is None :
        Resist=round(V/I,1)
        return f'Voltage={Resist}'
    else:
        curr=round(V/R,1)
        return f'Voltage={curr}'
    
print(ohmslaw(12, 'ad', None))
    
    
