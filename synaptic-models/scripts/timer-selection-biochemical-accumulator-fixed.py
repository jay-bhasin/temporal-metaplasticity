import numpy as np
import os
import sys
import argparse

import sys
sys.path.insert(0, '../utils')

import tqdm

import te_mp

parser = argparse.ArgumentParser()
parser.add_argument("directory", help="directory to store output files")
parser.add_argument("iters", help="number of iterations to run",type=int)
parser.add_argument("-i", "--itr_report", help="record output every n iterations", type=int, default=1)
parser.add_argument("-v0", "--v0", help="Path to initial couplings", type=str,default="")
# parser.add_argument("-s", "--sims", help="number of simulations to run",type=int, default=1)

def bimodal_distr(t):
    distr = np.exp(-(t-0.05)**2/(2*0.025**2)) + 2*np.exp(-(t-0.14)**2/(2*0.025**2))
    distr /=np.sum(distr)
    return distr

def __main__():
    args = parser.parse_args()
    
    ## Time vector
    dt_mp = 1e-3
    T_mp_max = 0.2

    tau = np.arange(0, int(T_mp_max/dt_mp))*dt_mp

    single_timer_adjustment_discretization = np.load('../utils/timer_adj_discretization.npy')
    biochem_timer_bank = np.copy(single_timer_adjustment_discretization[::17, 3, :])

    ## Setup distribution
    # Use example bimodal distribution (see text)
    distr = bimodal_distr(tau)

    cdf = np.cumsum(distr)
    get_interval = lambda r: np.interp(r, cdf, tau)

    if not os.path.isdir(args.directory):
        os.makedirs(args.directory)

    # leave_trange = False if args.sims > 1 else True

    if args.v0 == "":
        v_0 = np.ones(biochem_timer_bank.shape[0])*1/biochem_timer_bank.shape[0]
    else:
        v_0 = np.load(args.v0)

    # Run simulation
    v_final, v_all = te_mp.selectionFixed(tau, biochem_timer_bank, v_0, get_interval, its=args.iters, report_its = args.itr_report)
    np.save(args.directory + '/v_all.npy', v_all)
    np.save(args.directory + '/v_final.npy', v_final)

if __name__ == "__main__":
    __main__()