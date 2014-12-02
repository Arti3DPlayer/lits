#-*- coding: utf-8 -*-
#!/usr/bin/python

import os
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
		
		self.load_scenario()


	def load_scenario(self):
		
		load_script = """
			local response = http.get("http://example.com')
			log.info("Load time: "..response.total_load_time.."s")
			client.sleep(5)
			"""
		user_scenario = self.client.create_user_scenario({
		    'name': "My user scenario",
		    'load_script': load_script
		})


lia = LoadImpactAssigment(api_token='731de9cc2b6c5e6a69312dc8b201c6a0edfed098dce04727a822c1c8b7adeb18')

# file_path = os.path.join(os.path.dirname(__file__), 'apache-jmeter.jmx')
# xml = etree.parse(file_path)
# for root_hashtree in xml.getroot().getchildren():
# 	testplan = etree_to_dict(root_hashtree.find("TestPlan"))
# 	threadgroup = etree_to_dict(root_hashtree.find("hashTree").find("ThreadGroup"))
# 	config_test = etree_to_dict(root_hashtree.find("hashTree").find("hashTree").find("ConfigTestElement"))
	
# 	sample_proxies = [etree_to_dict(sample_proxy) for sample_proxy in root_hashtree.find("hashTree").find("hashTree").findall("hashTree")[1].findall("HTTPSamplerProxy")]
# 	print sample_proxy
# 	#print config_test['ConfigTestElement'][get_index(config_test['ConfigTestElement'], "@name", "HTTPSampler.domain")]


	


# 	# if len(hashtree_child):
# 	# 	threadgroup = dict()
# 	# 	config_test = dict()
# 	# 	sample_proxy = dict()
# 	# 	for tag in hashtree_child.find("ThreadGroup"):
# 	# 		key = tag.get("name").replace("ThreadGroup.", "")
# 	# 		threadgroup[key] = tag.text

# 	# 	config_test_elem = hashtree_child.find("hashTree").find("ConfigTestElement")
# 	# 	for tag in config_test_elem:
# 	# 		key = tag.get("name").replace("HTTPSampler.", "")
# 	# 		config_test[key] = tag.text

# 	# 	sample_proxy_elem = hashtree_child.find("hashTree").findall("hashTree")[1].find("HTTPSamplerProxy")
# 	# 	for tag in sample_proxy_elem:
# 	# 		key = tag.get("name").replace("HTTPSampler.", "")
# 	# 		sample_proxy[key] = tag.text

# 	#for hashtree_child in root_hashtree.find("hashTree"):
# 	#	print hashtree_child
# 		#for threadgroup in xml_hashtree_child.find("ThreadGroup"):
# 		#	print threadgroup