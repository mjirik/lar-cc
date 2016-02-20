""" boundary operators """
from larlib import *
""" convex-cells boundary operator --- best implementation """
def boundary(cells,facets):
    lenV = max(CAT(cells))+1
    csrCV = csrCreate(cells,lenV)
    csrFV = csrCreate(facets,lenV)
    csrFC = csrFV * csrCV.T
    facetLengths = [csrFacet.getnnz() for csrFacet in csrFV]
    m,n = csrFC.shape
    facetCoboundary = [[csrFC.indices[csrFC.indptr[h]+k] 
        for k,v in enumerate(csrFC.data[csrFC.indptr[h]:csrFC.indptr[h+1]]) 
            if v==facetLengths[h]] for h in range(m)]
    indptr = [0]+list(cumsum(AA(len)(facetCoboundary)))
    indices = CAT(facetCoboundary)
    data = [1]*len(indices)
    return csr_matrix((data,indices,indptr),shape=(m,n),dtype='b')

""" path-connected-cells boundary operator """
import larlib
import larcc
from larcc import *

def csrBoundaryFilter2(unreliable,out,csrBBMat,cells,FE):
    for row in unreliable:
        for j in range(len(cells)):
            if out[row,j] == 1:
                cooCE = csrBBMat.T[j].tocoo()
                flawedCells = [cooCE.col[k] for k,datum in enumerate(cooCE.data)
                    if datum>2]
                if all([facet in flawedCells  for facet in FE[row]]):
                    out[row,j]=0
    return out

def csrBoundaryFilter3(unreliable,out,csrBBMat,cells,FE):
    for col in unreliable:
        cooCE = csrBBMat.T[col].tocoo()
        flawedCells = [cooCE.col[k] for k,datum in enumerate(cooCE.data)
                    if datum>2]
        for j in range(out.shape[0]):
            if out[j,col] == 1:
                if all([facet in flawedCells  for facet in FE[j]]):
                    out[j,col]=0
    return out
""" path-connected-cells boundary operator """
def boundary2(CV,FV,EV):
    out = boundary(CV,FV)
    def csrRowSum(h): 
        return sum(out.data[out.indptr[h]:out.indptr[h+1]])    
    unreliable = [h for h in range(len(FV)) if csrRowSum(h) > 2]
    if unreliable != []:
        csrBBMat = boundary(FV,EV) * boundary(CV,FV)
        lenV = max(CAT(CV))+1
        FE = larcc.crossRelation0(lenV,FV,EV)
        out = csrBoundaryFilter2(unreliable,out,csrBBMat,CV,FE)
    return out

def boundary3(CV,FV,EV):
    out = boundary2(CV,FV,EV)
    lenV = max(CAT(CV))+1
    VV = AA(LIST)(range(lenV))
    csrBBMat = scipy.sparse.csc_matrix(boundary(FV,EV) * boundary2(CV,FV,EV))
    def csrColCheck(h): 
        return any([val for val in csrBBMat.data[csrBBMat.indptr[h]:csrBBMat.indptr[h+1]] if val>2])    
    unreliable = [h for h in range(len(CV)) if csrColCheck(h)]
    if unreliable != []:
        FE = larcc.crossRelation0(lenV,FV,EV)
        out = csrBoundaryFilter3(unreliable,out,csrBBMat,CV,FE)
    return out

def totalChain(cells):
    return csr_matrix(len(cells)*[[1]])

def boundaryCells(cells,facets):
    csrBoundaryMat = boundary(cells,facets)
    csrChain = csr_matrix(totalChain(cells))
    csrBoundaryChain = csrBoundaryMat * csrChain
    out = [k for k,val in enumerate(csrBoundaryChain.data.tolist()) if val == 1]
    return out

def boundary2Cells(cells,facets,faces):
    csrBoundaryMat = boundary2(cells,facets,faces)
    csrChain = csr_matrix(totalChain(cells))
    csrBoundaryChain = csrBoundaryMat * csrChain
    out = [k for k,val in enumerate(csrBoundaryChain.data.tolist()) if val == 1]
    return out

def boundary3Cells(cells,facets,faces):
    csrBoundaryMat = boundary3(cells,facets,faces)
    csrChain = csr_matrix(totalChain(cells))
    csrBoundaryChain = csrBoundaryMat * csrChain
    out = [k for k,val in enumerate(csrBoundaryChain.data.tolist()) if val == 1]
    return out

""" Marshalling a structure to a LAR cellular model """
import bool
import inters
from bool import *
def larMarshal2(struct):
    W,FW,EW = struct2lar(struct)
    quadArray = [[W[v] for v in face] for face in FW]
    parts = bool.boxBuckets3d(containmentBoxes(quadArray))
    Z,FZ,EZ = bool.spacePartition(W,FW,EW, parts)
    V,FV,EV = inters.larSimplify((Z,FZ,EZ),radius=0.0001)
    return V,FV,EV

