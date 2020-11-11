# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 09:20:33 2019

@Author: Zhi-Jiang Yang(Kotori)
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: kotori@cbdd.me& kotori@csu.edu.cn
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import requests
from lxml import etree
from collections import namedtuple
import re
import json
from requests import exceptions
import xml.etree.ElementTree as ET
import pandas as pd
import multiprocessing as mp

def GetInfoFromDrugBank(drugb_id,item_list=['Name','SMILES', 'ATC Codes']):
    """
    This function is aim to get molecular infomation through DrugBankID
    """
    def GetXpath(item):
        return '//*[@class="col-xl-2 col-md-3 col-sm-4"][text()="{}"]/following-sibling::dd[1]'.format(item)
    
    def GetInfo(xpath_list):
        idx = 0
        while idx != len(xpath_list):
            XPATH = xpath_list[idx]
            if len(XPATH) != 73:
                check = html.xpath(XPATH)
                if check:
                    yield check[0].xpath('string(.)')
                else:
                    yield None
            else:
                check = html.xpath(XPATH)
                if check:
                    yield [item.replace('/atc/','') for item in check]
                else:
                    yield None
            idx += 1


    try:   
        request_url = "https://go.drugbank.com/drugs/{}".format(drugb_id)
        s = requests.Session()
        html = s.get(request_url,timeout=30).text
        html = etree.HTML(html)
        
        atc_xpath = '//*[@class="col-xl-10 col-md-9 col-sm-8"]/a[contains(@href, "atc")]/@href'
        xpath_list = [[GetXpath(item),atc_xpath][item=='ATC Codes'] for item in item_list]
        info_list = [item for item in GetInfo(xpath_list)]
        info_list.insert(0,drugb_id)
         
        item_list = [x.replace(' ','_') for x in item_list]
        item_list.insert(0,'DrugBankID')
        res = namedtuple('DrugBank',item_list)      
        return res(*info_list)    
    except exceptions.Timeout:
        return 'Timeout'  
    except:
        return None


def GetInfoFromUniprot(UniProt_id,):
    """
    UniProt_id = 'P23975'
    """
    request_url = 'https://www.uniprot.org/uniprot/{}.xml'.format(UniProt_id)
    s = requests.Session()
    try:
        r = s.get(request_url,timeout=30)
        if r.status_code == 200:
            tree = ET.fromstring(r.text)
            entry = tree[0]
            dbReference = entry.findall('{http://uniprot.org/uniprot}dbReference[@type="ChEMBL"]')
            res = [i.attrib['id'] for i in dbReference]
        else:
            res = [None]       
    except:
        res = [None]
    
    return '|'.join(res)


def GetInfoFromZinc():
    """
    """
    pass



def GetTargetFromChembel(Chembl_id,Xref_src_db=['UniProt']):
    """
    CHEMBL25
    """
    request_url = 'https://www.ebi.ac.uk/chembl/api/data/target/{}.json'.format(Chembl_id)
    s = requests.Session()
    response = s.get(request_url,timeout=60).text
    data = json.loads(response)
    info = [Chembl_id,data['organism'],data['pref_name']]
    xref = [x['xref_id']\
            for x in data['target_components'][0]['target_component_xrefs']\
            if x['xref_src_db'] in Xref_src_db]
    info.append(xref)
    
    items = ['Chembl_id','Organism','Pref_name']
    items.extend(Xref_src_db)
    res = namedtuple('ChEMBLTarget',items)   
    return res(*info)


def GetInfoFromPubChem(cid,item_list=['InChI','InChI Key','Canonical SMILES']):
    """
    *Now only support the info exist in 3rd level titls
    """
    def GetRegx(item):
        return r'"TOCHeading": "{}".*?"String": "(.*?)"'.format(item)
    
    def GetInfo(regx_list):
        idx = 0
        while idx != len(regx_list):
            regx = regx_list[idx]
            check = re.findall(regx,html,re.S)
            if check:
                yield check[0]
            else:
                yield None            
            idx += 1
    
    try:
        try:
            cid = str(int(cid))
        except:
            pass
        cid = cid.replace('cid','')
        request_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{}/JSON/'.format(cid)
        s = requests.Session()
        html = s.get(request_url,timeout=30).text
        regx_list = [GetRegx(item) for item in item_list]
        info_list = [info for info in GetInfo(regx_list)]
        info_list.insert(0,cid)
        item_list = [x.replace(' ','_') for x in item_list]
        item_list.insert(0,'CID')    
    except exceptions.Timeout:
        return 'Timeout'
    except:
        return None

    res = namedtuple('PubChem',item_list)
    return res(*info_list)
        
    

def GetInfoFromKegg():
    """
    """
    pass



def GetInfoFromPDBbind(PDBcode,item_list=['PDB ID','Protein Name','Ligand Name','Resolution','Canonical SMILES','InChI String']):
    """
    10gs
    """
    def GetXpath(item):
        return '//*[@class="register"][text()="{}"]/following-sibling::td'.format(item)
    
    def GetInfo(xpath_list):
        idx = 0
        while idx != len(xpath_list):
            XPATH = xpath_list[idx]           
            check = html.xpath(XPATH)
            if check:
                yield check[0].xpath('string(.)').strip('\n\r')
            else:
                yield None           
            idx += 1
    try:
        request_url = 'http://www.pdbbind-cn.org/quickpdb.asp'
        s = requests.Session()
        form_data = {'quickpdb': PDBcode,}
        response = s.post(request_url,data=form_data,timeout=30)
        html = response.text
        html = etree.HTML(html)
        xpath_list = [GetXpath(item) for item in item_list]
        info_list = [info for info in GetInfo(xpath_list)]
        info_list.insert(0,PDBcode)
        
        item_list.insert(0,'PDBcode')
        item_list = [x.replace(' ','_') for x in item_list]
        res = namedtuple('PDBbind',item_list)
        
        return res(*info_list)
    except:
        return None



def GetInfoFromBindingDB(uniprot):
    """
    """
    def _getinfo(TREE,XPATH):
        return TREE.xpath(XPATH)
    
    ori_url = 'https://www.bindingdb.org/bind/tabLuceneResult.jsp?thisInput={}&submit=Go'.format(uniprot)
    s = requests.Session()
    response = s.get(ori_url)
    html = response.text
    tree = etree.HTML(html)
    num = _getinfo(tree, XPATH='//*[@class="red"]/text()')[0]
#    print(num)
    
    new_url = ''.join([response.url,'&Increment={}'.format(num)])
    
    response = s.get(new_url,timeout=120)
    html = response.text
    tree = etree.HTML(html)
    single = _getinfo(tree, XPATH='//*[@class="single"]')[0::3]
    double = _getinfo(tree, XPATH='//*[@class="double"]')[0::3]
    
    mid = [
            j.xpath('td[2]/a[1]/text()')[0] 
            for item in [single,double] for j in item
            ]
    smi = [
            j.xpath('td[2]//*[@style="display:none"]')[0].xpath('string(.)')
            for item in [single,double] for j in item
            ]
    ki = [
            j.xpath('*[@align="center"]')[0].xpath('string(.)')
            for item in [single,double] for j in item
            ]
    IC50 = [
            j.xpath('*[@align="center"]')[2].xpath('string(.)')
            for item in [single,double]
            for j in item
            ]
    kd = [
            j.xpath('*[@align="center"]')[3].xpath('string(.)')
            for item in [single,double] for j in item
            ]
    EC50_IC50 = [
            j.xpath('*[@align="center"]')[4].xpath('string(.)')
            for item in [single,double] for j in item
            ]
#    print(smi)
    
    out = pd.DataFrame({'mid':mid,
                        'SMILES':smi,
                        'Ki':ki,
                        'IC50':IC50,
                        'Kd':kd,
                        'EC50/IC50':EC50_IC50})
    
    return out
    


def GetDrugBankBind(drugbank_id):
    url = 'https://www.drugbank.ca/drugs/{}'.format(drugbank_id)
    container_xpath = '//*[contains(@class, "bond-list-container")]'
    card_xpath = '*[@class="bond-list"]/*[@class="bond card"]'
    data_xpath = '*[@aria-labelledby="binding properties"]//*[@class="table table-sm"]//tbody/tr'
    s = requests.Session()
    
    try:
        response = s.get(url)
        html = response.text
        tree = etree.HTML(html)
    except:
        yield pd.DataFrame({drugbank_id: {'UniprotID':None,
                            'Value':None,
                            'Unit':None,
                            'type':None}}).T  
                            
    containers = tree.xpath(container_xpath)
    if containers:
        for container in containers:
            _type = re.findall('bond-list-container\W(\w*)',container.attrib['class'])[0]
            
            cards = container.xpath(card_xpath)
            for card in cards:
                _id = card.xpath('*[@class="card-body"]//*[@class="col-md-5 col-sm-6"][text()="Uniprot ID"]/following-sibling::dd[1]')
                _id = _id[0].xpath('string(.)') if _id else None
                
                datas = card.xpath(data_xpath)
                if datas:
                    for data in datas:
                        unit,val = data.xpath('td/text()')[:2]
                        yield pd.DataFrame({drugbank_id:{'UniprotID':_id,
                                        'Value':val,
                                        'Unit':unit,
                                        'type':_type}}).T
                else:
                    yield pd.DataFrame({drugbank_id:{'UniprotID':_id,
                                        'Value':None,
                                        'Unit':None,
                                        'type':_type}}).T
    else:
        yield pd.DataFrame({drugbank_id: {'UniprotID':None,
                            'Value':None,
                            'Unit':None,
                            'type':None}}).T



def GetKey(uniprot):
    url = 'https://www.uniprot.org/uniprot/{}'.format(uniprot)
    response = requests.get(url)
    
    if response.status_code==200:
        html = response.text
        tree = etree.HTML(html)
        func = tree.xpath('//*[@class="databaseTable"]//td[text()="Molecular function"]/following-sibling::td')[0]
        func = func.xpath('string(.)')
        print('>>> {} Finished'.format(uniprot))
        return '|'.join(func.split(','))
    else:
        print('>>> {} Finished'.format(uniprot))
        return ''


def ChemblidToCid(chemblid):
    
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/xml".format(chemblid)
    
    response = requests.get(url)
    tree = etree.XML(response.text)
    
    cid = tree.findall(
        '{http://www.ncbi.nlm.nih.gov}PC-Compound//{http://www.ncbi.nlm.nih.gov}PC-CompoundType_id_cid'
        )[0].text
    
    return cid
    
def main(drugbank_id):
    d = GetDrugBankBind(drugbank_id)
    return pd.concat(d)
    
    
if '__main__' == __name__:
    
    drugbank_id = "DB00945"
    print(
        GetInfoFromDrugBank(drugbank_id)
    )
    