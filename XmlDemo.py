# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:37:29 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

import xml.etree.ElementTree as ET
import requests


request_url = 'https://www.ebi.ac.uk/chembl/api/data/atc_class?q=CHEMBL25'
s = requests.Session()
xml = s.get(request_url).text

tree = ET.fromstring(xml)#tree: <Element 'response' at 0x000001579A4F0B88>

atc = tree.findall('atc')[0]#atcs: <Element 'atc' at 0x000001579A4F0BD8>

for atc_class in atc:
    level5 = atc_class.findall('level5')[0].text
    print(level5)
