import qrcode
data=input("Enter data to encode in QR code(Text or link): ")
img = qrcode.make(data)

print("QR code generated and saved as qrcode.png")
img.show()