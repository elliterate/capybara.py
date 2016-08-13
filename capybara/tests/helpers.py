import json
from lxml import etree
from werkzeug.datastructures import ImmutableMultiDict


def extract_results(session):
    tree = etree.HTML(session.body)
    element = tree.xpath("//pre[@id='results']")[0]

    def inner_html(elem):
        return "".join(
            [elem.text or ""] +
            [etree.tostring(child).decode("utf-8") for child in elem] +
            [elem.tail or ""])

    return ImmutableMultiDict(json.loads(inner_html(element)))
