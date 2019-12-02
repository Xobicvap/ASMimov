import binascii

class FileReader:

  def __init__(self, filename, filepath='./'):
    self.filename = filepath + filename
    print("READING: " + self.filename)

  def _read(self):
    binarr = []
    keep_looping = True
    with open(self.filename, "rb") as filebuf:
      while keep_looping:
        byte = filebuf.read(1)
        if byte == b"":
          keep_looping = False
        else:
          binarr.append(byte)
    return binarr

  def read_file(self):
    binarr = self._read()
    bytearr = []
    for byte in binarr:
      strbyte = bytes.hex(byte)
      strbyte = "0x" + strbyte
      intbyte = int(strbyte, 16)
      bytearr.append(intbyte)
    return bytearr
    #return [int("0x" + binascii.hexlify(b), 16) for b in binarr]



