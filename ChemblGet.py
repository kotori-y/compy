# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:03:09 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Zelda Princess forever♥
"""

print(__doc__)

import requests
from requests import exceptions
import json
from collections import namedtuple



def SearchTargetFromName(name):
    """
    """
    proxies = {"http": "http://58.218.10.49:808",
               "http": "http://58.241.58.115:808",
               "http": "http://114.239.145.255:808"}
    resl = []
    res = namedtuple('TargetInfo',['organism','pref_name','arget_chembl_id','target_type'])
    request_url = 'https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={}'.format(name)
    s = requests.Session()
    try:
        f = s.get(request_url,timeout=60,proxies=proxies)
        if f.status_code == 200:
            data = json.loads(f.text)
            for target in data['targets']:
                info = [target['organism'],target['pref_name'],target['target_chembl_id'],target['target_type']]
                resl.append(res(*info))
            return resl
        else:
            return None
    except exceptions.Timeout:
        return 'Timeout'
    

#def SearchTargetFromUniprotID(uniprot_id):
#    """
#    uniprot_id = P28472 
#    """
#    request_url = 'https://www.ebi.ac.uk/chembl/api/data/target?Uniprot={}'.format(uniprot_id)
#    s = requests.Session()
#    xml = s.get(request_url,timeout=60).text
#    tree = x,l
    
    
    
    
    
if '__main__' == __name__:
    name = 'Carbonic anhydrase 4'
    res = SearchTargetFromName(name)
    print(res)