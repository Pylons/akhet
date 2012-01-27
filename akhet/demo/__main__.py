import os
import sys

import pkg_resources as pkgr
import pyramid.scripts.pserve as pserve
import akhet.demo

def main():
    args = sys.argv[:]
    if args and args[-1].lower().endswith(".ini"):
        pass
    else:
        ini_file = pkgr.resource_filename("akhet.demo", "development.ini")
        args.append(ini_file)
    print("Running 'pserve' with config file {}".format(ini_file))
    pserve.main(args)

if __name__ == "__main__":  main()
