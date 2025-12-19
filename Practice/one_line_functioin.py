cube=lambda x:x**3
print(cube(3))

fact=lambda y,x:x+y
print(fact(1,2))

line=lambda a,c,x:a*x+c
print(line(1,1,3))

exp=lambda x,a,b: a* numpy.exp(-b*x)

polynomial=lambda x,*params: sum(params[i]*x**i for i in params)

sine=lambda x,f,A:A*np.sine(2*pi*f*x)
