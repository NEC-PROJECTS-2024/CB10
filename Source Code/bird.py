from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.metrics import AUC
import numpy as np

bird = Flask(__name__)

dependencies = {
    'auc_roc': AUC
}

verbose_name = {
0: 'ABBOTTS BABBLER',
1: 'ABBOTTS BOOBY',
2: 'ABYSSINIAN GROUND HORNBILL',
3: 'AFRICAN CROWNED CRANE',
4: 'AFRICAN EMERALD CUCKOO',
5: 'AFRICAN FIREFINCH',
6: 'AFRICAN OYSTER CATCHER',
7: 'ALBATROSS',
8: 'ALBERTS TOWHEE',
9: 'ALEXANDRINE PARAKEET',
10: 'ALPINE CHOUGH',
11: 'ALTAMIRA YELLOWTHROAT',
12: 'AMERICAN AVOCET',
13: 'AMERICAN BITTERN',
14: 'AMERICAN COOT',
15: 'AMERICAN GOLDFINCH',
16: 'AMERICAN KESTREL',
17: 'AMERICAN PIPIT',
18: 'AMERICAN REDSTART',
19: 'AMETHYST WOODSTAR',
20: 'ANDEAN GOOSE',
21: 'ANDEAN LAPWING',
22: 'ANDEAN SISKIN',
23: 'ANHINGA',
24: 'ANIANIAU',
25: 'ANNAS HUMMINGBIRD',
26: 'ANTBIRD',
27: 'ANTILLEAN EUPHONIA',
28: 'APAPANE',
29: 'APOSTLEBIRD',
30: 'ARARIPE MANAKIN',
31: 'ASHY THRUSHBIRD',
32: 'ASIAN CRESTED IBIS',
33: 'AVADAVAT',
34: 'AZURE JAY',
35: 'AZURE TANAGER',
36: 'AZURE TIT',
37: 'BAIKAL TEAL',
38: 'BALD EAGLE',
39: 'BALD IBIS',
40: 'BALI STARLING',
41: 'BALTIMORE ORIOLE',
42: 'BANANAQUIT',
43: 'BAND TAILED GUAN',
44: 'BANDED BROADBILL',
45: 'BANDED PITA',
46: 'BANDED STILT',
47: 'BAR-TAILED GODWIT',
48: 'BARN OWL',
49: 'BARN SWALLOW',
50: 'BARRED PUFFBIRD',
51: 'BARROWS GOLDENEYE',
52: 'BAY-BREASTED WARBLER',
53: 'BEARDED BARBET',
54: 'BEARDED BELLBIRD',
55: 'BEARDED REEDLING',
56: 'BELTED KINGFISHER',
57: 'BIRD OF PARADISE',
58: 'BLACK & YELLOW  BROADBILL',
59: 'BLACK BAZA',
60: 'BLACK COCKATO',
61: 'BLACK FRANCOLIN',
62: 'BLACK SKIMMER',
63: 'BLACK SWAN',
64: 'BLACK TAIL CRAKE',
65: 'BLACK THROATED BUSHTIT',
66: 'BLACK THROATED WARBLER',
67: 'BLACK VULTURE',
68: 'BLACK-CAPPED CHICKADEE',
69: 'BLACK-NECKED GREBE',
70: 'BLACK-THROATED SPARROW',
71: 'BLACKBURNIAM WARBLER',
72: 'BLONDE CRESTED WOODPECKER',
73: 'BLUE COAU',
74: 'BLUE GROUSE',
75: 'BLUE HERON',
76: 'BLUE THROATED TOUCANET',
77: 'BOBOLINK',
78: 'BORNEAN BRISTLEHEAD',
79: 'BORNEAN LEAFBIRD',
80: 'BORNEAN PHEASANT',
81: 'BRANDT CORMARANT',
82: 'BROWN CREPPER',
83: 'BROWN NOODY',
84: 'BROWN THRASHER',
85: 'BULWERS PHEASANT',
86: 'BUSH TURKEY',
87: 'CACTUS WREN',
88: 'CALIFORNIA CONDOR',
89: 'CALIFORNIA GULL',
90: 'CALIFORNIA QUAIL',
91: 'CANARY',
92: 'CAPE GLOSSY STARLING',
93: 'CAPE LONGCLAW',
94: 'CAPE MAY WARBLER',
95: 'CAPE ROCK THRUSH',
96: 'CAPPED HERON',
97: 'CAPUCHINBIRD',
98: 'CARMINE BEE-EATER',
99: 'CASPIAN TERN',
100: 'CASSOWARY',
101: 'CEDAR WAXWING',
102: 'CERULEAN WARBLER',
103: 'CHARA DE COLLAR',
104: 'CHATTERING LORY',
105: 'CHESTNET BELLIED EUPHONIA',
106: 'CHINESE BAMBOO PARTRIDGE',
107: 'CHINESE POND HERON',
108: 'CHIPPING SPARROW',
109: 'CHUCAO TAPACULO',
110: 'CHUKAR PARTRIDGE',
111: 'CINNAMON ATTILA',
112: 'CINNAMON FLYCATCHER',
113: 'CINNAMON TEAL',
114: 'CLARKS NUTCRACKER',
115: 'COCK OF THE  ROCK',
116: 'COCKATOO',
117: 'COLLARED ARACARI',
118: 'COMMON FIRECREST',
119: 'COMMON GRACKLE',
120: 'COMMON HOUSE MARTIN',
121: 'COMMON IORA',
122: 'COMMON LOON',
123: 'COMMON POORWILL',
124: 'COMMON STARLING',
125: 'COPPERY TAILED COUCAL',
126: 'CRAB PLOVER',
127: 'CRANE HAWK',
128: 'CREAM COLORED WOODPECKER',
129: 'CRESTED AUKLET',
130: 'CRESTED CARACARA',
131: 'CRESTED COUA',
132: 'CRESTED FIREBACK',
133: 'CRESTED KINGFISHER',
134: 'CRESTED NUTHATCH',
135: 'CRESTED OROPENDOLA',
136: 'CRESTED SHRIKETIT',
137: 'CRIMSON CHAT',
138: 'CRIMSON SUNBIRD',
139: 'CROW',
140: 'CROWNED PIGEON',
141: 'CUBAN TODY',
142: 'CUBAN TROGON',
143: 'CURL CRESTED ARACURI',
144: 'D-ARNAUDS BARBET',
145: 'DARK EYED JUNCO',
146: 'DEMOISELLE CRANE',
147: 'DOUBLE BARRED FINCH',
148: 'DOUBLE BRESTED CORMARANT',
149: 'DOUBLE EYED FIG PARROT',
150: 'DOWNY WOODPECKER',
151: 'DUSKY LORY',
152: 'EARED PITA',
153: 'EASTERN BLUEBIRD',
154: 'EASTERN GOLDEN WEAVER',
155: 'EASTERN MEADOWLARK',
156: 'EASTERN ROSELLA',
157: 'EASTERN TOWEE',
158: 'ELEGANT TROGON',
159: 'ELLIOTS  PHEASANT',
160: 'EMERALD TANAGER',
161: 'EMPEROR PENGUIN',
162: 'EMU',
163: 'ENGGANO MYNA',
164: 'EURASIAN GOLDEN ORIOLE',
165: 'EURASIAN MAGPIE',
166: 'EUROPEAN GOLDFINCH',
167: 'EUROPEAN TURTLE DOVE',
168: 'EVENING GROSBEAK',
169: 'FAIRY BLUEBIRD',
170: 'FAIRY TERN',
171: 'FIORDLAND PENGUIN',
172: 'FIRE TAILLED MYZORNIS',
173: 'FLAME BOWERBIRD',
174: 'FLAME TANAGER',
175: 'FLAMINGO',
176: 'FRIGATE',
177: 'GAMBELS QUAIL',
178: 'GANG GANG COCKATOO',
179: 'GILA WOODPECKER',
180: 'GILDED FLICKER',
181: 'GLOSSY IBIS',
182: 'GO AWAY BIRD',
183: 'GOLD WING WARBLER',
184: 'GOLDEN CHEEKED WARBLER',
185: 'GOLDEN CHLOROPHONIA',
186: 'GOLDEN EAGLE',
187: 'GOLDEN PHEASANT',
188: 'GOLDEN PIPIT',
189: 'GOULDIAN FINCH',
190: 'GRAY CATBIRD',
191: 'GRAY KINGBIRD',
192: 'GRAY PARTRIDGE',
193: 'GREAT GRAY OWL',
194: 'GREAT JACAMAR',
195: 'GREAT KISKADEE',
196: 'GREAT POTOO',
197: 'GREATOR SAGE GROUSE',
198: 'GREEN BROADBILL',
199: 'GREEN JAY',
200: 'GREEN MAGPIE',
201: 'GREY PLOVER',
202: 'GROVED BILLED ANI',
203: 'GUINEA TURACO',
204: 'GUINEAFOWL',
205: 'GURNEYS PITTA',
206: 'GYRFALCON',
207: 'HAMMERKOP',
208: 'HARLEQUIN DUCK',
209: 'HARLEQUIN QUAIL',
210: 'HARPY EAGLE',
211: 'HAWAIIAN GOOSE',
212: 'HAWFINCH',
213: 'HELMET VANGA',
214: 'HEPATIC TANAGER',
215: 'HIMALAYAN BLUETAIL',
216: 'HIMALAYAN MONAL',
217: 'HOATZIN',
218: 'HOODED MERGANSER',
219: 'HOOPOES',
220: 'HORNBILL',
221: 'HORNED GUAN',
222: 'HORNED LARK',
223: 'HORNED SUNGEM',
224: 'HOUSE FINCH',
225: 'HOUSE SPARROW',
226: 'HYACINTH MACAW',
227: 'IBERIAN MAGPIE',
228: 'IBISBILL',
229: 'IMPERIAL SHAQ',
230: 'INCA TERN',
231: 'INDIAN BUSTARD',
232: 'INDIAN PITTA',
233: 'INDIAN ROLLER',
234: 'INDIGO BUNTING',
235: 'INLAND DOTTEREL',
236: 'IVORY GULL',
237: 'IWI',
238: 'JABIRU',
239: 'JACK SNIPE',
240: 'JANDAYA PARAKEET',
241: 'JAPANESE ROBIN',
242: 'JAVA SPARROW',
243: 'KAGU',
244: 'KAKAPO',
245: 'KILLDEAR',
246: 'KING VULTURE',
247: 'KIWI',
248: 'KOOKABURRA',
249: 'LARK BUNTING',
250: 'LAZULI BUNTING',
251: 'LESSER ADJUTANT',
252: 'LILAC ROLLER',
253: 'LITTLE AUK',
254: 'LONG-EARED OWL',
255: 'MAGPIE GOOSE',
256: 'MALABAR HORNBILL',
257: 'MALACHITE KINGFISHER',
258: 'MALAGASY WHITE EYE',
259: 'MALEO',
260: 'MALLARD DUCK',
261: 'MANDRIN DUCK',
262: 'MANGROVE CUCKOO',
263: 'MARABOU STORK',
264: 'MASKED BOOBY',
265: 'MASKED LAPWING',
266: 'MIKADO  PHEASANT',
267: 'MOURNING DOVE',
268: 'MYNA',
269: 'NICOBAR PIGEON',
270: 'NOISY FRIARBIRD',
271: 'NORTHERN CARDINAL',
272: 'NORTHERN FLICKER',
273: 'NORTHERN FULMAR',
274: 'NORTHERN GANNET',
275: 'NORTHERN GOSHAWK',
276: 'NORTHERN JACANA',
277: 'NORTHERN MOCKINGBIRD',
278: 'NORTHERN PARULA',
279: 'NORTHERN RED BISHOP',
280: 'NORTHERN SHOVELER',
281: 'OCELLATED TURKEY',
282: 'OKINAWA RAIL',
283: 'ORANGE BRESTED BUNTING',
284: 'ORIENTAL BAY OWL',
285: 'OSPREY',
286: 'OSTRICH',
287: 'OVENBIRD',
288: 'OYSTER CATCHER',
289: 'PAINTED BUNTING',
290: 'PALILA',
291: 'PARADISE TANAGER',
292: 'PARAKETT  AKULET',
293: 'PARUS MAJOR',
294: 'PATAGONIAN SIERRA FINCH',
295: 'PEACOCK',
296: 'PELICAN',
297: 'PEREGRINE FALCON',
298: 'PHILIPPINE EAGLE',
299: 'PINK ROBIN',
300: 'POMARINE JAEGER',
301: 'PUFFIN',
302: 'PURPLE FINCH',
303: 'PURPLE GALLINULE',
304: 'PURPLE MARTIN',
305: 'PURPLE SWAMPHEN',
306: 'PYGMY KINGFISHER',
307: 'QUETZAL',
308: 'RAINBOW LORIKEET',
309: 'RAZORBILL',
310: 'RED BEARDED BEE EATER',
311: 'RED BELLIED PITTA',
312: 'RED BROWED FINCH',
313: 'RED FACED CORMORANT',
314: 'RED FACED WARBLER',
315: 'RED FODY',
316: 'RED HEADED DUCK',
317: 'RED HEADED WOODPECKER',
318: 'RED HONEY CREEPER',
319: 'RED NAPED TROGON',
320: 'RED TAILED HAWK',
321: 'RED TAILED THRUSH',
322: 'RED WINGED BLACKBIRD',
323: 'RED WISKERED BULBUL',
324: 'REGENT BOWERBIRD',
325: 'RING-NECKED PHEASANT',
326: 'ROADRUNNER',
327: 'ROBIN',
328: 'ROCK DOVE',
329: 'ROSY FACED LOVEBIRD',
330: 'ROUGH LEG BUZZARD',
331: 'ROYAL FLYCATCHER',
332: 'RUBY THROATED HUMMINGBIRD',
333: 'RUDY KINGFISHER',
334: 'RUFOUS KINGFISHER',
335: 'RUFUOS MOTMOT',
336: 'SAMATRAN THRUSH',
337: 'SAND MARTIN',
338: 'SANDHILL CRANE',
339: 'SATYR TRAGOPAN',
340: 'SCARLET CROWNED FRUIT DOVE',
341: 'SCARLET IBIS',
342: 'SCARLET MACAW',
343: 'SCARLET TANAGER',
344: 'SHOEBILL',
345: 'SHORT BILLED DOWITCHER',
346: 'SMITHS LONGSPUR',
347: 'SNOWY EGRET',
348: 'SNOWY OWL',
349: 'SORA',
350: 'SPANGLED COTINGA',
351: 'SPLENDID WREN',
352: 'SPOON BILED SANDPIPER',
353: 'SPOONBILL',
354: 'SPOTTED CATBIRD',
355: 'SRI LANKA BLUE MAGPIE',
356: 'STEAMER DUCK',
357: 'STORK BILLED KINGFISHER',
358: 'STRAWBERRY FINCH',
359: 'STRIPED OWL',
360: 'STRIPPED MANAKIN',
361: 'STRIPPED SWALLOW',
362: 'SUPERB STARLING',
363: 'SWINHOES PHEASANT',
364: 'TAILORBIRD',
365: 'TAIWAN MAGPIE',
366: 'TAKAHE',
367: 'TASMANIAN HEN',
368: 'TEAL DUCK',
369: 'TIT MOUSE',
370: 'TOUCHAN',
371: 'TOWNSENDS WARBLER',
372: 'TREE SWALLOW',
373: 'TROPICAL KINGBIRD',
374: 'TRUMPTER SWAN',
375: 'TURKEY VULTURE',
376: 'TURQUOISE MOTMOT',
377: 'UMBRELLA BIRD',
378: 'VARIED THRUSH',
379: 'VENEZUELIAN TROUPIAL',
380: 'VERMILION FLYCATHER',
381: 'VICTORIA CROWNED PIGEON',
382: 'VIOLET GREEN SWALLOW',
383: 'VIOLET TURACO',
384: 'VULTURINE GUINEAFOWL',
385: 'WALL CREAPER',
386: 'WATTLED CURASSOW',
387: 'WATTLED LAPWING',
388: 'WHIMBREL',
389: 'WHITE BROWED CRAKE',
390: 'WHITE CHEEKED TURACO',
391: 'WHITE NECKED RAVEN',
392: 'WHITE TAILED TROPIC',
393: 'WHITE THROATED BEE EATER',
394: 'WILD TURKEY',
395: 'WILSONS BIRD OF PARADISE',
396: 'WOOD DUCK',
397: 'YELLOW BELLIED FLOWERPECKER',
398: 'YELLOW CACIQUE',
399: 'YELLOW HEADED BLACKBIRD',
400: 'ZEBRA DOVE'
}

model = load_model('birds_fine.h5', compile=False)

model.make_predict_function()

def predict_label(img_path, threshold=0.2):
    test_image = image.load_img(img_path, target_size=(224, 224))
    test_image = image.img_to_array(test_image) / 255.0
    test_image = test_image.reshape(1, 224, 224, 3)

    predict_x = model.predict(test_image)
    max_probability = np.max(predict_x)

    if max_probability < threshold:
        return "This image does not contain a bird."

    classes_x = np.argmax(predict_x, axis=1)
    return verbose_name[classes_x[0]]


# routes

@bird.route("/")
@bird.route("/first")
def first():
	return render_template('first.html')
    

    
@bird.route("/index", methods=['GET'])
def index():
	return render_template("index.html")


@bird.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/tests/" + img.filename	 # type: ignore
		img.save(img_path)

		predict_result = predict_label(img_path)

	return render_template("prediction.html", prediction = predict_result, img_path = img_path)
   

if __name__ =='__main__':
    bird.run(host='0.0.0.0', port=5000, debug=True)