#!/usr/bin/env python3


class SpatialOrbitalIndex:
    '''A single spatial orbital index'''
    def __init__(self, idx:int):
        self.idx = idx
    def __str__(self) -> str:
        return str(self.idx)
    
#examples:
p = SpatialOrbitalIndex(0)
print("Created spatial orbital " + str(p))


class SingleElectronSpin:
    '''A single electron's spin (either alpha or beta)'''
    def __init__(self, spin:bool):
        self.sz = spin
    
    @classmethod
    def from_str(cls, spin:str):
        if (spin == '+'):
            return cls(False)
        elif (spin == '-'):
            return cls(True)
        else:
            raise ValueError("Wrong string input for SingleElectronSpin.from_str( " + spin + " )")
    
    def __str__(self) -> str:
        if (self.sz == False):
            return "+"
        else:
            return "-"

#examples:
up = SingleElectronSpin(False) #either bool input
down = SingleElectronSpin.from_str("-") #or from string
print("Created spin up: " + str(up) + " and spin down: " + str(down))


import re

class SpinOrbitalIndex:
    '''A single spin orbital index composed of 
    (i) a spatial orbital index (SpatialOrbitalIndex) 
    (ii) a single spin (SingleElectronSpin)'''
    def __init__(self, idx:SpatialOrbitalIndex, spin:SingleElectronSpin):
        self.mo_idx = idx
        self.spin = spin

    @classmethod
    def from_str(cls, s:str):
        if re.match("^([0-9]+[+|-])", s):
            match = re.findall("^([0-9]+)([+|-])", s)
            return cls(SpatialOrbitalIndex(int(match[0][0])), SingleElectronSpin.from_str(match[0][1]))
        else:
            raise ValueError("Wrong string input for SpinOrbitalIndex.from_str( " + s + " )")

    def integrate_spin(self, other):
        if self.spin.sz == other.spin.sz:
            return 1.0
        return 0.0

    #Transform stored spatial orbital index and spin to unique spin orbital index
    def so_idx(self) -> int:
        return 2*self.mo_idx.idx + self.spin.sz

    def __str__(self) -> str:
        return str(self.mo_idx) + str(self.spin)
    
    #define comparison operators to allow usage in SortedList
    def __hash__(self) -> int:
        return self.so_idx()
    def __eq__(self, other) -> bool:
        return self.so_idx() == other.so_idx()
    def __lt__(self, other) -> bool:
        return self.so_idx() < other.so_idx()
    
#examples 
p_up = SpinOrbitalIndex(p, up)
p_down = SpinOrbitalIndex.from_str("0-")
print("Created spin orbitals " + str(p_up) + " and " + str(p_down))


from sortedcontainers import SortedSet
from typing import List

class SlaterDeterminant:
    '''A single Slater determinant composed of 
    (i) a sorted set of spin orbitals 
    (ii) a sign
    To ensure the correct sign, use create/annihilate functions to add or remove orbitals'''

    #initialize from orbital list (possibly unsorted)
    #create orbitals in reversed order. 
    #e.g.( [0+,1-,2+,1+], +1) -> +|1+> -> -|1+, 2+> -> +|1+, 1-, 2+> -> +|0+, 1+, 1-, 2+>
    def __init__(self, orbitals:List[SpinOrbitalIndex] = [], sign:int = +1):
        self.orbitals = SortedSet([])
        self.sign = sign
        for i in orbitals[::-1]:
            self.create(i)

    #construct directly from orbital string e.g. "0+1-2+..."
    #orbitals will be created in reversed order! (..., 2+, 1-, 0+) 
    @classmethod
    def from_str(cls, orbitalstring:str, sign:int = +1):
        if re.match("^([0-9]+[+|-])", orbitalstring):
            matches = re.findall("([0-9]+[+|-])", orbitalstring)
            orbitallist = []
            for i in matches:
                o = SpinOrbitalIndex.from_str(i)
                orbitallist.append(o)
            return cls(orbitallist, sign)
        else:
            raise ValueError("Wrong string input for SlaterDeterminant.from_str( " + orbitalstring + " )")

    def create(self, so:SpinOrbitalIndex):
        if self.sign == 0:
            return #do nothing if determinant vanished due to nilpotency
        if so in self.orbitals: #if orbital is already occupied, determinant vanishes
            self.orbitals.clear() 
            self.sign = 0 #!!! set sign to zero here, to distinguish true zero with Fermi vacuum |>
        else:
            if self.nelectrons() == 0: #if there are no occupied orbitals so far, just insert 
                self.orbitals.add(so)
            else:
                #iterate to position where new orbital would be added 
                it = iter(self.orbitals)
                element = next(it)
                count = 0
                while element < so:
                    count = count + 1
                    try:
                        element = next(it)
                    except StopIteration:
                        break
                #spin orbital would be added after 'count' indices -> multiply sign by (-1)^count
                if (count % 2 == 1):
                    self.sign = -1*self.sign
                self.orbitals.add(so)
    
    def annihilate(self, so:SpinOrbitalIndex):
        if self.sign == 0:
            return #do nothing if determinant vanished due to nilpotency
        if so not in self.orbitals: #if orbital is not occupied, determinant vanishes 
            self.orbitals.clear()
            self.sign = 0 #!!! set sign to zero here, to distinguish true zero with Fermi vacuum |>
        else:
            ann_idx = self.orbitals.index(so) #get index of annihilated orbital
            #orbital is annihilated arfter 'ann_idx' indices -> multiply sign by (-1)^ann_idx
            if (ann_idx % 2 == 1):
                self.sign = -1*self.sign
            self.orbitals.remove(so)


    def nelectrons(self) -> int:
        return len(self.orbitals)

    def __iter__(self):
        self.iter = iter(self.orbitals)
        return self.iter
    def __next__(self):
        return self.iter.__next__()

    def __str__(self):
        output = ""
        if self.sign == -1:
            output = output + "-"
        elif self.sign == 0:
            output = output + "0"
        else:
            output = output + "+"
        if (self.nelectrons() == 0):
            return output + "|>"
        it = iter(self.orbitals)
        element = next(it)
        output = output + "|" + str(element)
        while True:
            try:
                element = next(it)
                output = output + ", " + str(element)
            except StopIteration:
                break
        output = output + ">"
        return output
    
#examples 
det1 = SlaterDeterminant([p_up, p_down], +1)
det2 = SlaterDeterminant.from_str("0+0-", -1)
det3 = SlaterDeterminant.from_str("0-0+", +1) #beware: creation in reversed order! This possibly changes sign
print("Created Slater determinants " + str(det1) + " , " + str(det2) + " , and " + str(det3))


from typing import Dict
import math

class ConfigurationStateFunction(Dict[SlaterDeterminant, float]):
    '''A single configuration state function (linear combination of Slater Determinants) 
    -> inherting from dict mapping SlaterDeterminant -> prefactor (float)'''
    
    @classmethod
    def from_str(cls, stringmap:Dict[str, float]):
        detmap = {}
        for i in stringmap.items():
            detmap[SlaterDeterminant.from_str(i[0])] = i[1]
        return cls(detmap)
    
    def __str__(self):
        output = ""
        it = iter(self.items())
        keyvalue = next(it)
        output += str(keyvalue[1]) + "*" + str(keyvalue[0])
        while True:
            try:
                keyvalue = next(it)
                output += " + " +  str(keyvalue[1]) + "*" + str(keyvalue[0])
            except StopIteration:
                break
        return output
    
#examples 
csf1 = ConfigurationStateFunction({det1 : 1.0})
csf2 = ConfigurationStateFunction.from_str({"0+1-" : +1.0/math.sqrt(2.0), "0-1+" : -1.0/math.sqrt(2.0)})
print ("Created CSFs " + str(csf1) + " and " + str(csf2))


import numpy as np
from itertools import tee
import copy

def access_4s_pyscf_integrals(moints2, i:int, j:int, k:int, l:int) -> np.float64:
    '''Comfortable 4 index access to pyscf 2p integrals in mo basis with 4-fold symmetry (chemist notation!!!)'''
    #sort value pairs ij and kl 
    ij = sorted([i,j])
    kl = sorted([k,l])
    #calculate super indices (lower triangular matrix in column major order!)
    idx1 = int((ij[1]+1)*ij[1]/2 + ij[0])
    idx2 = int((kl[1]+1)*kl[1]/2 + kl[0])
    return moints2[idx1, idx2]

def slater_condon_rules(bra:SlaterDeterminant, ket:SlaterDeterminant, moints1, moints2) -> np.float64:
    '''Given two Slater determinants 'bra' and 'ket', and the 1 and 2 particle 
    integrals im MO basis 'moints1' and 'moints2', respectively, calculate <bra|H|ket>''' 
    result = 0.0

    #(1) extract (i) annihilators, (ii) creators, and (iii) common indices for the substitution ket -> bra
    annihilators = ket.orbitals.difference(bra.orbitals) 
    creators = bra.orbitals.difference(ket.orbitals)
    common = bra.orbitals.intersection(ket.orbitals)

    #check Slater Condon rule case (from substitution order)
    if len(annihilators) == 0:
        #Case 1: <Psi|H|Psi> = sum_(i in Psi) <i|h(1)|i> + sum_(i<j in Psi) <ij|g(1,2)|ij-ji>
        it1 = iter(bra)
        while True:
            try:
                so_i = next(it1) #SpinOrbitalIndex used for spin integration later
                i = so_i.mo_idx.idx 
                it1,it2 = tee(it1) #copy iterator using tee
                #<i|i> (spin integration is always 1) 
                result += moints1[i,i] 
                while True:
                    try:
                        so_j = next(it2)
                        j = so_j.mo_idx.idx
                        #<ij|ij> = [ii|jj] (spin integral is always 1)
                        result += access_4s_pyscf_integrals(moints2, i,i,j,j) 
                        #<ij|ji> = [ij|ji]
                        result -= so_i.integrate_spin(so_j) * access_4s_pyscf_integrals(moints2, i,j,j,i)
                    except StopIteration:
                        break
            except StopIteration:
                break
    elif len(annihilators) == 1:
        #Case 2: <Psi|H|Psi_I^A> = <I|h(1)|A> + sum_(i in Psi) <Ii|g(1,2)|Ai-iA>
        so_I = annihilators[0]
        I = so_I.mo_idx.idx
        so_A = creators[0]
        A = so_A.mo_idx.idx
        #<I|A>
        result += so_I.integrate_spin(so_A) * moints1[I,A]
        for so_i in bra.orbitals: 
            i = so_i.mo_idx.idx 
            #<Ii|Ai> = [IA|ii]
            result += so_I.integrate_spin(so_A) * access_4s_pyscf_integrals(moints2, I,A,i,i)
            #<Ii|iA> = [Ii|iA]
            result -= so_I.integrate_spin(so_i) * so_i.integrate_spin(so_A) * access_4s_pyscf_integrals(moints2, I,i,i,A)
    elif len(annihilators) == 2:
        #Case 3: <Psi|H|Psi_IJ^AB> = <IJ|g(1,2)|AB - BA>
        so_I = annihilators[0]
        I = so_I.mo_idx.idx 
        so_J = annihilators[1]
        J = so_J.mo_idx.idx
        so_A = creators[0]
        A = so_A.mo_idx.idx 
        so_B = creators[1] 
        B = so_B.mo_idx.idx 
        #<IJ|AB> = [IA|JB]
        result += so_I.integrate_spin(so_A) * so_J.integrate_spin(so_B) * access_4s_pyscf_integrals(moints2, I,A,J,B)
        #<IJ|BA> = [IB|JA]
        result -= so_I.integrate_spin(so_B) * so_J.integrate_spin(so_A) * access_4s_pyscf_integrals(moints2, I,B,J,A)


    #before returning the result, take care of determinant signs and signs introduced by substitution 
    temp = copy.deepcopy(ket) 
    for i in annihilators:
        temp.annihilate(i)
    for i in creators[::-1]:
        temp.create(i)
    return bra.sign * temp.sign * result


#overhead for CSFs -> calls determinant routine 'slater_condon_rules' for all combinations
def slater_condon_rules_csf(bra:ConfigurationStateFunction, 
                            ket:ConfigurationStateFunction, 
                            moints1, 
                            moints2) -> np.float64:
    result = 0.0
    for i in bra.items():
        for j in ket.items():
            result += i[1]*j[1]*slater_condon_rules(i[0], j[0], moints1, moints2)
    return result


