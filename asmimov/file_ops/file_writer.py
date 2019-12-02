from os import linesep

class FileWriter:

  def __init__(self, filename, filepath="./"):
    self.filename = filepath + filename

  def _add_newlines(self, lines):
    return [x + linesep for x in lines]

  def write(self, lines):
    lines_with_newlines = self._add_newlines(lines)
    with open(self.filename, "w+") as filebuf:
      filebuf.writelines(lines_with_newlines)

