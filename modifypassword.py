import argparse
import hashlib

HASH_OFFSET = 0x1d3eb
HASH_LENGTH = 20

# Parse all CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--binary', help = 'path to the program binary to patch', required=True)
parser.add_argument('-p', '--password', help = 'new password that the program should accept', required=True)
parser.add_argument('-d', '--dest', help = 'file where the patched executable should be saved', default='./patched.exe')
args = parser.parse_args()

# Generate SHA1 hash of new password
hash = hashlib.sha1(args.password.encode())
digest = hash.hexdigest()

# Read in the current (unmodified) binary
with open(args.binary, 'rb') as file:
    bin = file.read()

# Replace the hash in the current binary with the hash of the new password
bin = bin[:HASH_OFFSET] + bytes.fromhex(digest) + bin[HASH_OFFSET+HASH_LENGTH:]

# Write the patched binary
with open(args.dest, 'wb') as file:
    file.write(bin)

print(f'Succesfully wrote patched program binary to {args.dest}')