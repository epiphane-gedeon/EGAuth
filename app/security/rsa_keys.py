from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pathlib import Path
 
def generate_rsa_keys(key_size: int = 2048) -> tuple[bytes, bytes]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem
 
def load_or_create_keys(private_path: str, public_path: str):
    priv, pub = Path(private_path), Path(public_path)
    if not priv.exists():
        priv.parent.mkdir(parents=True, exist_ok=True)
        private_pem, public_pem = generate_rsa_keys()
        priv.write_bytes(private_pem)
        pub.write_bytes(public_pem)
    return priv.read_bytes(), pub.read_bytes()
 
if __name__ == '__main__':
    load_or_create_keys('keys/private.pem', 'keys/public.pem')
    print('Clés RSA générées dans ./keys/')
