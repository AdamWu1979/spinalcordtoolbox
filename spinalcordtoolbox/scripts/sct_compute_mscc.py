#!/usr/bin/env python
#########################################################################################
#
# Compute maximum spinal cord compression.
#
# ---------------------------------------------------------------------------------------
# Copyright (c) 2015 Polytechnique Montreal <www.neuro.polymtl.ca>
# Author: Julien Cohen-Adad
#
# About the license: see the file LICENSE.TXT
#########################################################################################

import sys
import os
import argparse

from spinalcordtoolbox.utils import Metavar, SmartFormatter, init_sct, printv, set_global_loglevel


# PARSER
# ==========================================================================================
def get_parser():
    # parser initialisation

    parser = argparse.ArgumentParser(
        description='Compute Maximum Spinal Cord Compression (MSCC) as in: Miyanji F, Furlan JC, Aarabi B, Arnold PM, '
                    'Fehlings MG. Acute cervical traumatic spinal cord injury: MR imaging findings correlated with '
                    'neurologic outcome--prospective study with 100 consecutive patients. Radiology 2007;243(3):820-'
                    '827.',
        add_help=None,
        formatter_class=SmartFormatter,
        prog=os.path.basename(__file__).strip(".py"))

    mandatoryArguments = parser.add_argument_group("\nMANDATORY ARGUMENTS")
    mandatoryArguments.add_argument(
        '-di',
        type=float,
        required=True,
        help='Anteroposterior cord distance (in mm) at the level of maximum injury. Example: 6.85',
        metavar=Metavar.float,
    )
    mandatoryArguments.add_argument(
        '-da',
        type=float,
        required=True,
        help='Anteroposterior cord distance (in mm) at the nearest normal level above the level of injury.',
        metavar=Metavar.float,
    )
    mandatoryArguments.add_argument(
        '-db',
        type=float,
        required=True,
        help='Anteroposterior cord distance (in mm) at the nearest normal level below the level of injury.',
        metavar=Metavar.float,
    )

    optional = parser.add_argument_group("\nOPTIONAL ARGUMENTS")
    optional.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit")
    optional.add_argument(
        "-v",
        help="Verbose: 0: nothing, 1: classic, 2: expended.",
        required=False,
        type=int,
        default=1,
        choices=(0, 1, 2))

    return parser


def mscc(di, da, db):
    return (1 - float(di) / ((da + db) / float(2))) * 100


# MAIN
# ==========================================================================================
def main(argv=None):
    parser = get_parser()
    arguments = parser.parse_args(argv if argv else ['--help'])
    verbose = arguments.v
    set_global_loglevel(verbose=verbose)

    # Get parser info
    di = arguments.di
    da = arguments.da
    db = arguments.db

    # Compute MSCC
    MSCC = mscc(di, da, db)

    # Display results
    printv('\nMSCC = ' + str(MSCC) + '\n', verbose, 'info')


if __name__ == "__main__":
    init_sct()
    main(sys.argv[1:])

