import json
from xml.dom.minidom import parse
import xml.dom.minidom
import os


wlist=['背','差','长','传','当','地','得','行','觉','空','乐','难','片','弹','为','系','相','血','应','只','重','中']
plist=['bei','cha','chang','chuan','dang','de','dei','hang','jiao','kong','le','nan','pian','tan','wei','xi','xiang','xue','ying','zhi','zhong','zhong1']
data_path="../data/zh-CN/"
wpaths=plist
phones=set()
train=[]
test=[]
for n,wpath in enumerate(wpaths):
    print("processing",wpath)
    #train data
    DOMTree = xml.dom.minidom.parse(os.path.join(data_path,wpath,"training.xml"))
    collection = DOMTree.documentElement
    sis = collection.getElementsByTagName("si")
    for si in sis:
        js_data = {'id': si.getAttribute('id')}
        js_data['text'] = si.childNodes[1].childNodes[0].data
        js_data['position'] = -1
        for i, w in enumerate(js_data['text']):
            if w == wlist[n]:
                js_data['position'] = i
        assert js_data['position'] != -1
        for w in si.getElementsByTagName("w"):
            if w.getAttribute('v') == wlist[n]:
                js_data['phone'] = w.getAttribute('p')
        assert 'phone' in js_data.keys()
        train.append(js_data)
        phones.add(js_data['phone'])
    #test data
    DOMTree = xml.dom.minidom.parse(os.path.join(data_path, wpath, "test.xml"))
    collection = DOMTree.documentElement
    sis = collection.getElementsByTagName("si")
    for si in sis:
        js_data = {'id': si.getAttribute('id')}
        js_data['text'] = si.childNodes[1].childNodes[0].data
        js_data['position'] = -1
        for i, w in enumerate(js_data['text']):
            if w == wlist[n]:
                js_data['position'] = i
        assert js_data['position'] != -1
        for w in si.getElementsByTagName("w"):
            if w.getAttribute('v') == wlist[n]:
                js_data['phone'] = w.getAttribute('p')
        assert 'phone' in js_data.keys()
        test.append(js_data)
        phones.add(js_data['phone'])
#save
with open("../data/train.json",'w',encoding='utf8') as f:
    f.write(json.dumps(train))
with open("../data/test.json",'w',encoding='utf8') as f:
    f.write(json.dumps(test))
info={"words":wlist,"wpaths":plist,"phones":sorted(list(phones))}
with open("../data/info.json",'w',encoding='utf8') as f:
    f.write(json.dumps(info))
