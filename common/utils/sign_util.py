import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from common.utils.decorator import Decorator


@Decorator.const_single
class SignUtil:

    __default_private_key_bytes = (b'-----BEGIN RSA PRIVATE KEY-----\n'
                                   b'MIIEpAIBAAKCAQEAtL7aQIEnpQJTmUY+hib5wVjEKkGdOSwmEEu7OepL2pMTbYM2\n'
                                   b'1j9e1pBOSzmQ6KwaNU+eIajogIiRawPsq/MSLEh4yOA9vstK2jOdndDb1VWXYFIq\n'
                                   b'UWkaBzXl8CjH3e32xIMtErPqhmQHdh1ng/YGzClNauM1MpIKFe/3q6j+16ButY8u\n'
                                   b'j6Zke4iCitsubQ7Z5KumYDQqEV2QF2ehlw78GE4rbiP+KuVycX74crF35Yrmp6D/\n'
                                   b'b2zy37EaqUxVep7BUOkRHTzl9ouYuitDN2rcyj9/6yoChPg/uvg8i1ibKUnmRqGp\n'
                                   b'FugkYqFYo2xRZwr6McI1ZDrOhmeNawwNIQhPpwIDAQABAoIBAA2KAFT1om/GBAIc\n'
                                   b'FMHoIyxHBxwNNzGZq4OWpgCEGvOABzlcVga9eiVYwOyknsS3DkLbuGzYDLaCxGB/\n'
                                   b'oO0Oc62Kg4sJ38YuJJNswLaaIbrSGFlC6QrudGCBj+b/VF1nnmUBAybUAFIvJa9E\n'
                                   b'1kS4cLDpZR8HxFaJ7E8mtGbmQqoJ07Z7GvYZRepboRrbT+ZgUs7s/3I+QmJvUZbQ\n'
                                   b'05E8Ixknx1tlxWeEBAih7wyHFHTTvTj+EVM5AgStQlYWi+d9zvhUTx8FXZ+idPec\n'
                                   b'FIrxsHOEgq66zyBQMYbwWT5gOXaeIC09MDSdqWaKCfHHDyJ6W1GiMIJNbD4uNgDM\n'
                                   b'MXLLvR0CgYEA4rjmSBTfgA3jG5GDUqMV2FNDCiQ5SaZsl5CTeQJ/VApw//p4kKGP\n'
                                   b'RkU/27w9x8LTxuq0zMmwmZ8ZuPAwUxh4Q7//ai9Pkj5OBzAIhnJGS/R+A8Edt3g2\n'
                                   b'yhlEzphgmWFbQVDCuPt/Qw1GQhKVFCg4aBqLT+9iQfhEcJ9RrfFl8CMCgYEAzBYH\n'
                                   b'vfEYgIz1T7DhTjmkrJtjOD8fylCEn/BPUbrla+VIR5xj2T2UUieJnwokRLnCM+O4\n'
                                   b'9sIn82hZEKIcH2j86edXT9N9MarehBc+chx4BjvjbCjtYtBeqn5TTcD4Rq0FAA9p\n'
                                   b'pxow7xb/23LvIJaoEFTKlC9qTqRqSLZNd3YTWK0CgYEAoJhEVg6i+fvcQOzjzqdC\n'
                                   b'lAb2V7qs8aR3Cy0XqQHB22/B9zAeMqSd7jKjNyyxvkwc4qviAaVj+I0gFUXdlR6i\n'
                                   b'IatgaoC0pmyHrMOzZjiP3sGCeXpTaGA4vxMDECwTUNILZ8qjA5Dx5jcC605qVure\n'
                                   b'ea9Duw1f1kbbg8L2gnWZtW0CgYEAos/0bzB25p8NWPz4UUqlN9pjBk09lE41785r\n'
                                   b'yPz7596rkg2OjpGU0RGftdQGaRl0d6b1OU5dRs75Ns7M9rXwBr47JoDHAKebCu/s\n'
                                   b'LmbNzdNbND9WWh13WDadSItoxiFjus+Q7vFzFlpX1X9Ui8AE5bpvPlaxTXnXHJjr\n'
                                   b'JiF5f6UCgYBkcxPb6Zp4YClsn7xCx7HY4TweP5oYwWuLcdWc6OU7cENPZ6TvGlH6\n'
                                   b'ev66kXscmsgM4KcC+PMcQRINdhGWWggqMauSyjoypjiKRK4N014CmW3zxv7knQIn\n'
                                   b'Gkik7G8MOiqa/GpuDWGbPPy4qtmcuEymsj26UNINSvCX+NgUGUjYtQ==\n'
                                   b'-----END RSA PRIVATE KEY-----\n')

    @property
    def default_private_key_bytes(self):
        return self.__default_private_key_bytes

    @property
    def default_private_key_str(self):
        return self.__default_private_key_bytes.decode("UTF-8")

    @property
    def default_private_key(self) -> RSAPrivateKey:
        return serialization.load_pem_private_key(self.default_private_key_bytes,
                                                  password=None,
                                                  backend=default_backend())

    @property
    def default_public_key(self) -> RSAPublicKey:
        return self.default_private_key.public_key()

    @property
    def default_public_key_bytes(self):
        return self.default_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @property
    def default_public_key_str(self):
        return self.default_public_key_bytes.decode("UTF-8")

    @staticmethod
    def encode_to_base64(data: bytes):
        return base64.b64encode(data)
