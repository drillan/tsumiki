import os
import re
from collections import OrderedDict
from itertools import groupby

import markdown
from jinja2 import Environment, FileSystemLoader
from mdx_gfm import GithubFlavoredMarkdownExtension


def HTML(source):
    return source


def Markdown(source):
    md = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()])
    html = md.convert(source)
    return html


class Tsumiki:
    template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "template")
    env = Environment(loader=FileSystemLoader(template_dir, encoding="utf8"))
    article_tpl = env.get_template("article.tpl")
    column_style_tpl = env.get_template("column_style.tpl")
    columns_style_tpl = env.get_template("columns_style.tpl")
    columns_tpl = env.get_template("columns.tpl")

    def __init__(self, text):
        self.section = Section(text)
        self.section_dict = self.section.section_dict
        self.section_html_list = [
            self.render_to_html(x) for x in self.section_dict.values()
        ]
        article = "\n".join(self.section_html_list)
        self.html = self.article_tpl.render({"article": article})

    def is_section_header(self, n, line):
        return bool(self.section_pattern.match(line)) * n

    def make_section_data(self, lines):
        match = self.section_pattern.match(lines[0])
        meta = {}
        meta["directive"] = match.group(1)
        meta["column"] = len(match.group(2))
        source = "\n".join(lines[1:])
        return meta, source

    def set_section_dict(self):
        section_dict = OrderedDict()
        id_ = -1
        prev_id = 0
        prev_column = 0
        for x in self.section_data:
            meta, source = x
            column = meta["column"]
            if column == 1:
                id_ += 1
                section_dict[id_] = x
            elif (prev_id == 0 or column != prev_column) and column > 1:
                id_ += 1
                section_dict[id_] = [x]
            else:
                section_dict[id_].append(x)
            prev_id = id_
            prev_column = column
        self.section_dict = section_dict

    def _render_to_html(self, data):
        meta, source = data
        directive = meta["directive"]
        return eval(f"{directive}(source)")

    def render_to_html(self, data):
        column = data[0][0]["column"]
        if column == 1:
            html = self._render_to_html(data[0])
            source = f"<div>{html}</div>"
            style = self.column_style_tpl.render()
            return "\n".join((style, source))
        elif column > 1:
            html = [self._render_to_html(d) for d in data]
            style = self.columns_style_tpl.render({"column_count": column})
            source = self.columns_tpl.render(
                {"column_count": column, "sections": html}
            )
            return "\n".join((style, source))


class Section:
    section_pattern = re.compile(r"^:([A-Z]\w+)(:+)$")

    def __init__(self, text):
        section_list = [x for x in self.section_iterator(text.split("\n"))]
        section_meta_list = [self.convert_metadta_from_header(x) for x in section_list]
        section_id = [x for x in self.id_iterator(section_meta_list)]
        section_groupby = [
            list(section)
            for id_, section in groupby(
                zip(section_id, section_meta_list), key=lambda x: x[0]
            )
        ]
        self.section_dict = OrderedDict()
        for section in section_groupby:
            self.set_section_dict(section)

    def section_iterator(self, lines):
        section = []
        for line in lines:
            if self.section_pattern.match(line) and section:
                yield section
                section = [line]
            elif line:
                section.append(line)
        yield section

    def convert_metadta_from_header(self, line):
        header = self.section_pattern.match(line[0])
        meta = {}
        meta["directive"] = header.group(1)
        meta["column"] = len(header.group(2))
        return meta, "\n".join(line[1:])

    def id_iterator(self, sections):
        id_ = -1
        prev_column = 0
        for section in sections:
            column = section[0]["column"]
            if column > 1 and column == prev_column:
                yield id_
            elif column == 1 or column != prev_column:
                id_ += 1
                yield id_
            prev_column = column

    def set_section_dict(self, section):
        id_ = section[0][0]
        source = [x[1] for x in section]
        self.section_dict[id_] = source


def load_ipython_extension(ipython):
    from . magic import TsumikiMagic

    ipython.register_magics(TsumikiMagic)
