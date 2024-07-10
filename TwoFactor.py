import time
import pyotp
import qrcode

def otp_gen(email):
    key = pyotp.random_base32()
    uri = pyotp.totp.TOTP(key).provisioning_uri( name = email, issuer_name= 'Loopy')
    print(uri)
    qrcode.make(uri).save("qr.png")
    totp = pyotp.TOTP(key)
    return totp

def verify_otp(totp, otp_input):
    return totp.verify(otp_input)



