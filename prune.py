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

BATCH_SIZE = 50

parser = argparse.ArgumentParser(description='Batch unsubscribe for large MailChimp lists')
parser.add_argument('-q', '--quiet', const=True, action='store_const', help='"quiet mode": supress messages')
parser.add_argument('-i', '--list-id', type=str, help='List ID (found under List->Settings->unique id)', required=True)
parser.add_argument('-k', '--key', type=str, help='API Key (found under Account->API Keys)', required=True)
parser.add_argument('file', type=str, help='File containing email list')
args = parser.parse_args()

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
    results = ms.listBatchUnsubscribe(id=args.list, emails=batch, send_goodbye=False)
    return results

@coroutine
def batch_unsubscribe(ms):
    """This coroutine unsunscribes emails in BATCH_SIZE batches (default=50).
    @ms: mailsnake instance
    """
    batch = []
    batch_count = 0
    try:
        while True:
            email = (yield)
            batch.append(email)
            if len(batch) == BATCH_SIZE:
                batch_count += 1
                results = perform_unsubscribe(ms, batch, batch_count)
                batch = []
    except GeneratorExit:
        if batch:
            batch_count += 1
            perform_unsubscribe(ms, batch, batch_count)

def main():
    ms = MailSnake(args.key)
    input_file = open(args.file, 'r')
    if not args.quiet:
        print "Opening '{file}' for input.".format(file=args.file)
    unsubscriber = batch_unsubscribe(ms)
    for line in input_file:
        email = line.strip()
        unsubscriber.send(email)

if __name__ == '__main__':
    main()
