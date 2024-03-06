from hashlib import sha256

susan = "susan_nasus_"
hash = "abeb6f8eb5722b8ca3b45f6f72a0cf17c7028d62a15a30199347d9d74f39023f"

for i in range(0, 1000000000, 10):
    if hash == sha256((susan + str(i)).encode('utf-8')).hexdigest():
        print("[V] - test: " + susan + str(i) + " | succeed !")
        break
    else:
        print("[X] - test: " + susan + str(i) + " | failed")