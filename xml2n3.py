import os
from lxml import etree
import sys
from rdflib import ConjunctiveGraph, Namespace, Literal


primer = ConjunctiveGraph()
myNS = Namespace('#')


def make_xpath(el, path=None):
    if path is None:
        path = ''
    if el is not None:
        path = '/%s[@%s="%s"]%s' % (el.tag, 'NAME', el.attrib['NAME'], path)
        return make_xpath(el.getparent(), path)
    else:
        return '/%s' % path


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <input xml file> <output n3 file>\n" % (argv[0],))
        return 1

    if not os.path.exists(argv[1]):
        sys.stderr.write("ERROR: File %r was not found!\n" % (argv[1],))
        return 1

    in_file = argv[1]

    tree = etree.parse(in_file)

    for el in tree.iter('*'):
        for child in el:
            primer.add((myNS[make_xpath(el)], myNS['child'], myNS[make_xpath(child)]))
        for attrib, value in el.attrib.iteritems():
            primer.add((myNS[make_xpath(el)], myNS[attrib], Literal(value)))

    for p in primer:
        print '%s %s %s' % p


if __name__ == "__main__":
    sys.exit(main(sys.argv))