import web
import json
from mimerender import mimerender
from xml.dom.minidom import Document
import copy
import cgi
from decimal import Decimal

class Dict2Xml(object):
    doc     = Document()

    def __init__(self, structure):
        if len(structure) == 1:
            rootName    = str(structure.keys()[0])
            self.root   = self.doc.createElement(rootName)

            self.doc.appendChild(self.root)
            self.build(self.root, structure[rootName])

    def build(self, father, structure):
        if type(structure) == dict:
            for k in structure:
                tag = self.doc.createElement(k)
                father.appendChild(tag)
                self.build(tag, structure[k])

        elif type(structure) == list:
            grandFather = father.parentNode
            tagName     = father.tagName
            grandFather.removeChild(father)
            for l in structure:
                tag = self.doc.createElement(tagName)
                self.build(tag, l)
                grandFather.appendChild(tag)

        else:
            data    = str(structure)
            tag     = self.doc.createTextNode(data)
            father.appendChild(tag)

    def display(self):
        print self.doc.toprettyxml(indent="  ")

urls = (
        '/complaints', 'complaints',
        '/categories', 'categories',
        '/category/(.*)', 'category',
        '/advice', 'advice',
        '/advice/(\d+)', 'adviceitem',
        '/advice/to/(\d+)', 'adviceto',
        '/advice/by/(\d+)', 'adviceby',
        '/advisors', 'advisors',
        '/advisor/(\d+)', 'advisor'
    )

app = web.application(urls, globals())

db = web.database(dbn = 'postgres', user='alex', pw='alex', db='medserver-test')

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


render_json = lambda **args: json.dumps(args, default = handler)
render_xml = lambda **args: Dict2Xml(args).display()

formatter = mimerender(
        default = 'json',
        json = render_json,
        xml = render_xml
    )

class complaints:
    @formatter
    def GET(self):
        complaints = db.query("""
            SELECT c.id, c.created, c.summary, c.pain_level, c.concern_level, area.name as category 
            FROM complaint c
            JOIN area ON c.area = area.id
            """)
        return dict(results = [dict(c) for c in complaints])

class categories:
    @formatter
    def GET(self):
        categories = db.query("""
            SELECT name, count(*) as complaints
            FROM area
            JOIN complaint ON area.id = complaint.area
            GROUP BY area.name
            """)
        return dict(results = [dict(r) for r in categories])

class category:
    @formatter
    def GET(self, name):
        complaints = db.query("""
            SELECT id, created, summary, pain_level, concern_level
            FROM complaint 
            WHERE area = (SELECT a.id FROM area a WHERE a.name = $name)
            """, vars=dict(name = name))
        return dict(results = [dict(c) for c in complaints])

class advice:
    @formatter
    def GET(self):
        responses = db.query("""
            SELECT id, advice, rating
            FROM response
            """)
        return dict(results = [dict(r) for r in responses])

    @formatter
    def POST(self):
        i = web.input()
        n = db.insert('response', complaint = i.complaint, advice = i.advice, advisor = i.advisor)
        web.created(headers = dict(Location = "/advice/" + str(n)))

class adviceitem:
    @formatter
    def GET(self, itemid):
        items = db.where("response", "advice, rating, complaint, advisor", id = itemid)
        return dict(results = [dict(r) for r in items])

    @formatter
    def PUT(self, itemid):
        i = dict(cgi.parse_qsl(web.data()))
        q = db.update('response', where = 'id = $itemid', rating = i["rating"], vars=locals())
        web.accepted(headers = dict(Location = "/advice/" + str(itemid)))
        return dict(results = ["/advice/" + str(itemid)])

class adviceto:
    @formatter
    def GET(self, itemid):
        items = db.where("response", "advice, rating, advisor", complaint = itemid)
        return dict(results = [dict(r) for r in items])

    @formatter
    def POST(self, itemid):
        i = web.input()
        n = db.insert('response', complaint = itemid, 
                advice = i.advice, advisor = i.advisor)
        web.created(headers = dict(Location = "/advice/" + str(n)))
        return dict(results = ["/advice/" + str(n)])

class adviceby:
    @formatter
    def GET(self, itemid):
        items = db.query("""
            SELECT response.id, advice, rating, complaint.summary as issue
            FROM response
            JOIN complaint ON response.complaint = complaint.id
            WHERE advisor = $a
            """, vars = dict(a = itemid))
        return dict(results = [dict(r) for r in items])

class advisors:
    @formatter
    def GET(self):
        items = db.query("""
            SELECT a.id, a.name, a.profile, a.member_since, a.institution, AVG(r.rating) as average_rating
            FROM advisor AS a
            JOIN response AS r ON r.advisor = a.id
            GROUP BY a.id, a.name, a.profile, a.member_since, a.institution
            """)
        return dict(results = [dict(r) for r in items])

class advisor:
    @formatter
    def GET(self, itemid):
        items = db.query("""
            SELECT a.id, a.name, a.profile, a.member_since, a.institution, 
                AVG(r.rating) as average_rating
            FROM advisor AS a
            JOIN response AS r ON r.advisor = a.id
            WHERE a.id = $a
            GROUP BY a.id, a.name, a.profile, a.member_since, a.institution
            """, vars = dict(a = itemid))
        return dict(results = [dict(r) for r in items])

if __name__ == '__main__':
    app.run()
