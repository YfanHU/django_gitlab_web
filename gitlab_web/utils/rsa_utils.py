import rsa

def rsa_new_keys():
    (pubkey,privkey) = rsa.newkeys(256)
    return pubkey.save_pkcs1().decode(encoding = 'utf-8'),privkey.save_pkcs1().decode(encoding = 'utf-8')

def rsa_encrypt(pubkey,text):
    pub = rsa.PublicKey.load_pkcs1(pubkey.encode())
    return rsa.encrypt(text.encode(),pub)

def rsa_decrypt(privkey,crypto):
    priv = rsa.PrivateKey.load_pkcs1(privkey.encode())
    return rsa.decrypt(crypto,priv).decode()

if __name__=='__main__':
    pub,priv = rsa_new_keys()
    rsa_encrypt(pub,'12345678')