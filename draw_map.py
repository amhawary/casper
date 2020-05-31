from PIL import Image,ImageDraw,ImageFont
import json


Coords = {"China": [3085,725,72], 
          "Denmark": [1882,372,16],
          "Japan": [3684,680,48],
          "Ecuador": [565,1253,36], 
          "Benin": [1862,1173,16],
          "Belgium": [1865,428,11], 
          "Belarus": [2153,421,18], 
          "Austria": [2009,506,10], 
          "Bahrain":[2503,829,9], 
          "Chile": [711,1575,56], 
          "Andorra": [1889,600,9], 
          "Holy See (Vatican City State)": [1980,624,9], 
          "Albania": [2059,641,10], 
          "Algeria": [1809,798,36], 
          "Angola": [2037,1438,20], 
          "Antigua and Barbuda": [1043,982,20], 
          "Argentina": [934,1729,28], 
          "Azerbaijan": [2422,617,8], 
          "Bahamas": [852,852,24], 
          "Barbados":[1030,1073,24], 
          "Belize": [666,961,11], 
          "Bhutan": [3021,795,11], 
          "Bolivia": [928,1519,22], 
          "Bosnia and Herzegovina": [2021,588,8], 
          "Botswana": [2127,1588,10], 
          "Bulgaria": [2132,587,10], 
          "Burkina Faso": [1776,1602,8], 
          "Burundi": [2199,1307,9], 
          "Cambodia": [3240,1044,10], 
          "Cape Verde": [1434,1006,10], 
          "Central African Republic": 31, 
          "Chad": [2075,993,20], 
          "Comoros": [2421,1410,12], 
          "Congo (Brazzaville)": [2033,1248,8], 
          "Congo (Kinshasa)": [2083,1288,14], 
          "Costa Rica": [516,1045,10], 
          "C\u00f4te d'Ivoire": [1724,1142,10], 
          "Croatia": [2010,568,8], 
          "Cuba": [794,904,10], 
          "Cyprus": [2192,699,10], 
          "Czech Republic": [2001,478,8], 
          "Dominica": [1023,1015,8], 
          "Dominican Republic": [953,946,8], 
          "El Salvador": [533,1050,8], 
          "Equatorial Guinea": [1908,1221,8], 
          "Eritrea": [2335,1019,8], 
          "Estonia": [2132,347,8], 
          "Fiji": [4062,1367,12], 
          "Finland": [2114,290,16], 
          "Gabon": [1977,1257,8], 
          "Gambia": [1525,1042,8], 
          "Georgia": [2303,581,10], 
          "Grenada": [938,1057,8], 
          "Guatemala": [504,1019,8], 
          "Guinea": [1653,1085,8], 
          "Guinea-Bissau": [1544,1075,8], 
          "Haiti": [822,911,8], 
          "Hungary": [2053,522,8], 
          "Iraq": [2364,740,26], 
          "Italy": [1945,553,10], 
          "Jamaica": [730,961,8], 
          "Jordan": [2307,776,8], 
          "Kazakhstan": [2580,501,14], 
          "Kenya": [2317,1244,9], 
          "Korea (South)": [3498,654,8], 
          "Kyrgyzstan":[2756,602,8], 
          "Lao PDR": [3209,939,8], 
          "Latvia": [2113,377,8], 
          "Armenia": [2382,623,8], 
          "Kuwait": [2435,809,10], 
          "Djibouti": [2431,1066,9], 
          "Iceland": [1669,235,12], 
          "Israel": [2252,743,14], 
          "Brunei Darussalam": [3385,1165,8], 
          "Ethiopia": [2323,1122,12], 
          "Lebanon": [2226,716,10], 
          "Greece": [2104,643,8], 
          "Cameroon": [1972,1181,10], 
          "Ghana": [1796,1135,12], 
          "Afghanistan": [2650,719,10], 
          "Egypt": [2198,845,28], 
          "Indonesia": [3505,1384,14], 
          "Colombia": [785,1200,10], 
          "Bangladesh":[3017,934,10], 
          "Ireland": [1717,466,16], 
          "Iran, Islamic Republic of": [2482,740,48], 
          "Guyana": [1002,1154,8], 
          "India": [2842,883,48], 
          "Germany": [1931,458,10], 
          "Honduras": [643,977,8], 
          "Australia": [3535,1636,48], 
          "Brazil": [1088,1410,72], 
          "Madagascar": 93, 
          "Lithuania": 94, 
          "Luxembourg": 95, 
          "Monaco": [1896,588,11], 
          "Liechtenstein": 97, 
          "Lesotho": 98, 
          "Liberia": 99, 
          "Libya": [2013,828,28], 
          "Macedonia, Republic of": 101, 
          "Malawi": 102, 
          "Malaysia": 103, 
          "Mali": 104, 
          "Malta": 105, 
          "Mauritania": 106, 
          "Mexico": [424,891,11], 
          "Moldova": 108, 
          "Mongolia": 109, 
          "Montenegro": [2061,640,9], 
          "Morocco": [1717,765,11], 
          "Mozambique": [2287,1540,10], 
          "Myanmar": 113, 
          "Nicaragua": [701,1003,3], 
          "Niger": [1914,990,14], 
          "Norway": [1930,307,16], 
          "Panama": [573,1072,16], 
          "Papua New Guinea": [3774,1283,8], 
          "Paraguay": [1022,1620,16], 
          "Philippines": [3560,1087,10], 
          "Poland": [2049,439,16], 
          "Romania": [2117,531,16], 
          "Russian Federation": [2300,324,84], 
          "Rwanda": [2197,1281,8], 
          "Saint Kitts and Nevis": [988,970,8], 
          "Maldives": [2855,1216,10], 
          "Namibia": [2036,1558,16], 
          "Peru": [599,1407,48], 
          "Republic of Kosovo": [2103,597,6], 
          "Nigeria": [1904,1103,18], 
          "Qatar": [2530,849,11], 
          "Pakistan": [2693,813,18], 
          "Portugal": [1640,621,20], 
          "Nepal": [2920,807,9], 
          "Mauritius": [2581,1553,10], 
          "Palestinian Territory": [2248,729,18], 
          "Netherlands": [1878,404,9], 
          "New Zealand": [3996,1972,12], 
          "Oman": [2558,960,12], 
          "Zimbabwe": [2193,1546,9], 
          "Uruguay": [1139,1817,20], 
          "San Marino": [1989,583,8], 
          "Uganda": [2266,1220,9], 
          "Switzerland": [1932,529,8], 
          "Saint Lucia": [916,993,8], 
          "Saint Vincent and Grenadines": [930,1069,8], 
          "Senegal": [1539,1003,10], 
          "Serbia": [2091,572,8], 
          "Seychelles": [2581,1334,10], 
          "Sierra Leone": [1576,1129,8], 
          "Slovakia": [2059,502,8], 
          "Slovenia": [2016,535,8], 
          "Somalia": [2411,1911,16], 
          "South Sudan": [2189,1112,18], 
          "Sri Lanka": [2959,1165,12], 
          "Sudan": [2186,978,18], 
          "Suriname": [1061,1146,8], 
          "Swaziland": [2278,1877,8], 
          "Sweden": [1992,335,10], 
          "Syrian Arab Republic (Syria)": [2316,699,20], 
          "Taiwan, Republic of China": [3432,916,14], 
          "Tajikistan": [2727,653,8], 
          "Tanzania, United Republic of": [2277,1351,18], 
          "Thailand": [3202,993,14], 
          "Timor-Leste": [3513,1421,8], 
          "Togo": [1832,1190,16], 
          "Trinidad and Tobago": [1007,1091,11], 
          "Tunisia": [1994,701,24], 
          "Turkey": [2259,642,28], 
          "Ukraine": [2203,495,28], 
          "Uzbekistan": [2621,599,9], 
          "Venezuela (Bolivarian Republic)": [898,1112,18], 
          "Viet Nam": [3336,1033,14], 
          "Western Sahara": [1517,861,22], 
          "Yemen": [2445,1005,20], 
          "Zambia": [2148,1481,20], 
          "Sao Tome and Principe": [1850,1243,16], 
          "Singapore": [3262,1215,16], 
          "United Arab Emirates": [2602,868,11], 
          "South Africa": [2079,1700,24], 
          "Spain": [1773,610,24], 
          "Saudi Arabia": [2386,884,20], 
          "Canada": [508,329,72], 
          "France": [1848,536,20], 
          "United Kingdom": [1735,334,14],
          "United States of America": [515,656,36]}
names_to_fix={
"Holy See (Vatican City State)":"Vatican",
"C\u00f4te d'Ivoire":"Ivory Coast",
"Iran, Islamic Republic of":"Iran",
"Syrian Arab Republic (Syria)":"Syria",
"Taiwan, Republic of China": "Taiwan",
"Tanzania, United Republic of":"Tanzania" ,
"Venezuela (Bolivarian Republic)": "Venezuela",
"Macedonia, Republic of":"Macedonia",
"Palestinian Territory":"Palestine",
"Swaziland":"Eswatini"}
def fix_name(name):
    if name in names_to_fix.keys():
        return names_to_fix[name]
    else:
        return name
data = json.load(open('casper_scores.json',"r"))
img = Image.open('blank map.jpg')
img2 = img
for i in data.keys():
    if i not in Coords.keys() or type(Coords[i])!=list:
        print("skipping",i)
        continue
    countryname =fix_name(i)
    order = str(data[i]) + "/186"
    draw = ImageDraw.Draw(img2)
    font = ImageFont.truetype("Roboto-Black.ttf", Coords[i][2])
    draw.text((Coords[i][0], Coords[i][1]),countryname,(0,0,0),font=font)
    draw.text((Coords[i][0], Coords[i][1] + Coords[i][2]),order,(0,0,0),font=font)
img2.save('../casper-team.github.io/static/index.jpg')