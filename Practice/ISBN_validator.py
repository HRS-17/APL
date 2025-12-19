def isbn_10validator(isbn:str):
    isbn=isbn.strip()
    isbn=isbn.split('-') 
    num=''
    num=num.join(isbn)

    # check the number of characters 
    if len(num)==9 and num.isdigit():
        # for i in num:
        #     if i not in  '0123456789':
        #         # raise ValueError('invalid character for a 9-digit number')
        #         return None 
        sum=0
        num_4_sum=num[::-1]
        for i in range(len(num)):
            sum+=int(num[i])*(i+1)
            
        if sum%11==10:
            print(sum)
            return 'X'
        else:
            print(sum)
            return str(sum%11)
        
    elif len(num)==10 and num.isdigit():
        
        # for i in num[:len(num)-1]:
        #     if i not in '0123456789':
        #         # raise ValueError('invalid character(1-9) for a 10-digit number')
        #         invalid_ch+=1
        #     if num[-1] not in '0123456789X':
        #         #raise ValueError('invalid  last  character for a 10-digit number')
        #         invalid_ch+=1
    
        # div by 11 check for !!! 10 BIT ISBN !!!
        sum=0
        num_4_sum=num[::-1]
        for i in range(len(num)):
            if num_4_sum[i].isdigit():
                sum+=int(num_4_sum[i])*(i+1)
            else:
                sum+=10*(i+1)
        print('10bit')
        if sum % 11==0:
            # raise ValueError('inputted number failed isbn sum check')
            return True
        else :
            return False
    else:
        return False
       

            

    
   
        

for i in ['0-7475-3269-X',"0134494164",'0000-0000-00',"0-7475--3269"]:
    print(isbn_10validator(i))
