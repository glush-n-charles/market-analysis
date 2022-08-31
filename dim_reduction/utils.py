'''
utils.py
By Michael Glushchenko.

THIS FILE CONTAINS UTILITY FUNCTIONS USED FOR PROCESSING
DATA INSIDE EACH OF THE FILES IN THE /DATA/MINUTE FOLDER.
'''

PATTERN_SIZE = 1000

def findMin(x,v,n):
    i, c =0, 0
    index, value, m = [], [], v[0]
    low = False

    for j in range(len(v) - 1):
        if v[j+1] >= m:
            c += 1
            if c == n:
                value.append(m)
                index.append(x[i])
                m = v[j+1]
                i = j + 1
                c = 0
        else:
            c = 0
            m = v[j+1]
            i = j + 1
            
    for j in range(n-1):
        low = True
        if v[len(v) - 1] > v[len(v) - j - 2]:
            low = False
    
    if low == True:
        value.append(v[len(v)-1])
        index.append(x[len(v)-1])
    
    return index, value

def findMax(x,v,n):
    i, c =0, 0
    index, value, m = [], [], v[0]
    high = False

    for j in range(len(v)-1):
        if v[j+1] <= m:
            c += 1
            if c == n or j + 1 == len(v) - 1:
                value.append(m)
                index.append(x[i])
                m = v[j+1]
                i = j+1
                c = 0
        else:
            c = 0
            m = v[j+1]
            i = j + 1
            
    for j in range(n-1):
        high = True
        if v[len(v) - 1] < v[len(v) - j - 2]:
            high = False

    if high == True:
        value.append(v[len(v)-1])
        index.append(x[len(v)-1])

    return index, value

def normalize(v):
    p = []
    m = max(v)
    n = min(v)
    d = m - n
    
    for i in range(len(v)):
        p.append((v[i] - n) / d)
    
    return p

def zipp(lv,hv,liv,hiv,p=0.01):
    li, hi, m = 0, 0, 0
    v, vi = [], []

    while li < len(lv) and hi < len(hv):
        m = li
        while liv[li] < hiv[hi]:
            if lv[m] - lv[li] > -p:
                m = li
            li += 1
        v.append(lv[m])
        vi.append(liv[m])

        m = hi
        while hiv[hi] < liv[li]:
            if hv[m] - hv[hi] < p:
                m = hi
            hi += 1
            if hi >= len(hv):
                break
        if hi >= len(hv):
            break
        v.append(hv[m])
        vi.append(hiv[m])

    return vi, v

def unzipp(x,y):
    lv, hv, liv, hiv = [], [], [], []

    for i in range(len(x)):
        if i % 2 == 0:
            liv.append(x[i])
            lv.append(y[i])
        else:
            hiv.append(x[i])
            hv.append(y[i])  

    return lv, hv, liv, hiv

def findInc(vec,x,y,change,daysbefore):
    v, vi, startendx, startendy = [], [], [], []

    veci = [*range(len(vec))]
    for i in range(1, len(x) - 1):
        if y[i+1] - y[i] >= change:
            n = x[i] + 1
            m = n - daysbefore
            if m >= 0:
                v.append(vec[m:n])
                vi.append(veci[m:n])
                startendx.append([x[i],x[i+1]])
                startendy.append([y[i],y[i+1]])
    return v, vi, startendx, startendy

def findDec(vec, x, y, change, daysbefore):
    v, vi, startendx, startendy = [], [], [], []
    
    veci = [*range(len(vec))]
    for i in range(1, len(x) - 1):
        if y[i+1] - y[i] <= change:
            n = x[i] + 1
            m = n - daysbefore
            if m >= 0:
                v.append(vec[m:n])
                vi.append(veci[m:n])
                startendx.append([x[i],x[i+1]])
                startendy.append([y[i],y[i+1]])

    return v, vi, startendx, startendy

def differences(v):
    return [v[i + 1] - v[i] for i in range(len(v) - 1)]

def connect_patterns(x, y, dist):
    xy = [x, y]
    
    for i in range(1, len(x)):
        if len(x[i]) < dist:
            for x in xy:
                matches = (j for j in range(len(x[i]), 0, -1) if x[i-1][:j] == x[i][-j:])
                j = next(matches, 0)
                x[i-1] = x[i-1] + x[i][j:]