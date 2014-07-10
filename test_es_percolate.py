__author__ = 'kuchar'
import random
import time
import elasticsearch

INDEX = 'test-index'
TYPE = 'test-type'
NR_OF_QUERIES = 300000
NR_OF_TESTS = 100

es = elasticsearch.Elasticsearch('localhost')

words = ['account','act','addition','adjustment','advertisement','agreement','air','amount','amusement','animal',
         'answer','apparatus','approval','argument','art','attack','attempt','attention','attraction','authority',
         'back','balance','base','behaviour','belief','birth','bit','bite','blood','blow','body','brass','bread',
         'breath','brother','building','burn','burst','business','butter','canvas','care','cause','chalk','chance',
         'change','cloth','coal','colour','comfort','committee','company','comparison','competition','condition',
         'connection','control','cook','copper','copy','cork','cotton','cough','country','cover','crack','credit',
         'crime','crush','cry','current','curve','damage','danger','daughter','day','death','debt','decision',
         'degree','design','desire','destruction','detail','development','digestion','direction','discovery',
         'discussion','disease','disgust','distance','distribution','division','doubt','drink','driving','dust',
         'earth','edge','education','effect','end','error','event','example','exchange','existence','expansion',
         'experience','expert','fact','fall','family','father','fear','feeling','fiction','field','fight','fire',
         'flame','flight','flower','fold','food','force','form','friend','front','fruit','glass','gold','government',
         'grain','grass','grip','group','growth','guide','harbour','harmony','hate','hearing','heat','help','history',
         'hole','hope','hour','humour','ice','idea','impulse','increase','industry','ink','insect','instrument',
         'insurance','interest','invention','iron','jelly','join','journey','judge','jump','kick','kiss','knowledge',
         'land','language','laugh','law','lead','learning','leather','letter','level','lift','light','limit','linen',
         'liquid','list','look','loss','love','machine','man','manager','mark','market','mass','meal','measure',
         'meat','meeting','memory','metal','middle','milk','mind','mine','minute','mist','money','month','morning',
         'mother','motion','mountain','move','music','name','nation','need','news','night','noise','note','number',
         'observation','offer','oil','operation','opinion','order','organization','ornament','owner','page','pain',
         'paint','paper','part','paste','payment','peace','person','place','plant','play','pleasure','point','poison',
         'polish','porter','position','powder','power','price','print','process','produce','profit','property',
         'prose','protest','pull','punishment','purpose','push','quality','question','rain','range','rate','ray',
         'reaction','reading','reason','record','regret','relation','religion','representative','request','respect',
         'rest','reward','rhythm','rice','river','road','roll','room','rub','rule','run','salt','sand','scale',
         'science','sea','seat','secretary','selection','self','sense','servant','sex','shade','shake','shame',
         'shock','side','sign','silk','silver','sister','size','sky','sleep','slip','slope','smash','smell','smile',
         'smoke','sneeze','snow','soap','society','son','song','sort','sound','soup','space','stage','start',
         'statement','steam','steel','step','stitch','stone','stop','story','stretch','structure','substance','sugar',
         'suggestion','summer','support','surprise','swim','system','talk','taste','tax','teaching','tendency',
         'test','theory','thing','thought','thunder','time','tin','top','touch','trade','transport','trick','trouble',
         'turn','twist','unit','use','value','verse','vessel','view','voice','walk','war','wash','waste','water',
         'wave','wax','way','weather','week','weight','wind','wine','winter','woman','wood','wool','word','work',
         'wound','writing','year'
]

mappings = {
    'mappings': {
        TYPE: {
            'properties': {
                'name': {
                    u'type': u'string',
                },
                'location': {
                    u'type': u'geo_point',
                }
            }
        }
    }
}

try:
    es.indices.delete(index=INDEX)
except Exception:
    pass

es.indices.create(index=INDEX, body=mappings)

query_template = """{
    "query": {
        "filtered": {
            "filter": {
                "geo_distance": {
                    "distance": "%s",
                    "location": [%s, %s]
                }
            },
            "query": {
                "match": {
                    "_all": "%s"
                }
            }
        }
    },
    "type": "%s"
}"""
start = time.time()
for i in xrange(1, NR_OF_QUERIES):
    query_str = " ".join([random.choice(words) for x in range(random.randrange(1,4))])
    lon = random.randint(-179,179)
    lat = random.randint(-179,179)
    distance = random.randint(1,100)
    doc = query_template % (distance, lon, lat, query_str, TYPE)
    es.create(index=INDEX, doc_type='.percolator', body=doc, id=i)

es.indices.refresh(index=INDEX)

print "Indexed", NR_OF_QUERIES, "queries into precolator, took", (time.time() - start), "seconds"

doc = {
    "doc":{
        "name": "belief",
        "location": [88,132]
    }
}

# Warm up
for i in xrange(10):
    es.percolate(index=INDEX, doc_type=TYPE, body=doc)

sum = 0
for i in xrange(NR_OF_TESTS):
    sum += es.percolate(index=INDEX, doc_type=TYPE, body=doc)['took']

avg = float(sum)/float(NR_OF_TESTS)

print "After", NR_OF_TESTS, "tests, average query time:", avg