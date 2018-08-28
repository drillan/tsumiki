from IPython import display
from IPython.core.magic import Magics, cell_magic, magics_class
from . import Tsumiki


@magics_class
class TsumikiMagic(Magics):
    @cell_magic
    def tsumiki(self, line=None, cell=None):
        tsumiki = Tsumiki(cell)
        return display.HTML(tsumiki.html)
