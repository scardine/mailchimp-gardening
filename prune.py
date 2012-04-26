#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        MaiChimp Prune
# Purpose:     Unsubscribe for large MailChimp lists
#
# Author:      PauloS
#
# Created:     23/04/2012
# Copyright:   (c) PauloS 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from mailsnake import MailSnake
import logging
import argparse
import sys

BATCH_SIZE = 50
FORMAT = '%(asctime)-15s %(message)s'
LOGLEVEL = logging.INFO

# COMMAND LINE OPTIONS
parser = argparse.ArgumentParser(description='Batch unsubscribe for large MailChimp lists')
parser.add_argument('-q', '--quiet', const=True, action='store_const', help='"quiet mode": supress messages')
parser.add_argument('-i', '--list-id', type=str, help='List ID (found under List->Settings->unique id)', required=True)
parser.add_argument('-f', '--logfile', type=str, help='Log file name (default: stderr)')
parser.add_argument('-l', '--loglevel', type=str, help='Log level (default: ERROR)')
parser.add_argument('-L', '--lists', type=str, help='Return list names and unique ids')
parser.add_argument('-k', '--key', type=str, help='API Key (found under Account->API Keys)', required=True)
parser.add_argument('file', type=str, help='File containing email list')
args = parser.parse_args()

# LOGGING
if args.logfile:
    logfile = open(args.logfile, 'w')
else:
    logfile = sys.stderr
if args.loglevel:
    level = getattr(logging, args.loglevel.upper(), None)
    if level in (logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG):
        raise ValueError('Invalid log level. Should be CRITICAL, ERROR, WARNING, INFO or DEBUG.')
else:
    level = LOGLEVEL
logging.basicConfig(file=logfile, level=level, format=FORMAT)

def coroutine(func):
    """When using coroutines, remembering to call .next() is easy to
    forget. This decorator solves this.

    Credit: copied verbatim from David Beazley presentation at
    PyCon'2009 in Chicago, Illinois)."""
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

def perform_unsubscribe(ms, batch):
    """Perform unsubscribe of a batch of emails.
    @ms: mailsnake instance
    @batch: list of email addresses
    """
    results = ms.listBatchUnsubscribe(id=args.list_id, emails=batch, send_goodbye=False)
    if results.get('error_count', 0):
        for error in results.get('errors', []):
            logging.error(str(error))
    return results

@coroutine
def batch_unsubscribe(ms):
    """This coroutine unsunscribes emails in BATCH_SIZE batches (default=50).
    @ms: mailsnake instance
    """
    batch = []
    batch_count = 0
    error_count = 0
    unsubscribe_count = 0
    try:
        while True:
            email = (yield)
            batch.append(email)
            if len(batch) == BATCH_SIZE:
                batch_count += 1
                results = perform_unsubscribe(ms, batch)
                unsubscribe_count += results.get('success_count', 0)
                error_count += results.get('error_count', 0)
                logging.info("Batch {batch}: {unsubs} email(s) unsubscribed, {errors} error(s) so far.".format(unsubs=unsubscribe_count, errors=error_count, batch=batch_count))
                batch = []
    except GeneratorExit:
        if batch:
            batch_count += 1
            results = perform_unsubscribe(ms, batch)
            unsubscribe_count += results.get('success_count', 0)
            error_count += results.get('error_count', 0)
            logging.info("Last batch: {unsubs} email(s) unsubscribed, {errors} error(s) total.".format(unsubs=unsubscribe_count, errors=error_count, batch=batch_count))

def main():
    ms = MailSnake(args.key)
    input_file = open(args.file, 'r')
    logging.info("Opening '{file}' for input.".format(file=args.file))
    unsubscriber = batch_unsubscribe(ms)
    for line in input_file:
        if ',' in line:
            email = line.split(',')[0] # CSV
        else:
            email = line.strip()       # Plain text
        if '@' not in email:
            continue # Header?
        unsubscriber.send(email)

if __name__ == '__main__':
    main()
