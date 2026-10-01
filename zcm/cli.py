from __future__ import annotations
import argparse
from scm.chemistry import assign_oxidation_states, gibbs_free_energy

def main(argv=None):
    p=argparse.ArgumentParser(prog='zcm')
    sub=p.add_subparsers(dest='command',required=True)
    ox=sub.add_parser('oxidation'); ox.add_argument('formula'); ox.add_argument('--charge',type=int,default=0)
    dg=sub.add_parser('gibbs'); dg.add_argument('delta_h',type=float); dg.add_argument('delta_s',type=float); dg.add_argument('temperature',type=float)
    a=p.parse_args(argv)
    if a.command=='oxidation':
        r=assign_oxidation_states(a.formula,a.charge)
        print(r)
    else:
        print(gibbs_free_energy(a.delta_h,a.delta_s,a.temperature))

if __name__=='__main__': main()
