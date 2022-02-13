# AUTOGENERATED! DO NOT EDIT! File to edit: html.ipynb (unless otherwise specified).

__all__ = ['td', 'tr', 'th', 'table', 'row', 'ROW']

# Cell
from IPython.display import HTML

# Cell
def td(obj):
    """Create a table entry from string or object with html representation."""
    if hasattr(obj, '_repr_html_'):
        return f'<td style="text-align:left;">{obj._repr_html_()}</td>'
    elif hasattr(obj, '_repr_image_svg_xml'):
        return f'<td style="text-align:left;">{obj._repr_image_svg_xml()}</td>'
    else:
        return f'<td style="text-align:left;">{obj}</td>' # uses __str__


# Cell
def tr(cells):
    """Create a table row"""
    tds = [td(cell) for cell in cells]
    return "<tr>\n" + "\n".join(tds) + "\n</tr>"


def th(cells):
    """Create a table header"""
    return tr(cells).replace("<td ", "<th ").replace("</td>", "</th>")


# Cell
def table(rows, header="", cls: str = "gtbook_table"):
    """Create a table from rows"""
    return "<table width=\"100%\" class={cls}>\n" + header + "\n" + "\n".join(rows) + "</table>\n"

def row(cells):
    """Create a table with a single row"""
    return table([tr(cells)])

def ROW(cells): return HTML(row(cells))