import hashlib
import Crypto.Cipher as cipher

thing = input('> ')

#hashversion = hashlib.sha256(bytes(thing, 'utf-8')).hexdigest()
dehashed = cipher.decrypt(thing)
print(dehashed)


