# Demo of SHA256 function iteratin over 20 values
# IMPORTANT: the encode function is necessary to avoid a runtime error


import hashlib

text = "I am Satoshi Nakamoto"

for nonce in range(20):
    input = text + str(nonce)
    hash = hashlib.sha256(input.encode('utf-8')).hexdigest()
    print(input + ' => ' + hash)