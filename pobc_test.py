#!/usr/bin/env python

import os
import sys
import getopt



def usage():
    
    u = '''
    Name:
        %s - POBC automate test tool 

    Synopsis:
        %s [-h] [-c cmd] [-p params]

    Description:
        Arguments are as following:
            -h  Print the help message
            -c  Configuration mode, ex:
            	    TestAll		test all case
                    InterfaceTest	interface test
                    ComponentTest	component test
		    ApiTest		raspberrypi interface test
    '''

    prog = os.path.basename(sys.argv[0])
    print('Usage:')
    print(u % (prog, prog))
    sys.exit(1)

def TestAll(params):
    print('Test all')

def InterfaceTest(params):
    print('Interface test')

def ComponentTest(params):
    print('Component test')

def ApiTest(params):
    print('Api test')

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:p:")
    except getopt.GetoptError as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(limit=1, file=sys.stdout)
        sys.exit(1)

    cmd = ''
    params = ''
    for op, value in opts:
        if op == '-h':
            usage()
        elif op == '-c':
            cmd = value
        elif op == '-p':
            params = value
        else:
            usage()
    if cmd == 'TestAll':
        TestAll(params)
    elif cmd == 'InterfaceTest':
        InterfaceTest(params)
    elif cmd == 'ComponentTest':
        ComponentTest(params)
    elif cmd == 'ApiTest':
        ApiTest(params)
    else:
        print('Unknown command %s' % cmd)
