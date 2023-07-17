import numpy as np
import random
from math import ulp
import struct

def getFPUnbiasedExponent32bits(fpNumber:np.single):
    data = struct.pack("!f", np.single(fpNumber))
    return ((struct.unpack("!L", data)[0] & int("01111111100000000000000000000000", base = 2))>>23)-127
def getFPUnbiasedExponent64bits(fpNumber:np.double):
    data = struct.pack("!d", np.double(fpNumber))
    return ((struct.unpack("!Q", data)[0] & int("0111111111110000000000000000000000000000000000000000000000000000", base = 2))>>52)-1023
def getLongIntFromDouble(fpNumber:np.double):
    data = struct.pack("!d", np.double(fpNumber))
    return struct.unpack("!Q", data)[0]
def getDoubleFromLongInt(intNumber):
    data = struct.pack("!Q", intNumber)
    return struct.unpack("!d", data)[0]
def getLongIntFromDoubleMantissa(fpNumber:np.double):
    data = struct.pack("!d", np.double(fpNumber))
    return struct.unpack("!Q", data)[0] & int("0000000000001111111111111111111111111111111111111111111111111111", base = 2)
def getLongIntFromSingleMantissa(fpNumber:np.single):
    data = struct.pack("!f", np.single(fpNumber))
    return struct.unpack("!L", data)[0] & int("00000000011111111111111111111111", base = 2)
def getExponentNotationStringFromDouble(fpNumber:np.double):
    unbiasedExponent = getFPUnbiasedExponent64bits(fpNumber)
    sign = "" if fpNumber >= 0 else "-"
    mantissaInFloat = 1.0 + getLongIntFromDoubleMantissa(fpNumber) * 2**-52
    return f"{sign}2**{unbiasedExponent}*{mantissaInFloat}"
def getExponentNotationBinStringFromDouble(fpNumber:np.double):
    unbiasedExponent = getFPUnbiasedExponent64bits(fpNumber)
    sign = "" if fpNumber >= 0 else "-"
    mantissaInBin = bin(getLongIntFromDoubleMantissa(fpNumber))[2:].rjust(52, "0")
    return f"{sign}2**{unbiasedExponent}*1.{mantissaInBin}"
def countPossibleFloatsBetweenTwoNumbers(x1, x2):
    assert x1 <= x2, "it requires x1 <= x2"
    assert np.sign(x1) == np.sign(x2),  "this method doesn't work when you have to cross zero, so same sign for x1, x2"
    exp1 = getFPUnbiasedExponent64bits(x1)
    exp2 = getFPUnbiasedExponent64bits(x2)
    longMantissa1 = getLongIntFromDoubleMantissa (x1)
    longMantissa2 = getLongIntFromDoubleMantissa (x2)
    if x1 >= 0 and x2 >= 0:
        n = 2**52*(np.abs(exp2 - exp1)-1) + (2**52 - longMantissa1) + longMantissa2
    else:
        n = 2**52*(np.abs(exp2 - exp1)-1) + (2**52 - longMantissa2) + longMantissa1
    return n
def addMantissaIntToFloat(x, n):
    assert n >= 0
    assert x >= 0
    exp = getFPUnbiasedExponent64bits(x)
    longMantissa = getLongIntFromDoubleMantissa (x)

    longMantissaResult = (longMantissa + n)%(2**52)
    expResult = exp + int(np.floor((longMantissa + n)/(2**52)))

    return 2**expResult * (1.0 + longMantissaResult*2**-52)

def checkIfXIsReachable(x, pwm):
    initialY = pwm.cdfPieceWiseMech(x)
    resultingX = pwm.invCdfPieceWiseMech(initialY)
    return x == resultingX
def findFirstReachableXGreaterOrEqualThanX(x, pwm):
    while True:
        isXReachable = checkIfXIsReachable(x, pwm)
        if isXReachable:
            break
        else:
            x = np.nextafter(x, np.inf) 
    return x
def shouldIGetHoles(minTStarToAnalyze, pwm):
    conditionOnPrecision = ulp(minTStarToAnalyze) < 2**-53 * (np.exp(pwm.eps)/pwm.P)
    conditionOnProbNumberRange = minTStarToAnalyze > pwm.R
    return conditionOnPrecision, conditionOnProbNumberRange

def possibleUpperBoundFormulaForEBarToGetHoles (pwm):
    t = np.exp(pwm.eps / 2)
    E = pwm.E
    Abar = pwm.Abar
    EbarUpperBound = E*((t*(t+1)-3)/(t-1)) - Abar
    return EbarUpperBound

def weightedCumSumIntX(pmfNValues, pPMFList):
    assert len(pmfNValues) == len(pPMFList)
    lenOfBoundarySegments = [pmfNValues[i+1] - pmfNValues[i] for i in range(len(pmfNValues)-1)]
    weightedPValues = np.concatenate(([0.0], lenOfBoundarySegments * pPMFList[1:]))
    pCumulList = np.cumsum(weightedPValues)
    return pCumulList

def findAllTPowersOf2InTheFeasibleTStarRegion (pwm):
    assert pwm.tStarMin >= 0, f"{pwm.tStarMin} should be >= 0 at this stage of development"
    assert pwm.tStarMax >= 0, f"{pwm.tStarMax} should be >= 0 at this stage of development"
    
    minExponent = int(np.floor(np.log2(np.abs(pwm.tStarMin))))
    maxExponent = int(np.floor(np.log2(np.abs(pwm.tStarMax))))

    tPowersOf2 = [np.double(2**e) for e in range(minExponent, maxExponent+1)][1:]
    return tPowersOf2
def findPDFAreaBetween2Boundaries (bMinFloat, bMaxFloat, pwm):
    assert bMinFloat <= bMaxFloat, "bMin should be <= bMax"
    if bMinFloat <= pwm.L and bMaxFloat <= pwm.L:
        area = pwm.P / np.exp(pwm.eps) * (bMaxFloat - bMinFloat)
    elif bMinFloat >= pwm.L and bMaxFloat >= pwm.L and bMinFloat <= pwm.R and bMaxFloat <= pwm.R:
        area = pwm.P * (bMaxFloat - bMinFloat)
    elif bMinFloat >= pwm.R and bMaxFloat >= pwm.R:
        area = pwm.P / np.exp(pwm.eps) * (bMaxFloat - bMinFloat)
    else:
        raise Exception("The purpose of this function is to calculate areas within the same pdf probability. Bad choice of boundaries.")
    return area
def calculatePpmfFromPdfBoundariesAndArea(bMinPDF, bMaxPDF, Area, pwm):
    pPMF = Area / countPossibleFloatsBetweenTwoNumbers(bMinPDF, bMaxPDF, pwm)
    return pPMF

def transformPDFToPMF(pwm):
    pdfXBoundariesValues = np.sort(np.concatenate((findAllTPowersOf2InTheFeasibleTStarRegion(pwm), [pwm.tStarMin, pwm.tStarMax, pwm.L, pwm.R])))
    #print(f"BoundariesPDF: {pdfBoundariesValues}")

    areasPDF = [findPDFAreaBetween2Boundaries(pdfXBoundariesValues[i], pdfXBoundariesValues[i+1], pwm) for i in range(len(pdfXBoundariesValues)-1)]
    #print(f"AreasPDF: {areasPDF}, sum should be 1: {np.sum(areasPDF)}")

    pmfNBoundariesValues = [countPossibleFloatsBetweenTwoNumbers(pdfXBoundariesValues[0], pdfXBoundariesValues[i]) for i in range(len(pdfXBoundariesValues))]
    #print(f"BoundariesPMF: {pmfNBoundariesValues}")
     
    pPDFList = []
    for b in pdfXBoundariesValues:
        if b <= pwm.L:
           pPDFList.append(pwm.P / np.exp(pwm.eps))
        elif b <= pwm.R:
            pPDFList.append(pwm.P)
        else:
            pPDFList.append(pwm.P / np.exp(pwm.eps))
    pPMFList  = np.array([0.0])
    for i in range(len(pdfXBoundariesValues)-1):
        if pmfNBoundariesValues[i+1]-pmfNBoundariesValues[i] != 0.0:
            pPMFList = np.append(pPMFList, areasPDF[i]/(pmfNBoundariesValues[i+1]-pmfNBoundariesValues[i]))
        else:
            pPMFList = np.append(pPMFList, 0.0)
    
    #pPMFList = np.concatenate(([0.0], [areasPDF[i]/(pmfNBoundariesValues[i+1]-pmfNBoundariesValues[i]) for i in range(len(pdfXBoundariesValues)-1)]))
    #print(f"pPMFList: {pPMFList}")
    return pPMFList, pmfNBoundariesValues, pPDFList, pdfXBoundariesValues

def samplingCDFMethodIntXIntY (nSamples, pCumulList, pmfNBoundariesValues):
    goodNSamplesList = []
    xBoundaries = np.array(pmfNBoundariesValues)
    pCumulMax = np.max(pCumulList)
    assert np.issubdtype(pCumulMax.dtype, np.integer), "This method is meant for p to be ints"
    while(np.size(goodNSamplesList) < nSamples):
        pCumulCandidate = random.randint(0, pCumulMax)
        i = np.argmax(pCumulCandidate <= pCumulList)
        if i == 0:
            goodNSamplesList = np.append(goodNSamplesList, int(nBoundDown))
            continue
        pCumulBoundUp = pCumulList[i]
        pCumulBoundDown = pCumulList[i-1]
        assert pCumulCandidate <= pCumulBoundUp and pCumulCandidate >= pCumulBoundDown, f"Wrong selection of boundaries for pCumulCandidate = {pCumulCandidate}"
        ratioOnY = (pCumulCandidate-pCumulBoundDown) / (pCumulBoundUp-pCumulBoundDown)
        nBoundUp = xBoundaries[i]
        nBoundDown = xBoundaries[i-1]
        nCandidate = int(nBoundDown + ratioOnY*(nBoundUp - nBoundDown))
        goodNSamplesList = np.append(goodNSamplesList, nCandidate)
    return goodNSamplesList
def samplingCDFMethodIntXFloatY (nSamples, pmfPFloatsBoundariesValues, pmfNBoundariesValues):
    goodNSamplesList = []
    xBoundaries = np.array(pmfNBoundariesValues)
    pCumulList = weightedCumSumIntX(pmfNBoundariesValues, pmfPFloatsBoundariesValues)
    pCumulMax = np.max(pCumulList)
    assert pCumulMax <= 1.0, "this method is meant for p to be a float"
    while(np.size(goodNSamplesList) < nSamples):
        pCumulCandidate = random.uniform(0, pCumulMax)
        i = np.argmax(pCumulCandidate <= pCumulList)
        if i == 0:
            goodNSamplesList = np.append(goodNSamplesList, int(nBoundDown))
            continue
        pCumulBoundUp = pCumulList[i]
        pCumulBoundDown = pCumulList[i-1]
        assert pCumulCandidate <= pCumulBoundUp and pCumulCandidate >= pCumulBoundDown, f"Wrong selection of boundaries for pCumulCandidate = {pCumulCandidate}"
        ratioOnY = (pCumulCandidate-pCumulBoundDown) / (pCumulBoundUp-pCumulBoundDown)
        nBoundUp = xBoundaries[i]
        nBoundDown = xBoundaries[i-1]
        nCandidate = int(nBoundDown + ratioOnY*(nBoundUp - nBoundDown))
        goodNSamplesList = np.append(goodNSamplesList, nCandidate)
    return goodNSamplesList

def samplingRejectionMethodMultipleProbFloatXFloatY(nSamples, pdfXBoundariesValues, pdfPList):
    goodNSamplesList = []
    assert len(pdfXBoundariesValues) == len(pdfPList)
    if len(set(pdfXBoundariesValues)) < 1:
        raise Exception(f"boundaries invalid, they overlap: {pdfXBoundariesValues}")
    nAttempts = 0
    boundaries = np.array(pdfXBoundariesValues)
    bMax = np.max(boundaries)
    bMin = np.min(boundaries)
    pList = pdfPList
    pMax = np.max(pList)
    assert pMax <= 1.0, "this method is meant for p to be a float"
    while(np.size(goodNSamplesList) < nSamples):
        nCandidate = random.uniform(bMin, np.nextafter(bMax, np.inf))
        if nCandidate > bMax:
            #This could happen due to a numpy bug, I think
            continue
        pCandidate = random.uniform(0, pMax)
        i = np.argmax(nCandidate <= boundaries)
        if (pCandidate < pList[i]) or i==0:
            goodNSamplesList = np.append(goodNSamplesList, nCandidate)
        nAttempts += 1
    return goodNSamplesList
def samplingRejectionMethodMultipleProbIntXFloatY(nSamples, pmfBoundariesValues, pPMFList):
    goodNSamplesList = []
    nAttempts = 0
    boundaries = np.array(pmfBoundariesValues)
    bMax = np.max(boundaries)
    bMin = np.min(boundaries)
    pList = pPMFList
    pMax = np.max(pList)
    #assert pMax <= 1.0, "this method is meant for p to be a float"
    while(np.size(goodNSamplesList) < nSamples):
        nCandidate = random.randint(bMin, bMax)
        pCandidate = random.uniform(0, pMax)
        i = np.argmax(nCandidate <= boundaries)
        if pCandidate < pList[i] or i==0:
            goodNSamplesList = np.append(goodNSamplesList, nCandidate)
        nAttempts += 1
    return goodNSamplesList
def samplingRejectionMethodMultipleProbIntXIntY(nSamples, pmfBoundariesValues, pPMFList):
    goodNSamplesList = []
    nAttempts = 0
    boundaries = np.array(pmfBoundariesValues)
    bMax = np.max(boundaries)
    bMin = np.min(boundaries)
    pList = pPMFList
    pMax = np.max(pList)
    #assert np.issubdtype(pMax.dtype, np.integer), "This method is meant for p to be ints"
    #they are meant to be int only in the discreteCDF, not in the pmf
    while(np.size(goodNSamplesList) < nSamples):
        nCandidate = random.randint(bMin, bMax)
        pCandidate = random.uniform(0, pMax)
        #This has to be uniform, since they are INT only in the CDF, here they are FP
        #Since here we are using the PMF
        i = np.argmax(nCandidate <= boundaries)
        if pCandidate < pList[i]:
            goodNSamplesList = np.append(goodNSamplesList, nCandidate)
        nAttempts += 1
    return goodNSamplesList

def calculateFactorForPCumulFloatToPCumulInts(boundaries, pCumulListFloat):
    assert len(boundaries) == len(pCumulListFloat)
    assert pCumulListFloat[0] == 0.0
    
    nNumbersBetweenBoundaries = np.array([boundaries[i+1]-boundaries[i] for i in range(len(boundaries)-1)])
    distanceBetweenPCumulFloats = np.array([pCumulListFloat[i+1]-pCumulListFloat[i] for i in range(len(pCumulListFloat)-1)])
    f = np.max(nNumbersBetweenBoundaries / distanceBetweenPCumulFloats)
    return f

def calculatePCumulIntsFromPCumulFloats(boundaries, pCumulListFloat):
    f = calculateFactorForPCumulFloatToPCumulInts(boundaries, pCumulListFloat)
    #pCumulListInt = np.ceil(f*np.array(pCumulListFloat))
    pCumulListInt = (f*np.array(pCumulListFloat)).astype(int)
    return pCumulListInt, f

def inverseOfWeightedCumSum(pCumulList, pmfNValues):
    assert len(pmfNValues) == len(pCumulList)
    z = pCumulList.copy()
    z[1:] -= z[:-1].copy()
    lenOfBoundarySegments = np.array([pmfNValues[i+1] - pmfNValues[i] for i in range(len(pmfNValues)-1)])
    pList = np.concatenate(([0.0],  z[1:] / lenOfBoundarySegments ))
    return pList

def testDifferenceBetweenProbCumulIntervalRatio(pCumulListInts, pCumulListFloat):
    distancesBetweenPCumulFloats = [pCumulListFloat[i+1] - pCumulListFloat[i] for i in range(len(pCumulListFloat)-1)]
    ratioBetweenPCumulDistancesFloats = np.divide(np.vstack([distancesBetweenPCumulFloats]*len(distancesBetweenPCumulFloats)),np.vstack(distancesBetweenPCumulFloats))

    distancesBetweenPCumulInts = [pCumulListInts[i+1] - pCumulListInts[i] for i in range(len(pCumulListInts)-1)]
    ratioBetweenPCumulDistancesInts = np.divide(np.vstack([distancesBetweenPCumulInts]*len(distancesBetweenPCumulInts)),np.vstack(distancesBetweenPCumulInts))

    maxDifference = np.max(ratioBetweenPCumulDistancesFloats - ratioBetweenPCumulDistancesInts)
    return maxDifference, ratioBetweenPCumulDistancesFloats, ratioBetweenPCumulDistancesInts

def fromPFloatToPInt(pListFloat, xboundaries):
    pCumulListFloat = weightedCumSumIntX(xboundaries, pListFloat)
    pCumulListInts, f = calculatePCumulIntsFromPCumulFloats(xboundaries, pCumulListFloat)
    pList = inverseOfWeightedCumSum(pCumulListInts, xboundaries)
    return pList

def fromPFloatToCumulPInt(pListFloat, nboundaries):
    pCumulListFloat = weightedCumSumIntX(nboundaries, pListFloat)
    pCumulListInts, f = calculatePCumulIntsFromPCumulFloats(nboundaries, pCumulListFloat)
    return pCumulListInts

def privatizeDataset(pwm, Abar, DMod ):
    privateDS = []
    for ti in DMod:
        pwm.updateAllParameters(ti, Abar, pwm.Ebar, pwm.E, pwm.eps)
        pdfXBoundariesValues = [pwm.Ebar-pwm.C + pwm.Abar, pwm.L , pwm.R , pwm.Ebar+pwm.C+ pwm.Abar]
        pdfPList = [0.0, pwm.P / np.exp(pwm.eps), pwm.P, pwm.P / np.exp(pwm.eps)]

        #pPMFListFloat, pmfNValues,_,_ = su.transformPDFToPMF(pwm)
        #intfptStarINT = su.samplingRejectionMethodMultipleProbIntXFloatY(1, pmfNValues, pPMFListFloat)
        #tiStarList = [su.addMantissaIntToFloat(pwm.tStarMin, sample) for sample in intfptStarINT]
        #privateDS = np.append(privateDS,tiStarList)
        privateDS = np.append(privateDS, samplingRejectionMethodMultipleProbFloatXFloatY(nSamples = 1,  pdfXBoundariesValues = pdfXBoundariesValues, pdfPList = pdfPList))
    return privateDS
def analyzeAbarSingleDS (Abar, pwm, DMod, checkForSameExp = True, privateDS = None):
    originalAverage = np.average(DMod)
    if privateDS is None:   
        privateDS = privatizeDataset(pwm, Abar, DMod)
    if checkForSameExp:
        lowerPowerOf2Set = set([getFPUnbiasedExponent64bits(tiStar) for tiStar in privateDS])
        if len(lowerPowerOf2Set) > 1:
            raise Exception(f"DS not sharing the exponent: minExp = {getFPUnbiasedExponent64bits(np.min(privateDS))}, maxExp = {getFPUnbiasedExponent64bits(np.max(privateDS))}, Abar = {Abar}")
    errorPercOnAvg = (np.average(privateDS-Abar)- originalAverage)/originalAverage
    errorAbsOnAvg = np.average(privateDS-Abar)- originalAverage
    return errorPercOnAvg, errorAbsOnAvg
    
def analyzeAbarMultipleIterationsOfDS (Abar, pwm, DMod, iterationsForAveragingResults, checkForSameExp = True):
    errorPercOnAvgForEachIteration = []
    errorAbsOnAvgForEachIteration = []
    for _ in range(iterationsForAveragingResults):
        errorPercOnAvg, errorAbsOnAvg = analyzeAbarSingleDS (Abar, pwm, DMod, checkForSameExp = checkForSameExp)
        errorPercOnAvgForEachIteration = np.append(errorPercOnAvgForEachIteration, errorPercOnAvg)
        errorAbsOnAvgForEachIteration = np.append(errorAbsOnAvgForEachIteration, errorAbsOnAvg )
    return np.average(np.abs(errorAbsOnAvgForEachIteration)), np.average(np.abs(errorPercOnAvgForEachIteration))