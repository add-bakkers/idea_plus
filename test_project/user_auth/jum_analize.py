from pyknp import Juman
import codecs
import re

jumanpp = Juman()

def juman_analize(text):
    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub(r'[︰-＠]', "", text)#全角記号
    text=re.sub(r'[!-/:-@[-`{-~]', "", text)#半角記号
    text=re.sub('\n', "", text)#改行文字
    text=text.replace(" ","")
    results=[]
    if len(text)==0:
        return results
    result=jumanpp.analysis(text)
    for mrph in result.mrph_list(): #各形態素にアクセス
        if len(re.sub(r'[0-9]+', "", mrph.midasi))==0:
            continue
        if (mrph.hinsi[-2:]=="名詞" or mrph.imis[-2:]=="名詞"):
            results.append(mrph) #見出し語をリストに追加
    return results
