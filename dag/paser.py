import  numpy as np
# #
# # m = np.zeros([100,100],dtype='int')
# #
# # f = open("test", "r")
# o = open("Epigenomics_50","w")
# # for line in f.readlines():
# #     l = line.split()
# #     if l[0] == "<child":
# #         c_id = int(l[1][10:12])
# #     elif l[0] == "<parent":
# #         p_id = int(l[1][10:12])
# #         m[p_id][c_id] = 1
# #
# #
#
#
# o = open("Epigenomics_50","w")
# m = np.zeros([50,50],dtype='int')
# for i in xrange(12):
#     m[0][i + 1] = 1
#     m[i + 1][12 + i + 1] = 1
#     m[12 + i + 1][24 + i + 1] = 1
#     m[24 + i + 1][36 + i + 1] = 1
#     m[36 + i + 1][49] = 1
#
# for i in xrange(50):
#     for j in xrange(50):
#         o.write(" %d" % m[i][j])
#     o.write("\n")
#
#
# o = open("CyberShake_24","w")
# m = np.zeros([24,24],dtype='int')
# for i in xrange(5):
#     m[0][i + 2] = 1
#     m[1][i + 7] = 1
#     m[i + 2][i + 12] = 1
#     m[i + 7][i + 17] = 1
#     m[i + 2][22] = 1
#     m[i + 7][22] = 1
#     m[i + 12][23] = 1
#     m[i + 17][23] = 1


#
# o = open("Epigenomics_24","w")
# m = np.zeros([24,24],dtype='int')
# for i in xrange(5):
#     m[0][i + 1] = 1
#     m[i + 1][i + 6] = 1
#     m[i + 6][i + 11] = 1
#     m[i + 11][i + 16]  = 1
#     m[i + 16][21] = 1
#     m[21][22] = 1
#     m[22][23] = 1
#
# o = open("LIGO_24","w")
# m = np.zeros([24,24],dtype='int')
# for i in xrange(6):
#     m[i][i + 6] = 1
#     m[i + 6][12] = 1
#
# for i in xrange(5):
#     m[12][i + 13] = 1
#     m[i + 13][i + 18] = 1
#     m[i + 18][23] = 1


# o = open("LIGO_50","w")
# m = np.zeros([50,50],dtype='int')
# for i in xrange(12):
#     m[i][i + 12] = 1
#     m[i + 12][24] = 1
#     m[24][25 + i] = 1
#     m[25 + i][37 + i] = 1
#     m[37 + i][49] = 1
#
# for i in xrange(50):
#     for j in xrange(50):
#         o.write(" %d" % m[i][j])
#     o.write("\n")


o = open("LIGO_100","w")
m = np.zeros([100,100],dtype='int')
for i in xrange(25):
    m[i][i + 25] = 1
    m[i + 25][50] = 1

for i in xrange(24):
    m[50][51 + i] = 1
    m[51 + i][75 + i] = 1
    m[75 + i][99] = 1

for i in xrange(100):
    for j in xrange(100):
        o.write(" %d" % m[i][j])
    o.write("\n")