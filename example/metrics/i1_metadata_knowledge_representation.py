from fair_test import FairTest
import json
import rdflib
# JSON-LD workaround 
# from pyld import jsonld
# from rdflib import ConjunctiveGraph
# from rdflib.serializer import Serializer


class MetricTest(FairTest):
    metric_path = 'i1-metadata-knowledge-representation'
    applies_to_principle = 'I1'
    title = 'Metadata uses a formal knowledge representation language (strong)'
    description = """Maturity Indicator to test if the metadata uses a formal language broadly applicable for knowledge representation.
This particular test takes a broad view of what defines a 'knowledge representation language'; in this evaluation, a knowledge representation language is interpreted as one in which terms are semantically-grounded in ontologies.
Any form of RDF will pass this test"""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'


    def evaluate(self):        
        # https://github.com/vemonet/fuji/blob/master/fuji_server/helper/preprocessor.py#L190
        g = self.retrieve_rdf(self.subject)
        if len(g) > 1:
            self.success('Successfully parsed the RDF metadata retrieved with content negotiation. It contains ' + str(len(g)) + ' triples')

        self.info('Check embedded metadata available from extruct')
        if 'extruct' in self.data.keys() and 'json-ld' in self.data['extruct'].keys():
            extruct_g = rdflib.ConjunctiveGraph()
            try:
                # print(json.dumps(self.data['extruct']['json-ld'], indent=2))
                extruct_g.parse(data=json.dumps(self.data['extruct']['json-ld']), format='json-ld')
                self.success('JSON-LD metadata embedded in HTML from extruct successfully parsed with RDFLib')
            except Exception as e:
                self.warn('Could not parse JSON-LD metadata from extruct with RDFLib')
                print(e)
        # TODO: other format? microdata, dublincore, etc
        else:
            self.warn('No metadata embedded in HTML available for parsing from extruct')

        return self.response()

    test_test={
        'https://doi.org/10.1594/PANGAEA.908011': 1,
    }