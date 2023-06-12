import base64
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import Salsa20
from Crypto.PublicKey import RSA
private_key_pem='''-----BEGIN RSA PRIVATE KEY-----
MIGqAgEAAiEAxLsPt3Ywql0RgiLytt+PRWR4JfpM+NK5R4UUi/eHUn0CAwEAAQIg
fUNieX1+9Sr3V/ZqtvhYH0blpZBTR/vQ/Jt6sJxhrj0CEQD4Dos9a4R60c7GQ8QM
O4xTAhEAywfFBOkb3DhgBnsQjIFL7wIQPI9Qby5QqauPT9g7hMEFAQIQI7zqYULn
NIx32qwu7YyU4QIRAIIeDM2UcI8VzS5PELS+wzE=
-----END RSA PRIVATE KEY-----
'''

private_key = RSA.importKey(private_key_pem)
print("private key components:")
print("modulus:", private_key.n)
print("decryption key:", private_key.d, "\n")

x = bytes_to_long(base64.b64decode("p3pCyMhV+P19R/my0cSe86fo1Jg1MET30Uq5b7bhidE="))

salsa_key = long_to_bytes(pow(x,private_key.d,private_key.n))

msgs = ['{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"qTKiNKohZbA=","Msg":"XUuNmKaWp7KMWJsOBhg99QYmVFw="}',
'{"Nonce":"5Cm8cDK8rkU=","Msg":"Vmxolx8UtloxfVYIai4k9Ig8Iv26Cl3cj7uWH5Y1yhzJd3Os"}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"Hoeu+KZMx0c=","Msg":"jshDkQSeAa7PRTBouVsnSMQaEidvUUXD8/Y5SMSQG2y6zT1Yd9s="}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"OSl59/tcdZ4=","Msg":"O3q2wrQRqzdw7eGQXQ71c7loQY0="}',
'{"Nonce":"QxINfAqWnDo=","Msg":"scjIXivMqxZiKzgiBnDeST4KyV7Y78bznPNxxdJ992eFFbckrVzA6ZFL"}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"nrpfzC0NzVc=","Msg":"pecSTPgY6L8glMJQnFezVB17QgAOEjHHwsMuBxmKKHsDFrD6bMTAo6ZU/OPJsD5639lfpWJL4u0twDyXvqUrtPBkLjeYMleUEhGtgVgj2X0="}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"Ngysxj8cCA8=","Msg":"EpSg5qLLgiLm6lBy6E5QjyXaDt8="}',
'{"Nonce":"tghorstI878=","Msg":"Br+uz9CQfekqh91dpoVb3toir1NuE/6AJflpc0gFf5WcnbZgGcJZOonh+z+v+14p9w=="}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"FdaywZ2O2p4=","Msg":"fOFdQycwdE+3D5sH5gldZyP9azYsxJnh/0GgQK5rtqpW76rlhN4pcCUeKuH5MP0JilMEbLBbK1Wn9kPjO6QZ+m7zMvjPJWt3kZhWmsu+9t2c80v9HtuenbN7BKJGV5qFVa07rqxe/gD0jxOG3eY3oBINO7FDF43DoKfn/nqRqPpRrhLeKRMhgdffiXeGwDEEiE6l9eMcqz2bdQT8KIjUG896BmMOIEPRsTNwRt8NlgAQd75mlw80DdSjGVnu+HZ9Y+AxvVR81e0QPSZLjB2lz7ECvndg0r7cQhJ7S3IMlHgNnsIj8xXkF5psyE2DFobezaxYLfLvAAgnVS5v8bVZBLUTuFa2gSB2CqFzEQBVM5lsqooj0LOxYFhLvtyfSMvX4RhGyVTD0CI+qukUZpV3tSryGz3XZMVFtjq1PuDkxxGDG7zFdRQJ79fcAzcW40WHDw+mzYn4uCkyN7Mufe7UVhL3DpnC0tQQ0qPqRX2dlbuopPTuTyD7nhNHlmy+xnCSm01lJKD2qsOmNq+q+Hxtj9yFIJUgZ69cLjVCtOeiyxpJE1AaI6wX4BV9a5VpfmzjVGb/6xuDyRozGnr5rfQ="}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"NwnrStALBZo=","Msg":"N0AjrHSUlr4EFPKaUzIaoPP+nO4="}',
'{"Nonce":"zvBjL+laOhU=","Msg":"Kk5ihQTvdY7i1d59pKGSg4Z/lguP40XImq3xrH2j4mxVexZPJdY="}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"7VTkaI/asBg=","Msg":"8p7h+51fbsc0PGlZyEwXwmr1H3VH6M64lbyc7MXqj3APKojQS22BmxE2ifKfIKdNG4qdOhwBk8DvWzVgVR8/Ej2S4RVFXe+tQGES8QoMNHBtaUMXcldcIXSatCtxwMssNIyOI3C1O0fBmJ8hA7sFSZaJopWdhQ+1KrI3OCM4vr0w6pXZcc17QTZzc0+riM375UCqhVvIQ/GBhn3tEN2s3sXVNTpq0UWPU+jbn8vuRJln+2aRtKXUCPd/lAvM/n46X77C38BceQEkRrLlhCF8kgTraQOxPGVLT5zn9OnJW81Jhi+aJiosFvjXeJFOTSsv5sUAsphzlAxEzLG3cKip1gDrMAX8IBY50M7mhjEdAXgHSCqIwQWk3Gpe8PzMhjlgQ7nibSS8c0sSh9xVQhAbMOGG5Mpwtfz4STV8XpsHW7+LkABRnWha0rQ28z4OmOLDNy72iCYVRNEs2H36CR80tyMnepvO5tk+P5pBxeSNzbxlCDwWDiyL8RxQfenMFe3zn+rTba/uRcnoPfcNzYSy4XfLdWwwXMNbizh07GSicim/FZek6no+peI/Ml2AsSsHilGF3tpIk1L4+qfwJmDMk0PreT8qBHznrPAtqpZ8N0a/aVTeov/cLBGmzOwvJH98nkc8W4yfQVyRoj7h7eQi8dud7NfVuTrued2VSXTfjcrdfiYwVCEgBhMalH49r8uJSlrNh6RNlWTvPtXNqc0atsrz7rAzdXy1s7ywUDKl0kiMWjtHHfC8AV9fj+4824ySHvSZ3EJ+u8kQS1rtpq5yqBWwdD0lhXRafsbqWSL5sMkmGYyc5X8RWdcKTc72rvQu1u07wi1xXwcUrGKwSwEqxf78VuWaYq51w+yIouadeJm+yVs68vEPNYytuESkFE4TFGSLxeGHcagcspOcTydfRdQAZ5DAcClNOnmPmBQ4FLvS4m17eIIzD7qaShXBEg9++RmzySou3yVn98KxvxKyDrPFtJLrLbqK5ernLgDaKwCnyxOLzHzGzciEDQD2N4Dd5u+uc0cM8iEnfrJSoe5y69kRE3KWf2oi2c+8k5OqsDwthJqiDjDDygyyL7QAxBM7D+6S6uAqWnWER0qCiu25uNJsigELvXN4QnGated25nyMPCTPZuaBUm1VZ1aO0VLIUtIPajr3hgUaXn09/VbHqIavzUmLoP2C4LavRHm5DxmqvPqsg708tEXSAS0VoRQwE4DfcbCm/rmZSSewFwzL2lN5EgkcbmCdcLcPObjB+sa2P/kht+1rMGGebWZa+Dqw32/Bk+oroNO+SfoKQq+cOP8Jzqqzj2PctF9NYwTSG5BdrVbTmOlAYmRxiVBI/d4uPqChHQhrBo1nyUUHLpDRyeYleyGwBPhjaZu4ky/LaJgDgF5oP4wA0eyVmpGLtioFKjuaEYYkEBLfy3xczMCMbZXwz216HrYTN+WG6+xXbuJZThjkELqB7lHQJTil05fLq3BLxMmYwFEV2yTzqnwkHJVDTkSNzMWkgVjMohC2uEYjOuZXmj2hEy8mhhoQz+3ZyVNsL4noPpq1iWfAd2eoZuWdX0DG06m3/CIhhkVGeaUjb4+UvdgKeymgidseki4+e2Zd0fIJY8OJbWC8BJNMGhpKsZUeXnxuAFcKlBUOE1mPnZvp/34627pPz4D55dKgZuSiCMR8B5ajVbJrdSXVX+mjvN4ZjO8ILgIIjAPQzmVKtstD9bIGLDUg64eD36kp6oF7FAcYnvTDQvX0u5vjW8cU6BCxKPSqLLjtawwrVW8IYFofiloEAB1iWONF07cJF2CzJDH+It782OLMpaToVDrOoaH+SN+D2WebKov5WzogdzoaQsTcOHkiQ5yPWnLWKUt+BkjsQ6Ta3m/K0tHBH9WnudDqGaoN8Q=="}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"8QySSqRLWHo=","Msg":"NMiV2Et6nyCF6fKQtFkhRDjE1VY="}',
'{"Nonce":"0jaHO3mjUz4=","Msg":"T5tUtuZExzvjzXDrgg+EVj/bPsy2Q7Xapy/xRk4QnPSJ8fk5o0PVt575SA=="}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"LQUtOwKasqM=","Msg":"vCyXKZKcjkDVhZa+dkbmg0Pcn4w0KLIoSo4nalGs+Ig41V0e/wAaPdFM7q6dGWY9aKKs6R1+cw=="}',
'{"ClientId":"1d10cce9-d8a4-4401-a585-69d73724fada","Nonce":"QIG/OhHBybA=","Msg":"1LM/ZHxn7vs9qTFqy76H4DyiAFE="}',
'{"Nonce":"VOoO8TX8Srg=","Msg":"QKQ0dkvDMHgVWBFDyLKct6Jw73+aLawdD4JyOTvN8A=="}']

for m in msgs:

    J = json.loads(m)

    nonce = base64.b64decode(J["Nonce"])
    msg = base64.b64decode(J["Msg"])

    cipher = Salsa20.new(key=salsa_key, nonce=nonce)
    plaintext = cipher.decrypt(msg)

    J2 = json.loads(plaintext)
    
    if "Command" in J2:
        print("\nCommand: %s" % J2["Command"])
    elif "Output" in J2:
        print(J2["Output"])