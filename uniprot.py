# -*- coding: utf-8 -*-
"""
Created on Sun May 24 16:36:41 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


from multiprocessing import Pool
import pandas as pd
from requests import Session
from lxml import etree
from xml.etree import ElementTree as ET
import json
from functools import namedtuple


def GetUniprotInfo(uniprotID='P08684', attemp=0):
    """
    """
    #attemp = 0
    if attemp > 5:
        print(uniprotID)
        return [None, None, None]
        
    url = 'https://www.uniprot.org/uniprot/{}'.format(uniprotID)
    s = Session()
    
    try:
        response = s.get(url, timeout=20)
        html = response.text
        
        tree = etree.HTML(html)
        
        protein = tree.xpath('//*[@id="content-protein"]')[0].xpath('string(.)')
        gene = tree.xpath('//*[@id="content-gene"]')[0].xpath('string(.)')
        org = tree.xpath('//*[@id="content-organism"]')[0].xpath('string(.)')
        
    except :
        attemp += 1
        print(attemp)
        GetUniprotInfo(uniprotID, attemp)

        
    print(uniprotID)
    return [protein, gene, org]


def GetInfoFromUniprot(UniProt_id, attemp=0):
    """
    UniProt_id = 'P23975'
    """
    request_url = 'https://www.uniprot.org/uniprot/{}.xml'.format(UniProt_id)
    s = Session()
    try:
        r = s.get(request_url, timeout=60)
        if r.status_code == 200:
            tree = ET.fromstring(r.text)
            entry = tree[0]
            name = entry.find('{http://uniprot.org/uniprot}protein//{http://uniprot.org/uniprot}recommendedName')[0].text
            gene = entry.find('{http://uniprot.org/uniprot}gene')[0].text
            organ = entry.find('{http://uniprot.org/uniprot}organism')[0].text
            # res = [i.attrib['id'] for i in dbReference]
        else:
            if attemp>=5:
                name, gene, organ = [None]*3    
            else:
                return GetInfoFromUniprot(UniProt_id, attemp+1)
    except:
        if attemp>=5:
            name, gene, organ = [None]*3    
        else:
            return GetInfoFromUniprot(UniProt_id, attemp+1)
    
    print(UniProt_id)
    return {'Name':name, 'Gene':gene, 'Organism':organ}


def main(targets):
    """
    """
    pool = Pool()
    res = pool.map_async(GetInfoFromUniprot, targets).get()
    pool.close()
    pool.join()
    return res

if '__main__' == __name__:
    from tqdm import tqdm
    data = pd.read_csv(r'C:\Users\0720\Desktop\MATE\Sorcha\0729.csv')
    targets = data[data.Gene.isna()].UniProt.tolist()
    res = []
    
    for target in tqdm(targets):
        res.append(GetInfoFromUniprot(target))
    
    