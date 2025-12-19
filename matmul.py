def matrix_multiply(matrix1, matrix2):
    # This function should be implemented by the students
    # Placeholder implementation that always raises NotImplementedError
    
   
    #  ----------------------------------- ---------!!! INPUT ERROR CHECKING PART !!!-------------------------------------------------------------------



    #  calculate order of matrix 1 

    if (len(matrix1)==0):
        raise ValueError                    # Raise error if matrix in empty 
    else:
        mat_1_rows=len(matrix1)
    mat_1_columns=len(matrix1[0])
    
    for i in range(len(matrix1)):
        if len(matrix1[i])!=mat_1_columns:
            raise ValueError                # Raises error if no.of.row elements are not consistent
    
    #calculate order of matrix 2
    if (len(matrix2)==0):
        raise ValueError                    # Raise error if matrix in empty 
    else:
        mat_2_rows=len(matrix2)
    mat_2_columns=len(matrix2[0])
    
    for i in range(len(matrix2)):
        if len(matrix2[i])!=mat_2_columns:
            raise ValueError                # Raises error if no.of.row elements are not consistent
    
   
    #check order for matrix multiplication
    if (mat_1_columns!=mat_2_rows):
        raise ValueError                    # Raise error if matrix cannot be multiplied
    
    #check consistency of elements in matrix

    for i in range(len(matrix1)):
        for j in matrix1[i]:
            if not isinstance(j,(int,float)):
                raise TypeError             # Raise error if non numeric value is found
            
    for i in range(len(matrix2)):
        for j in matrix2[i]:
            if not isinstance(j,(int,float)):
                raise TypeError              # Raise error if non numeric value is found
    
    # -------------------------------------------------!!!  MATRIX MULTIPLICATION PART !!!-------------------------------------------------------------


    # final multiplied matrix
    mat_final_columns=mat_2_columns
    mat_final_rows=mat_1_rows
    mat_final=[]
   
    for i in range(mat_final_rows):
        mat_final.append([])
        for j in range(mat_final_columns):
            
            val=0
            for k in range(mat_1_columns):
                val+=matrix1[i][k]*matrix2[k][j]
            val=round(val,2)
            mat_final[i].append(val)
    return mat_final








            
            

   



