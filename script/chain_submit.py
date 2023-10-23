#!/usr/bin/env python3
"""Submit several jobs that depend on each other in a chain.

Call as   chain_submit.py path/to/runfile.1 [path/to/runfile.2 [...]]

Will cd into the directory, submit the runfile and then do the same
for the next, using the returned job id as dependency.

"""

# It will work with python2, too, for now. Sadly clusters still have that.
from __future__ import print_function

import os
import sys
import subprocess
import optparse
import re


# Choose a profile from below.
PROFILE="lichtenberg_slurm"

# Entries in the profile tuples:
#
# 1) The command to submit a job on this machine which does not depend
#    on another job. All commands are given as lists, where the first
#    entry is the binary (e.g. qsub) and the following entries are the
#    arguments. The string {runfile} in any entry will be replaced by
#    the name of your submission script.
#
# 2) The command to submit a job that depends on another job. Same as
#    1, except that {jobid} will also be replaced by the id of the job
#    that the new job should depend on.
#
# 3) re.compile(r'...'), replace the ellipsis with the regular expression
#    to extract the job ID from the output of the submission command. The
#    regex should contain exactly one group (parentheses) that will be
#    extracted by the code later. This is the ID. For example if the output
#    looks like
#
#               12345.quismas.foobar
#
#    and the number part is the ID, then you can use something like
#    re.compile(r'(\d+)') or re.compile(r'(\d+)\.quismas\.foobar')
#
# 4) Should be either "arg" or "stdin". This tells this script if the
#    submission command wants the submission script as an argument
#    (qsub run.sh) or via stdin (bsub < run.sh).
PROFILES = {
    "juropa": (["/usr/bin/msub", "{runfile}"],
               ["/usr/bin/msub", "-W depend=afterok:{jobid}", "{runfile}"],
               re.compile(r'(\d+)'),
               "arg"),
    "quismas": (["/opt/torque/bin/qsub", "{runfile}"],
                ["/opt/torque/bin/qsub", "-W", "depend=afterok:{jobid}",
                 "{runfile}"],
                re.compile(r'(\d+)'),
                "arg"),
    "lichtenberg": (["bsub"],
                    ["bsub", "-w", "done({jobid})"],
                    re.compile(r'Job <(\d+)> is submitted'),
                    "stdin"),
    "lichtenberg_slurm": (["sbatch", "{runfile}"],
                          ["sbatch", "-d", "afterok:{jobid}", "{runfile}"],
                          re.compile(r'Submitted batch job (\d+)'),
                          "arg"),
    # On dabasco depend=afterok doesn't work.
    "dabasco": (["qsub", "{runfile}"],
                ["qsub", "-W", "depend=afterok:{jobid}", "{runfile}"],
                re.compile(r'(\d+)'),
                "arg"),
    }


SUBMIT_FIRST, SUBMIT_FOLLOW, CRE, SUBMIT_KIND = PROFILES[PROFILE]


parser = optparse.OptionParser()
parser.add_option("-i", dest="jobid", default=None,
                  help="Let first job depend on this job id.")
parser.add_option("-p", dest="parallel", action="store_true", default=False,
                  help="Disable dependency handling for the jobs and just "
                       "submit in parallel. Together with -i all jobs will "
                       "depend on a single job id.")
(options, args) = parser.parse_args()

if not args:
    print("Usage:  chain_submit.py path/to/runfile.1 [path/to/runfile.2 [...]]")
    sys.exit(1)

basedir = os.path.abspath(os.path.curdir)
jobid = options.jobid
jobids = []
for i, job in enumerate(args):
    jobpath, runfile = os.path.split(job)
    if jobpath:
        os.chdir(jobpath)

    # Prepare command.
    if (i == 0 or options.parallel) and jobid is None:
        proc = subprocess.Popen([s.format(runfile=runfile)
                                 for s in SUBMIT_FIRST],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
    else:
        proc = subprocess.Popen([s.format(runfile=runfile,
                                          jobid=jobid)
                                 for s in SUBMIT_FOLLOW],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)

    # Prepare stdin
    if SUBMIT_KIND == "stdin":
        with open(runfile) as f:
            stdin = f.read()
    else:
        stdin = ""

    # Execute.
    stdout, _ = proc.communicate(stdin)

    m = CRE.search(stdout)
    try:
        jobid_ = int(m.group(1))
    except (ValueError, IndexError, AttributeError):
        print("Unknown string returned from submission command:")
        print()
        print(stdout)
    jobids.append(jobid_)
    if not options.parallel:
        # If the -p option was specified, we retain a possible jobid
        # provided by the -i option (or None).
        jobid = jobid_

    print("Submitted", jobid_)

    os.chdir(basedir)
