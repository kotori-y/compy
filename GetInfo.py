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

#print(__doc__)

import requests
from lxml import etree
from collections import namedtuple


def GetInfoFromDrugBank(drugb_id,item_list=['Name','SMILES','ATC Codes']):
    """
    This function is aim to get molecular infomation through DrugBankID
    """
    def GetXpath(item):
        return '//*[@class="col-md-2 col-sm-4"][text()="{}"]/following-sibling::dd[1]'.format(item)
    
    def GetInfo(xpath_list):
        idx = 0
        while idx != len(xpath_list):
            XPATH = xpath_list[idx]
            if len(XPATH) != 64:
                if html.xpath(XPATH):
                    yield html.xpath(XPATH)[0].xpath('string(.)')
                else:
                    yield None
            else:
                if html.xpath(XPATH):
                    yield [item.replace('/atc/','') for item in html.xpath(XPATH)]
                else:
                    yield None
            idx += 1
    
        
    request_url = "https://www.drugbank.ca/drugs/{}".format(drugb_id)
    s = requests.Session()
    html = s.get(request_url,timeout=60).text
    html = etree.HTML(html)
    
    atc_xpath = '//*[@class="col-md-10 col-sm-8"]/a[@href="ATC Codes"]/@href'
    xpath_list = [[GetXpath(item),atc_xpath][item=='ATC Codes'] for item in item_list]
    info_list = [item for item in GetInfo(xpath_list)]
    info_list.insert(0,drugb_id)
     
    item_list = [x.replace(' ','_') for x in item_list]
    item_list.insert(0,'DrugBankID')
    res = namedtuple('DrugBank',item_list)
    
    return res(*info_list)


def GetInfoFromZinc():
    """
    """
    pass


def GetInfoFromChembel():
    """
    """
    pass


def GetInfoFromPubChem(cid):
    """
    """
    pass


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

    request_url = 'http://www.pdbbind-cn.org/quickpdb.asp'
    s = requests.Session()
    form_data = {'quickpdb': PDBcode,
                 'x': 42,
                 'y': 21}
    response = s.post(request_url,data=form_data,timeout=60)
    html = response.text
    html = etree.HTML(html)
    xpath_list = [GetXpath(item) for item in item_list]
    info_list = [html.xpath(XPATH)[0].xpath('string(.)').strip('\n\r') for XPATH in xpath_list]
    info_list.insert(0,PDBcode)
    
    item_list.insert(0,'PDBcode')
    item_list = [x.replace(' ','_') for x in item_list]
    res = namedtuple('PDBbind',item_list)
    
    return res(*info_list)
    
        
if '__main__' == __name__:
#    drugbank_id = ['DB00010',
#                   'DB00569',
#                   'DB01226']
#    
#    for drugb_id in drugbank_id:
#        res = GetInfoFromDrugBank(drugb_id,item_list=['Name','SMILES','ATC Codes','CAS number','InChI Key'])
#        print(res)
#        print('\n')
    
    
    PDBcode = '10gs'
    res = GetInfoFromPDBbind(PDBcode)
    print(res)
        
        
        
        
        
        
        
        
        
        
        
        
        