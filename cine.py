import json

import requests
from bs4 import BeautifulSoup

URL = "http://infocar.dgt.es/etraffic/Incidencias?ca=13&provIci=28&caracter=acontecimiento&accion_consultar=Consultar&IncidenciasRETENCION=IncidenciasRETENCION&IncidenciasPUERTOS=IncidenciasPUERTOS&IncidenciasMETEOROLOGICA=IncidenciasMETEOROLOGICA&IncidenciasEVENTOS=IncidenciasEVENTOS&IncidenciasOTROS=IncidenciasOTROS&IncidenciasRESTRICCIONES=IncidenciasRESTRICCIONES&ordenacion=fechahora_ini-DESC"
content = requests.get(URL)
soup = BeautifulSoup(content.text, "html.parser")
results = []

items = soup.find('tbody')
for item in items.findAll('tr'):
    incidence = {}
    columns = item.findAll('td')
    incidence["hora_inicio"] = columns[0].find('span', {'class': 'orange'}).get_text()
    incidence["fecha_inicio"] = columns[0].findAll('p')[1].find('a').text
    incidence["hora_fin"] = columns[1].find('span', {'class': 'orange'}).get_text()
    incidence["fecha_fin"] = columns[1].findAll('p')[1].text if len(columns[1].findAll('p')) > 0 is not None else ""
    incidence["tipo"] = columns[2].find('img').get('alt')
    incidence["provincia"] = columns[3].findAll('p')[0].text + " " + columns[3].findAll('p')[1].text
    incidence["carretera"] = columns[4].find('b').text
    description = ""
    for info in columns[5].findAll('span'):
        description += info.text
    incidence["descripcion"] = description
    results.append(incidence)

with open("results.json","w") as results_file:
    json.dump(results, results_file,indent=4,sort_keys=True, ensure_ascii=False)