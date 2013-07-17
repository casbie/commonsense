#-*-coding:utf-8-*-

#1. load concepts
#2. for relation r, load related concepts
#3. analysis(filter)

import json
from postagger_zh.postagger import POSTagger

def do_pos(text):
	tagger = POSTagger()
	tag_map={}
	for token, tag in tagger.tag(text):
		if token == '。':
			continue
		tag_map[token] = tag
	return tag_map

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

def load_sentence(relation):
	fp=open('relation/'+relation+'.txt','r')
	sentence=[]
	for line in fp:
		tmp=line.strip()
		tmp=tmp.replace('。','')
		#tmp=tmp.replace('[','')
		#tmp=tmp.replace(']','')
		#tmp=tmp.replace(' ','')
		spt=tmp.split(',')
		start=spt[0]
		end=spt[1]
		stc=spt[2]
		sentence.append([unicode(start,'utf-8'),unicode(end,'utf-8'),unicode(stc,'utf-8')])
	return sentence

def filter_HasProperty():
	return

#rule1: no verb in start position
#rule2: no Nc, Nd in start position
#rule3: no non-verb in end position
#rule4: VH13 is adj.
def filter_CapableOf():
	sentence = load_sentence('CapableOf')
	fp_out=open('CapableOf_wrong.txt','w')
	fp_trans=open('CapableOf_to_HasSubevent.txt','w')
	count=0
	for stc in sentence:
		count = count+1
		start_map=do_pos(stc[0])
		end_map=do_pos(stc[1])
		template=stc[2].split(' ')[1]
		start_wrong=0
		end_wrong=1
		start_v=0
		end_v=0
		
		#check start position
		for tok in start_map:
			if start_map[tok][0:2] == 'DM':
				break
			
			if (start_map[tok][0] == 'V' and start_map[tok][1] != 'H'):
				start_v = 1
				start_wrong = 1
				break
			if start_map[tok][0:2] == 'Nc' or start_map[tok][0:2] == 'Nd':
				start_wrong = 1
				break

		#check end position
		for tok in end_map:
			if end_map[tok][0:2] == 'DM':
				break

			if (end_map[tok][0] == 'V' and end_map[tok][1] != 'H'):
				end_v = 1
				end_wrong = 0
				break
		
		if start_v == 1 and end_v == 1:
			for tok in start_map:
				fp_trans.write(tok+'_'+start_map[tok]+',')
			fp_trans.write(template.encode('utf-8')+',')
			for tok in end_map:
				fp_trans.write(tok+'_'+end_map[tok]+',')
			fp_trans.write('\n')

		#if start_wrong == 1 and end_wrong == 1:
		#	for tok in start_map:
		#		fp_out.write(tok+'_'+start_map[tok]+',')
		#	fp_out.write(template.encode('utf-8')+',')
		#	for tok in end_map:
		#		fp_out.write(tok+'_'+end_map[tok]+',')
		#	fp_out.write('\n')

		if count%100==0:
			print count


if __name__=='__main__':
    #conceptNet = load_conceptNet('../conceptnet_json/conceptnet4_zh.json')
	filter_CapableOf()
