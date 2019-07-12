import datetime
import hashlib
import sys
import argparse
import time
########################
import printlogo

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print("Starting Shrack v0.0.1")
time.sleep(1)
print(" ")
printlogo.pl()
print(" ")
print(" ")
print(" ")
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 
print("Starting cracking at: " + st)
time.sleep(1)

parser = argparse.ArgumentParser(description='SHRACK: The hash cracker')
parser.add_argument('--type', help='Hash type', required=True)
parser.add_argument('--string', help='Hash string', required=True)
parser.add_argument('--wordlist', help='Wordlist', required=True)
parser.add_argument('--v',help="(true/false) Show more information while cracking", default=False, type=lambda x: (str(x).lower() == 'true'))
args = parser.parse_args()

supported_types = ('md5', 'sha256', 'sha1', 'sha224', 'sha384')
hash_string = args.string
hash_type = args.type
wordlist = args.wordlist
def encrypt(hash_type, hash_string):
    if hash_type == "md5":
        return (hashlib.md5(hash_string.encode()).hexdigest())
    if hash_type == "sha256":
        return (hashlib.sha256(hash_string.encode()).hexdigest())
    if hash_type == "sha1":
        return (hashlib.sha1(hash_string.encode()).hexdigest())
    if hash_type == "sha224":
        return (hashlib.sha224(hash_string.encode()).hexdigest())
    if hash_type == "sha384":
        return (hashlib.sha384(hash_string.encode()).hexdigest())

def summary(guess):
    print("HashString : " + hash_string)
    print("HashType   : " + hash_type)
    print("Result     : " + guess)

def crack_hash(hash_type, hash_string):
    if hash_type in supported_types:
        with open(wordlist, 'r') as wl:
            guesses = wl.read().split('\n')
            found = False
            result = "(none)"
            for guess in guesses:
                hashed_guess = encrypt(hash_type, guess) 
                if hashed_guess == hash_string:
                    print(bcolors.OKGREEN + "\nFOUND MATCH:\n" + bcolors.ENDC)
                    ets = time.time()
                    etstss = (ets-ts) - 1
                    print(hash_string + ":" + bcolors.BOLD + bcolors.OKGREEN + guess + bcolors.ENDC + " (cracked after " + str(guesses.index(guess)) + " guesses in " + str(etstss) + " seconds)")
                    found = (True)
                    result = guess
                    break
                else:
                    if args.v:
                        print(bcolors.FAIL + "Fail \"" + guess + "\"" + bcolors.ENDC + " (" + str(guesses.index(guess) + 1) + "/" + str(guesses.__len__()) + ")")
            print("End of the list.")
            if found:
                if args.v:
                    print('\nMD5 OF THE RESULT:')
                    print(encrypt('md5', result))
                    print('\nSHA1 OF THE RESULT:')
                    print(encrypt('sha1', result))
                    print('\nSHA224 OF THE RESULT:')
                    print(encrypt('sha224', result))
                    print('\nSHA384 OF THE RESULT:')
                    print(encrypt('sha384', result))
            print("\n\nSummary:\n\n")
            summary(result)              
    else: 
        print("hash type \"" + hash_type + "\" is not supported.")
        print("")
        print("Supported types:")
        for hashtype in supported_types:
            print("  " + hashtype)

crack_hash(hash_type, hash_string)