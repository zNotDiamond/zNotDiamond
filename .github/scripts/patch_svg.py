import sys
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

path = sys.argv[1]
tree = ET.parse(path)
root = tree.getroot()
parents = {child: parent for parent in root.iter() for child in parent}


def q(tag):
    return f"{{{NS}}}{tag}"


def remove(el):
    parents[el].remove(el)


def text_at(x, y):
    for t in root.iter(q("text")):
        if t.get("x") == x and t.get("y") == y:
            return t
    return None


def group_at(transform):
    for g in root.iter(q("g")):
        if g.get("transform") == transform:
            return g
    return None


# left graph to remove
g = group_at("translate(40, 520)")
if g is not None:
    remove(g)

# stars counters to remove
g = group_at("translate(608, 802), scale(2)")
if g is not None:
    remove(g)
t = text_at("650", "830")
if t is not None:
    remove(t)

# contributions repositioning
t = text_at("384", "830")
if t is not None:
    t.set("x", "100"); t.set("y", "610")
t = text_at("394", "830")
if t is not None:
    t.set("x", "110"); t.set("y", "610")

# Forks repositioning
g = group_at("translate(736, 802), scale(2)")
if g is not None:
    g.set("transform", "translate(50, 650), scale(2)")
t = text_at("772", "830")
if t is not None:
    t.set("x", "86"); t.set("y", "678")

tree.write(path, encoding="utf-8", xml_declaration=False)
