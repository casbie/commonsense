#-*-coding:utf-8-*-

#1. load concepts
#2. for relation r, load related concepts
#3. analysis(filter)
import json
from postagger_zh.postagger import POSTagger
import multiprocessing

def do_pos(text):
	tagger = POSTagger()
	tag_map={}
	order=[]
	for token, tag in tagger.tag(text):
		if token == '。':
			continue
		tag_map[token] = tag
		order.append(token)
	return tag_map, order

#not used now
#loading the conceptNet json data from given file
#output format: [rel, start, end]
def load_conceptNet(file_name):
    json_file = open(file_name,'r')
    conceptNet = []
    for line in json_file:
        data = json.loads(line)
        rel = data['rel'].encode('utf-8')[len('/r/'):]
        start = data['start'].encode('utf-8')[len('/c/zh_TW/'):]
        end = data['end'].encode('utf-8')[len('/c/zh_TW/'):]
        conceptNet.append([rel,start,end])
    json_file.close()
    return conceptNet

#input file format:
#start,end,surfaceText([start]temp[end]temp)
#output format: (start,end,sentence)
def load_sentence(relation):
	fp=open('../../relation/'+relation+'.txt','r')
	sentence=[]
	for line in fp:
		tmp=line.strip()
		tmp=tmp.replace('。','')
		spt=tmp.split(',')
		start=spt[0]
		end=spt[1]
		stc=spt[2]
		sentence.append([unicode(start,'utf-8'),unicode(end,'utf-8'),unicode(stc,'utf-8')])
	return sentence

def run(stc):
	[start_map, start_order]=do_pos(stc[0])
	[end_map, end_order]=do_pos(stc[1])
	template=[]
	stc_sp=stc[2].split(' ')
	for i in range(0,len(stc_sp)):
		if '[' not in stc_sp[i]:
			template.append(stc_sp[i])
		else:
			if stc_sp[i] == '[['+stc[0]+']]':
				template.append('A')
			else:
				template.append('B')
	surfaceText=stc[2].replace('[','').replace(']','').replace(' ','')

	print stc[0]
	return [start_order, end_order, start_map, end_map, template, surfaceText]

def pos_all(relation):
	sentence = load_sentence(relation)
	fp_out=open(relation+'_pos.txt','w')
	pool = multiprocessing.Pool(10)
	p = pool.map( run , sentence )
	json_list=[]
	for i in p:
		start_order=i[0]
		end_order=i[1]
		start_map=i[2]
		end_map=i[3]
		template=i[4]
		surfaceText=i[5]
		tmp_map={}
		tmp_start=[]
		tmp_end=[]
		tmp_template=''
		for tok in start_order:
			tmp_start.append(tok+'_'+start_map[tok])
		tmp_map['start']=tmp_start
		for tok in end_order:
			tmp_end.append(tok+'_'+end_map[tok])
		tmp_map['end']=tmp_end
		for i in template:
			tmp_template=tmp_template+i
		tmp_map['template']=tmp_template
		tmp_map['surfaceText']=surfaceText
		json_list.append(tmp_map)
	json.dump(json_list,fp_out)

def run_stc(stc):
	surfaceText=stc[2].replace('[','').replace(']','').replace(' ','')
	[stc_map,stc_order]=do_pos(surfaceText)
	print stc[0]
	return [stc_order, stc_map, surfaceText]

def pos_all_stc(relation):
	sentence = load_sentence(relation)
	fp_out=open(relation+'_posstc.txt','w')
	pool = multiprocessing.Pool(10)
	p = pool.map( run_stc , sentence )
	json_list=[]
	for i in p:
		stc_order=i[0]
		stc_map=i[1]
		surfaceText=i[2]
		tmp_stc=[]
		tmp_map={}
		for tok in stc_order:
			tmp_stc.append(tok+'_'+stc_map[tok])
		tmp_map['sentence']=tmp_stc
		tmp_map['surfaceText']=surfaceText
		json_list.append(tmp_map)
	json.dump(json_list,fp_out)

if __name__=='__main__':
    	#relation_list=['CapableOf']
	#relation_list=['HasSubevent','AtLocation','Causes','IsA','Desires']
	relation_list=['MadeOf','SymbolOf','HasFirstSubevent','MotivatedByGoal','UsedFor','HasProperty','NotDesires','CausesDesire']
	for rel in relation_list:
		pos_all(rel)
		pos_all_stc(rel)
