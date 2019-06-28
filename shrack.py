import hashlib
import sys
import argparse
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
print(" ")
printlogo.pl()

parser = argparse.ArgumentParser(description='SHRACK: The hash cracker')
parser.add_argument('--type', help='Hash type', required=True)
parser.add_argument('--string', help='Hash string', required=True)
parser.add_argument('--wordlist', help='Wordlist', required=True)
parser.add_argument('--v',help="(true/false) Show more information while cracking", default=False, type=lambda x: (str(x).lower() == 'true'))
args = parser.parse_args()

supported_types = ('md5', 'sha256', 'sha1', 'sha224')
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

def crack_hash(hash_type, hash_string):
    if hash_type in supported_types:
        with open(wordlist, 'r') as wl:
            guesses = wl.read().split('\n')
            for guess in guesses:
                hashed_guess = encrypt(hash_type, guess) 
                if hashed_guess == hash_string:
                    print(bcolors.OKGREEN + "\nFOUND MATCH\n" + bcolors.ENDC)
                    print(hash_string + ":" + guess + " (cracked after " + str(guesses.index(guess)) + " guesses)")
                    break
                else:
                    if args.v:
                        print(bcolors.FAIL + "Fail \"" + guess + "\"" + bcolors.ENDC + " (" + str(guesses.index(guess) + 1) + "/" + str(guesses.__len__()) + ")")

    else: 
        print("hash type \"" + hash_type + "\" is not supported.")
        print("")
        print("Supported types:")
        for hashtype in supported_types:
            print("  " + hashtype)

crack_hash(hash_type, hash_string)