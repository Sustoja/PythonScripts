import hashlib
import time

max_nonce = 2 ** 32


def proof_of_work(header, difficulty_bits):
    target = 2 ** (256 - difficulty_bits)

    for nonce in range(max_nonce):
        block = str(header) + str(nonce)
        hash_result = hashlib.sha256(block.encode('utf-8')).hexdigest()

        if int(hash_result, 16) < target:
            print("Success with nonce %d" % nonce)
            print("Hash is %s" % hash_result)
            return (hash_result, nonce)

    print("Failed after %d (max_nonce) tries" % nonce)
    return nonce


if __name__ == '__main__':
    nonce = 0
    hash_result = ''

    for difficulty_bits in range(24):
        # difficulty = 2 ** difficulty_bits
        print("Difficulty: %d bits" % difficulty_bits)
        print("Starting search...")

        start_time = time.time()
        new_block = 'test block with transactions' + hash_result
        (hash_result, nonce) = proof_of_work(new_block, difficulty_bits)
        end_time = time.time()

        elapsed_time = end_time - start_time
        print("Elapsed time: %.4f seconds" % elapsed_time)

        if elapsed_time > 0:
            hash_power = float(int(nonce) / elapsed_time)
            print("Hashing power: %ld hashes per second\n" % hash_power)
