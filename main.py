#!/usr/bin/env python3
# python >= 3.7

import logging
import argparse
from verify import Verification

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-logl", 
        "--log_level", 
        default="warning",
        help=(
            "Provide logging level. "
            "Example -logl debug, default='warning'"
        ),
    )
    parser.add_argument(
        "-logf", 
        "--log_file", 
        default=None,
        help=(
            "Provide log file. "
            "Example -logf debug.txt, default=None"
        ),
    )
    parser.add_argument(
        "-pol", 
        "--policy", 
        default=[],
        nargs='+',
        help=(
            "Provide the policies to verify. "
            "This overrides --exclude_policy if both specified. "
            "Example -pol StaticPolicy, default=None(use all policies)"
        ),
    )
    parser.add_argument(
        "-expol", 
        "--exclude_policy", 
        default=[],
        nargs='+',
        help=(
            "Provide the excluded policies. "
            "Example -expol StaticPolicy, default=None"
        ),
    )
    parser.add_argument(
        "-prog", 
        "--program", 
        default=[],
        nargs='+',
        help=(
            "Provide the programs to verify. "
            "This overrides --exclude_program if both specified. "
            "Example -prog Revocation, default=None(use all policies)"
        ),
    )
    parser.add_argument(
        "-exprog", 
        "--exclude_program", 
        default=[],
        nargs='+',
        help=(
            "Provide the excluded programs. "
            "Example -exprog Revocation, default=None"
        ),
    )
    parser.add_argument(
        "-rep", 
        "--report", 
        default=['x', '-', 'n'],
        nargs='+',
        help=(
            "Provide the type of result to report: 'X' for failed, '-' for passed, and 'N' for not applicable. "
            "Example -exprog Revocation, default=All"
        ),
    )


    options = parser.parse_args()
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    level = levels.get(options.log_level.lower())
    if level is None:
        raise ValueError(
            f"log level given: {options.log}"
            f" -- must be one of: {' | '.join(levels.keys())}")
    file = options.log_file
    logging.basicConfig(filename=file, filemode='w', format='[%(levelname)s]: %(message)s', level=level)
    v = Verification(programs=options.program, policies=options.policy, ex_programs=options.exclude_program, ex_policies=options.exclude_policy, reports=options.report)
    v.run() 
    v.print_stats()