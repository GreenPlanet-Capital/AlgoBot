import numpy as np
a = np.array([1,2,3,5,7,5,6,8,9,10,9,10,11,12,12,20])

def std(price_array):
        std_val = np.std(price_array)
        return std_val

def sma(price_array):
    sma_val = np.sum(price_array)/len(price_array)
    return sma_val

def wma(price_array):
    sum_val = 0 
    div = len(price_array)
    for j,i in enumerate(price_array):
        sum_val += (j+1)*i
    wma_val = (sum_val*2)/(div*(div+1))
    return wma_val

def mcg(price_array):
    len_pa = len(price_array)
    base_val_array = price_array[:len_pa - 1]
    base_val = np.sum(base_val_array)/len(base_val_array)
    numer = (price_array[-1] - base_val)
    denom = len_pa*((price_array[-1]/base_val)**4)
    frac = numer/denom
    mcg_val = frac + base_val
    return mcg_val

def lin_reg(price_array):
    n = len(price_array)
    sum_y = 0
    sum_xy = 0
    sum_x = (n+1)*n/2
    sum_x2 = n*(n+1)*(2*n+1)/6
    for i,j in enumerate(price_array):
        sum_y += j
        sum_xy += (i+1)*j 
    lin_reg = (n*sum_xy - (sum_x*sum_y))/((n*sum_x2) - (sum_x*sum_x))
    return lin_reg
    

print("STD: " + str(std(a)))
print("WMA: " + str(wma(a)))
print("SMA: " + str(sma(a)))
print("MCG: " + str(mcg(a)))
print("LinReg: " + str(lin_reg(a)))