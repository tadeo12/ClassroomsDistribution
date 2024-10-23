
def expr(x, k):
    return (15*x - 2*k) * (15*x - 2*k -1)/2

def productoria(aulas, comisiones):
    producto = 1
    for k in range(0, comisiones - 1):
        producto *= expr(aulas, k)
    return producto


x=int(input("aulas: "))
n=int(input("comisiones: "))
print(productoria(x, n))