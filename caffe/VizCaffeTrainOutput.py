#!/usr/bin/python
from __future__ import print_function

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
    ap.add_argument("-l", "--logx", action="store_true",
                    help="log x scale")

    ap.add_argument("train_out_files", nargs = '*',
                    help="Caffe training output files")

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


if __name__ == '__main__':
    ap = CreateArgumentParser()
    args = ap.parse_args()

    import sys
    import os.path
    import matplotlib.pyplot as plt

    if args.logx:
        pltFunc = plt.semilogx  # loglog
    else:
        pltFunc = plt.plot

    if len(args.train_out_files) <= 0:
        result = GetTrainStat(sys.stdin)
        plt.subplot(2, 1, 1)
        pltFunc(result.listTrainIter, result.listTrainLoss)
        plt.subplot(2, 1, 2)
        pltFunc( result.listTestIter, result.listTestAccuracy)
    else:
        import glob
        pltLegend = []
        for fp in args.train_out_files:
            for dataFile in glob.glob(fp):
                result = GetTrainStat( dataFile )
                _, fname = os.path.split(dataFile)
                pltLegend.append( os.path.splitext(fname)[0] )
                plt.subplot(2, 1, 1)
                pltFunc(result.listTrainIter, result.listTrainLoss)
                plt.subplot(2, 1, 2)
                pltFunc(result.listTestIter, result.listTestAccuracy)
        plt.legend( pltLegend )

    plt.subplot(2, 1, 1)
    plt.ylabel('Train Loss')
    plt.grid(b=True, which='major')
    plt.grid(b=True, which='minor',linestyle='--')

    plt.subplot(2, 1, 2)
    plt.grid(b=True, which='major')
    plt.grid(b=True, which='minor',linestyle='--')
    plt.xlabel('Train Iteration')
    plt.ylabel('Test Accuracy')
    plt.show()