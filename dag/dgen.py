import  numpy as np

Num = 1000
Vmin = 100
Vmax = 200

for p in xrange(Num):
    n = np.random.randint(Vmin,Vmax)
    f = open("./t/%d" % p,"w")
    m = np.zeros([n,n],dtype='int')
    for i in xrange(n):
        for j in xrange(n):
            if i < j and np.random.random() <= 0.1:
                m[i][j] = 1
    f.write("%d\n" % n)
    for i in xrange(n):
        for j in xrange(n):
            f.write("%d " % m[i][j])
        f.write("\n")
    f.close()
