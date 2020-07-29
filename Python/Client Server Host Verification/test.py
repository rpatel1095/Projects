import hmac
c1="arianna"
c2="grande"
d1=hmac.new("k3521".encode(),c1.encode("utf-8"))
d2=hmac.new("k3522".encode(),c1.encode("utf-8"))
d3=hmac.new("k3521".encode(),c1.encode("utf-8"))
d4=hmac.new("k3521".encode(),c2.encode("utf-8"))
print(d1.hexdigest())
print(d2.hexdigest())
print(d3.hexdigest())
print(d4.hexdigest())
print(d1.hexdigest()==d2.hexdigest())
print(d1.hexdigest()==d3.hexdigest())
print(d1.hexdigest()==d4.hexdigest())
exit()