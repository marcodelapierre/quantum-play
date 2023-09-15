#!/usr/bin/env python3

import qb.core

tqb=qb.core.session()
tqb.qb12()

tqb.sn=32
tqb.qn=2
tqb.acc='qdk_gen1'

tqb.instring='''
    __qpu__ void QBCIRCUIT(qreg q) {
    OPENQASM 2.0;
    include "qelib1.inc";
    creg c[2];
    h q[0];
    measure q[1] -> c[1];
    measure q[0] -> c[0];
    }'''

tqb.run()

print(tqb.out_raw[0])

