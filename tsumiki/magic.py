from IPython import display
from IPython.core import magic_arguments
from IPython.core.magic import Magics, cell_magic, magics_class
from . import Tsumiki


@magics_class
class TsumikiMagic(Magics):
    @magic_arguments.magic_arguments()
    @cell_magic
    def tsumiki(self, line=None, cell=None):
        """
        Write with mixed markup langueges.

        Parameters
        ----------
        -r : render to jinja2 template.

        Examples
        --------

        %%tsumiki

        :Markdown:
        # Title
        * list1
        * list2

        :Markdown::
        ## Sub Title1
        * list3
        * list4

        :HTML::
        <h2>Sub Title2</h2>
        <ul>
          <li>list5</li>
          <li>list6</li>
        </ul>
        """
        
        opts, args = self.parse_options(line, "r", mode="list")
        if "r" in opts:
            import jinja2
            from jinja2schema import infer

            user_ns = self.shell.user_ns
            template_params = {}
            for x in infer(cell).keys():
                if x in user_ns:
                    template_params[x] = user_ns[x]

            template = jinja2.Template(cell)
            text = template.render(**template_params)
        else:
            text = cell

        tsumiki = Tsumiki(text)
        return display.HTML(tsumiki.html)
