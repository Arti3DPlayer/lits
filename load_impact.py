#-*- coding: utf-8 -*-
#!/usr/bin/python

import os
import urllib
import loadimpact

from lxml import etree


def etree_to_dict(tree):
    """
    Convert etree element to dict
    """
    d = {tree.tag : map(etree_to_dict, tree.iterchildren())}
    d.update(('@' + k, v) for k, v in tree.attrib.iteritems())
    d['text'] = tree.text
    return d


def get_index(seq, attr, value):
    """
    Find dict key in list and return index of element
    """
    return next(index for (index, d) in enumerate(seq) if d[attr] == value)


class LoadImpactAssigment(object):

    def __init__(self, api_token, xml_file_name='apache-jmeter.jmx'):
        self.xml_file_name = xml_file_name
        self.client = loadimpact.ApiTokenClient(api_token=api_token)
        self.read_xml(self.xml_file_name)

    def read_xml(self, file_name):
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        xml = etree.parse(file_path)
        for root_hashtree in xml.getroot().getchildren():
            self.testplan = etree_to_dict(root_hashtree.find("TestPlan"))
            self.threadgroup = etree_to_dict(root_hashtree.find("hashTree").find("ThreadGroup"))
            self.config_test = etree_to_dict(root_hashtree.find("hashTree").find("hashTree").find("ConfigTestElement"))
            self.sample_proxies = [etree_to_dict(sample_proxy) for sample_proxy in root_hashtree.find("hashTree").find("hashTree").findall("hashTree")[1].findall("HTTPSamplerProxy")]

        self.load_scenarios()
        self.load_config()

    def load_scenarios(self):
        domain = self.config_test['ConfigTestElement'][get_index(self.config_test['ConfigTestElement'], "@name", "HTTPSampler.domain")]['text']
        for script in self.sample_proxies:
            path = script['HTTPSamplerProxy'][get_index(script['HTTPSamplerProxy'], "@name", "HTTPSampler.path")]['text']
            method = script['HTTPSamplerProxy'][get_index(script['HTTPSamplerProxy'], "@name", "HTTPSampler.method")]['text']
            for collection_prop in script['HTTPSamplerProxy'][get_index(script['HTTPSamplerProxy'], "@name", "HTTPsampler.Arguments")]['elementProp']:
                query = dict()
                for element_prop in collection_prop['collectionProp']:
                    q_name = element_prop['elementProp'][get_index(element_prop['elementProp'], "@name", "Argument.name")]['text']
                    q_value = element_prop['elementProp'][get_index(element_prop['elementProp'], "@name", "Argument.value")]['text']
                    query[q_name] = q_value

                query = urllib.urlencode(query)
                if query:
                    query = "?%s" % query
                try:
                    self.client.create_user_scenario({
                    'name': "%s%s%s" % (domain, path, query),
                    'load_script': 'http.request_batch({{"%s", "%s%s%s"}})' % (method, domain, path, query)
                    })
                except loadimpact.exceptions.ConflictError:
                    print 'Url http.request_batch({{"%s", "%s%s"}) is already exsist.' % (method, path, query)

    def load_config(self):
        name = self.testplan['@testname']
        domain = self.config_test['ConfigTestElement'][get_index(self.config_test['ConfigTestElement'], "@name", "HTTPSampler.domain")]['text']
        tracks = list()
        scenario_count = len(self.client.list_user_scenarios())
        for scenario in self.client.list_user_scenarios():
            tracks.append({
                "clips": [{
                    "user_scenario_id": int(scenario.id), 'percent': 100/scenario_count
                }],
                "loadzone": loadimpact.LoadZone.AMAZON_US_ASHBURN,
            })
        num_threads = int(self.threadgroup['ThreadGroup'][get_index(self.threadgroup['ThreadGroup'], "@name", "ThreadGroup.num_threads")]['text'])
        ramp_time = int(self.threadgroup['ThreadGroup'][get_index(self.threadgroup['ThreadGroup'], "@name", "ThreadGroup.ramp_time")]['text'])
        config = self.client.create_test_config({
            'name': name,
            'url': 'http://%s/' % domain,
            'config': {
                "load_schedule": [{"users": num_threads, "duration": ramp_time}],
                "tracks": tracks,
                "user_type": "sbu"
            }
        })


if __name__ == "__main__":
    lia = LoadImpactAssigment(api_token='731de9cc2b6c5e6a69312dc8b201c6a0edfed098dce04727a822c1c8b7adeb18')