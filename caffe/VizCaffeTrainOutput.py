#!/usr/bin/python
from __future__ import print_function
import numpy as np
def CreateArgumentParser():
    import argparse
    import textwrap
    ap = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''\
                This tool is used to ...
             '''),
            # After the help
            epilog=textwrap.dedent('''\
                examples:
                ---------------------------------------------------------------------------
             ''')
            )

    ap.add_argument("train_out_files", nargs = '*',
                    help="Caffe training output files")

    ap.add_argument("-x", "--xrange", nargs = '+', type = int, default = None,
                    help="<x_min [<x_max>]>")

    ap.add_argument("-c", "--concatenate_logs", action="store_true",
                    help="concatenate training out logs")
    ap.add_argument("-m", "--concatenate_mode", type=int, default = 0,
                    help="log concatenate mode: 0 = don't adjust iteration number")


    ap.add_argument("-l", "--logy", action="store_true", default = False,
                    help="log y scale")

    ap.add_argument("--accuracy_min", default = None, type = float,
                    help="min accuracy for display")

    ap.add_argument("-w", "--avg_window_size", type = int,
                    help="average window size in iterations")    

    return ap


def GetTrainStat( trainOut ):
    """
    :param trainOut: any iterable object, e.g., file object, sys.stdin
    :return:

    I1029 14:52:44.493795 25829 solver.cpp:330] Iteration 57000, Testing net (#0)
    I1029 14:52:46.712065 25829 solver.cpp:397]     Test net output #0: accuracy = 0.747
    I1029 14:52:46.712085 25829 solver.cpp:397]     Test net output #1: loss = 0.805219 (* 1 = 0.805219 loss)

    I1029 14:52:46.795838 25829 solver.cpp:218] Iteration 57000 (10.5908 iter/s, 18.8844s/200 iters), loss = 0.745292
    I1029 14:52:46.796061 25829 solver.cpp:237]     Train net output #0: loss = 0.745292 (* 1 = 0.745292 loss)

    I1029 14:52:46.796069 25829 sgd_solver.cpp:105] Iteration 57000, lr = 0.01

    I1029 14:56:45.001917 25829 solver.cpp:218] Iteration 59800 (11.9675 iter/s, 16.7119s/200 iters), loss = 0.612757
    I1029 14:56:45.001960 25829 solver.cpp:237]     Train net output #0: loss = 0.612757 (* 1 = 0.612757 loss)
    I1029 14:56:45.001963 25829 sgd_solver.cpp:105] Iteration 59800, lr = 0.01

    I1029 14:57:01.641068 25829 solver.cpp:310] Iteration 60000, loss = 0.711669
    I1029 14:57:01.641083 25829 solver.cpp:330] Iteration 60000, Testing net (#0)
    I1029 14:57:03.798398 25829 solver.cpp:397]     Test net output #0: accuracy = 0.7553
    I1029 14:57:03.798415 25829 solver.cpp:397]     Test net output #1: loss = 0.792614 (* 1 = 0.792614 loss)
    """
    import re

    if isinstance( trainOut, basestring):
        try:
            dataSrc = open(trainOut, 'r')
        except IOError:
            import sys
            print('ERROR: failed to open {}'.format(trainOut) )
            sys.exit(-1)
    else:
        dataSrc = trainOut

    curIterIdx = None
    result = type('',(),{})
    result.listTrainIter = []
    result.listTrainLoss = []
    result.listTestIter = []
    result.listTestAccuracy = []
    for line in dataSrc:
        m = re.search(r'Iteration\s+(\d+)', line)
        if m:
            curIterIdx = int( m.group(1) )

        m = re.search(r'Train\s+net\s+output\s+.+loss\s+=\s+([\d\.]+)', line)
        if m:
            result.listTrainIter.append(curIterIdx)
            result.listTrainLoss.append( float(m.group(1)) )

        #m = re.search(r'Test\s+net\s+output\s+.+accuracy\s+=\s+([\d\.]+)', line)
        m = re.search(r'Test\s+net\s+output\s+.+detection_eval\s+=\s+([\d\.]+)', line)
        if m:
            result.listTestIter.append(curIterIdx)
            result.listTestAccuracy.append( float(m.group(1)) )

    if isinstance(trainOut, basestring):
        dataSrc.close()

    return result

#def PlotTrainTestResult( result ):

def MovingAverage (values, window, mode='same'):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, mode)
    return sma

def AppendTrainingStat( src, tgt, catMode = 0):
    src.listTrainLoss += tgt.listTrainLoss
    src.listTestAccuracy += tgt.listTestAccuracy

    off = src.listTrainIter[-1] if catMode != 0 else 0
    src.listTrainIter += [ e + off for e in tgt.listTrainIter ]

    off = src.listTestIter[-1] if catMode != 0 else 0
    src.listTestIter += [ e + off for e in tgt.listTestIter ]

    return src

def LoadTrainingStat( list_srcSpec, catFlag = False, catMode = 0):
    import glob

    results = []
    legends = []
    if catFlag:
        rst = None
    for srcSpec in list_srcSpec:
        print('Loading ' + srcSpec if isinstance(srcSpec, basestring) else 'stdin')
        if isinstance(srcSpec, basestring): 
            for dataFile in glob.glob(srcSpec):
                r = GetTrainStat( dataFile )
                if not catFlag:
                    results.append(r)
                    _, fname = os.path.split(dataFile)
                    legends.append( os.path.splitext(fname)[0] )
                elif rst is not None:
                    AppendTrainingStat(rst, r, catMode)
                else:
                    rst = r
        else:
            if not catFlag:
                results.append(GetTrainStat(srcSpec))
                legends.append('stdin')
            elif rst is not None:
                AppendTrainingStat(rst, r, catMode)
            else:
                rst = r            

    if catFlag:
        results = [rst]
        legends = ['']

    for r in results:
        r.listTrainIter = np.array(r.listTrainIter, dtype=np.int)
        r.listTrainLoss = np.array(r.listTrainLoss)
        r.listTestIter  = np.array(r.listTestIter, dtype=np.int)
        r.listTestAccuracy = np.array(r.listTestAccuracy)

    return results, legends

if __name__ == '__main__':
    ap = CreateArgumentParser()
    args = ap.parse_args()

    import sys
    import os.path
    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    if args.logy:
        # pltFunc = plt.semilogx  # loglog
        pltFunc1 = ax1.semilogy  # loglog
        pltFunc2 = ax2.semilogy  # loglog
    else:
        pltFunc1 = ax1.plot
        pltFunc2 = ax2.plot

    if len(args.train_out_files) <= 0:
        args.train_out_files = [sys.stdin]


    list_result, pltLegend = LoadTrainingStat(args.train_out_files, 
                                args.concatenate_logs,
                                args.concatenate_mode
                            )

    xmin = xmax = 0
    idx_min = idx_max = 0        
    max_accuracy = 0.0
    for result in list_result:
        pltFunc1(result.listTrainIter, result.listTrainLoss)
        if args.avg_window_size is not None:  
            # [::-1] create a reversed-order view of the array                    
            # a = np.append(result.listTrainLoss, 
            #                     np.repeat(result.listTrainLoss[-1], args.avg_window_size-1)
            # )
            #a = np.array([result.listTrainLoss[i] for i in xrange(result.listTrainLoss.shape[0]-1, -1, -1) ])
            avg_loss = MovingAverage(result.listTrainLoss, args.avg_window_size)                    
            #avg_loss = MovingAverage(result.listTrainLoss[::-1], args.avg_window_size)
            pltFunc1(result.listTrainIter, avg_loss)                

        #plt.subplot(2, 1, 2)
        pltFunc2(result.listTestIter, result.listTestAccuracy, 'r')
        m = np.max(result.listTestAccuracy)
        if max_accuracy < m:      max_accuracy = m

        i = np.argmin(result.listTrainIter)
        if xmin > result.listTrainIter[i]:
            xmin = result.listTrainIter[i]
            idx_min = i
        i = np.argmax(result.listTrainIter)
        if xmax < result.listTrainIter[i]:
            xmax = result.listTrainIter[i]
            idx_max = i

    if args.xrange is None:
        args.xrange = (xmin, xmax)
    elif len(args.xrange) < 2:
        idx_min = np.searchsorted(result.listTrainIter, args.xrange[0])
        args.xrange.append(xmax)        
    plt.legend( pltLegend )

    #plt.subplot(2, 1, 1)
    ax1.set_ylabel('Train Loss')
    ax1.set_xlabel('Train Iteration')    
    # plt.grid(b=True, which='major')
    # plt.grid(b=True, which='minor',linestyle='--')
    # To show grid only for ax2 (details at http://matplotlib.1069221.n5.nabble.com/full-grid-for-2nd-y-axis-wit-twinx-td41259.html)
    #  - xaxis grid is shown in ax1  # twinx => no xaxis grid for ax2
    #  - yaxis grid is hidden in ax1
    #   ax1.grid()
    #   ax2.grid()
    #   ax1.yaxis.grid(False)
    # ax1.grid()    
    ax1.xaxis.grid(b=True, which='major')  # 'both'
    ax1.xaxis.grid(b=True, which='minor',linestyle=':')
    # # see https://stackoverflow.com/questions/19940518/cannot-get-minor-grid-lines-to-appear-in-matplotlib-figure
    # #for why ax.minorticks_on is needed
    ax1.minorticks_on()

    ax1.set_ylim( (np.min(result.listTrainLoss[idx_min:idx_max+1]), 
               np.max(result.listTrainLoss[idx_min:idx_max+1])
               )
    )
    ax1.set_xlim(args.xrange)    
    #plt.subplot(2, 1, 2)
    # plt.grid(b=True, which='major')
    # plt.grid(b=True, which='minor',linestyle='--')
    ax2.set_ylabel('mAP')
    # ax2.grid(b=True, which='major', axis='both')
    # ax2.grid(b=True, which='minor',axis='both', linestyle=':')    
    ax2.yaxis.grid(b=True, which='major')
    ax2.yaxis.grid(b=True, which='minor', linestyle=':')        
    #ax1.yaxis.grid(False)    
    # see https://stackoverflow.com/questions/19940518/cannot-get-minor-grid-lines-to-appear-in-matplotlib-figure
    #for why ax.minorticks_on is needed
    ax2.minorticks_on()    
    if args.accuracy_min is not None:
        ax2.set_ylim((args.accuracy_min, max_accuracy))

    #plt.xlim(args.xrange)    
    plt.show()