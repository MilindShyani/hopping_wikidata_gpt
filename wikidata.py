import requests
import argparse
from SPARQLWrapper import SPARQLWrapper, JSON

def get_wikidata_id(entity_name):
    url = 'https://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'search': entity_name
    }

    response = requests.get(url, params=params)
    data = response.json()

    # If there are results, get the ID of the first
    if data['search']:
        return data['search'][0]['id']
    else:
        return None


def get_linked_ids(wikidata_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # SPARQL query to get all items linked to a specific Wikidata ID
    sparql_query = """
        SELECT DISTINCT ?item ?itemLabel WHERE {
          wd:""" + wikidata_id + """ ?p ?item .
          ?item wikibase:statements ?st .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        """
    sparql.setQuery(sparql_query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    ids_and_labels = []
    for result in results["results"]["bindings"]:
        # Extract the QID from the result's URI
        qid = result['item']['value'].split('/')[-1]
        # Get the label (name) of the item
        label = result['itemLabel']['value']
        ids_and_labels.append((qid, label))

    return ids_and_labels



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve Wikidata QID for an entity.')
    parser.add_argument('entity', help='The entity for which to find the Wikidata QID')
    args = parser.parse_args()

    entity = args.entity
    qid = get_wikidata_id(entity)
    if qid:
        print(f"The QID for '{entity}' is {qid}")
    else:
        print(f"No QID found for '{entity}'")

    visited = set()
    visited.add((qid, entity))

    to_visit = get_linked_ids(qid)
    k = 0

    while k < 1:
        new_visit = set()
        while to_visit:
            (id, name) = to_visit.pop()
            if (id,name) not in visited:
                new_ids_labels = get_linked_ids(id)
                if len(new_ids_labels) <= 20:
                    for nid,nlab in new_ids_labels:
                        new_visit.add((nid, nlab))
                visited.add((id,name))
        to_visit = new_visit
        k += 1

        print(visited, "\n \n \n \n", new_visit)










