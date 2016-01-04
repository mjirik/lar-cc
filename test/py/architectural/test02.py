""" test file """
from larlib import *


V = [[3,-3],
[9,-3],[0,0],[3,0],[9,0],[15,0],
[3,3],[6,3],[9,3],[15,3],[21,3], 
[0,9],[6,9],[15,9],[18,9],[0,13],
[6,13],[9,13],[15,13],[18,10],[21,10], 
[18,13],[6,16],[9,16],[9,17],[15,17],
[18,17],[-3,24],[6,24],[15,24],[-3,13]]
FV = [
[22,23,24,25,29,28], [15,16,22,28,27,30], [18,21,26,25], 
[13,14,19,21,18], [16,17,23,22], [11,12,16,15],
[9,10,20,19,14,13], [2,3,6,7,12,11], [0,1,4,8,7,6,3],
[4,5,9,13,18,17,16,12,7,8],[17,18,25,24,23]]
dwelling = [V,FV]

(W,FW) = larApply(s(-1,-1))(dwelling)
(V,FV) = dwelling
(V,FV) = movePoint2point([ (V,FV),(W,FW) ])(V[20])(W[25])
EV = face2edge(FV)
VIEW(EXPLODE(1.2,1.2,1)(MKPOLS((V,EV))))

lines = [[V[u],V[v]] for u,v in EV]
V,FV,EV,polygons = larFromLines(lines)
VIEW(EXPLODE(1.2,1.2,1)(MKPOLS((V,EV))))
VIEW(EXPLODE(1.2,1.2,1)(MKTRIANGLES((V,FV[:-1],EV)))) # bug in triangulation!
VIEW(SKEL_1(EXPLODE(1.2,1.2,1)(MKTRIANGLES((V,FV[:-1],EV))))) # bug in triangulation!

VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
VIEW(larModelNumbering(1,1,1)(V,[VV,EV,FV],submodel,5))

FE = crossRelation(V,FV,EV)
W,FW,EW = (V,[FV[14]],[EV[e] for e in FE[14]])
VIEW(STRUCT(MKPOLS((W,FW,EW))))
VIEW(SKEL_1(EXPLODE(1.2,1.2,1)(MKTRIANGLES((W,FW,EW)))))
