#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 单线程和多线程执行速度对比

from time import ctime, sleep

from utils.threadutil import MyThread


# 斐波那契数
def fib(x):
    sleep(0.005)
    if x < 2:
        return 1
    return fib(x - 2) + fib(x - 1)


# 阶乘
def fac(x):
    sleep(0.1)
    if x < 2:
        return 1
    return x * fac(x - 1)


def sum(x):
    sleep(0.1)
    if x < 2:
        return 1
    return x + sum(x - 1)


funcs = [fib, fac, sum]
n = 12


def main():
    nfuncs = range(len(funcs))

    print('******Single Thread******')
    for i in nfuncs:
        print('starting ', funcs[i].__name__, ' at', ctime())
        print(funcs[i](n))
        print(funcs[i].__name__, ' finished at ', ctime())

    print('******Multiple Thread******')
    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (n,), funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()
        print(threads[i].get_result())

    print('All done')


if __name__ == '__main__':
    main()
