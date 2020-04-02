import sqlite3

def Search(word,word_net_dict,conn):

    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    word_id = -1
    for row in cur:
        word_id = row[0]
    results_dict = {}
    if word_id==-1:
        return results_dict #wordnetに存在しない

    cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
    synsets = []
    for row in cur:
        synsets.append(row[0])
    results_dict = {}
    roop_search=[]
    for synset in synsets:
        # 上位語にアクセスし続ける
        while(synset in word_net_dict.keys()):
            results_dict[synset]=word_net_dict[synset]
            if synset in roop_search:
                break
            synset = word_net_dict[synset]
            roop_search.append(synset)
    return results_dict
