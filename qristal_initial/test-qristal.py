#!/usr/bin/env python3

import qb.core

tqb=qb.core.session()
tqb.qb12()
tqb.qn=4
tqb.random=3
tqb.run()

print(tqb.out_raw[0])
