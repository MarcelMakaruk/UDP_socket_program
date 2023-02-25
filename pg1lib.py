import zlib
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


# generate private key and store it as a global variable
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

def getPubKey():
    """
    Generate and return an encryption key
    
    Returns:
        bytes: this host's encryption key
    """
    public_key = private_key.public_key()
    public_key_str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_str_b64 = base64.b64encode(public_key_str)

    return public_key_str_b64

def encrypt(message, pubkey):
    """
    Encrypt a message with peer's encryption key

    Args:
        message (bytes): plaintext message to encrypt
        pubkey (bytes): peer's encryption key (formatted as output to getPubKey())

    Returns:
        bytes: base64 encoded ciphertext
    """
    # pubkey = pubkey.decode()
    public_key_str = base64.b64decode(pubkey)
    public_key = serialization.load_pem_public_key(
        public_key_str,
        backend=default_backend()
    )

    key = Fernet.generate_key()
    encrypted_key = public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    encrypted_key_b64 = base64.b64encode(encrypted_key)
    
    f = Fernet(key)
    encrypted_msg = f.encrypt(message) 
    encrypted_msg_b64 = base64.b64encode(encrypted_msg)

    return encrypted_key_b64 + b';' + encrypted_msg_b64


def decrypt(cipher):
    """
    Decrypt a message with this host's private key

    Args:
        cipher (bytes): plaintext message to encrypt
        
    Returns:
        bytes: decrypted plaintext message
    """
    cipher = cipher.split(b';')
    cipher_key = base64.b64decode(cipher[0])
    cipher_msg = base64.b64decode(cipher[1])
    
    decrypted_key = private_key.decrypt(
        cipher_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    f = Fernet(decrypted_key)
    decrypted_msg = f.decrypt(cipher_msg)
    
    return decrypted_msg


def checksum(data):
    """
    Calculate the checksum for the input data

    Args: 
        data (bytes): the data to process

    Return: 
        int: the checksum 
    """
    crc = zlib.crc32(data)
    return crc
