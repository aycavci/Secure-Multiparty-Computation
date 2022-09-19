from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKeyWithSerialization, \
    RSAPublicKeyWithSerialization


class RingMPC:
    MAX_SIZE = 2048

    def __init__(self):
        self.public_keys = []

        # TODO fetch all public keys properly
        for i in range(3):
            with open('pub{}.pem'.format(i), 'rb') as key_file:
                self.public_keys.append(
                    serialization.load_pem_public_key(
                        key_file.read(),
                    )
                )

    def enc(self, message: bytes, frm: int, to: int):
        len_diff = (to - frm + len(self.public_keys)) % len(self.public_keys)
        cipher_text = message
        for i in range(len_diff):
            print(len(cipher_text))
            cipher_text = self.public_keys[(frm + i + 1) % len(self.public_keys)].encrypt(
                cipher_text,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                )
            )
        return cipher_text

    def dec(self, cipher_text: bytes, private_key: RSAPrivateKeyWithSerialization):
        message = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            )
        )
        return message

    def sign(self, cipher_text: bytes, private_key: RSAPrivateKeyWithSerialization):
        signature = private_key.sign(
            cipher_text,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return signature

    def verify(self, signature: bytes, cipher_text: bytes,
               public_key: RSAPublicKeyWithSerialization):
        public_key.verify(
            signature,
            cipher_text,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
