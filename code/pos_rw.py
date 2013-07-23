#-*-coding:utf-8-*-

import json
from postagger_zh.postagger import POSTagger
import multiprocessing
import csv

#input: text
#output: the result of pos, the order of segmentation
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
	fp=open('../relation/'+relation+'_test.txt','r')
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

#The following two methods is doing the POS for the start and end parts seperately.
#pos_all: deal with all sentences for given relation
#run: for parallel purpose
def run(stc):
	start=stc[0]
	end=stc[1]
	surfaceText=stc[2].replace('[','').replace(']','').replace(' ','')
	
	[start_map, start_order]=do_pos(start)
	[end_map, end_order]=do_pos(end)
	[stc_map,stc_order]=do_pos(surfaceText)
	
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

	print stc[0]
	return [start_order, end_order, stc_order, start_map, end_map, stc_map, template, surfaceText]

def pos_all(relation):
	sentence = load_sentence(relation)
	fp_out=open('../output/'+relation+'_pos.txt','w')
	pool = multiprocessing.Pool(10)
	p = pool.map( run , sentence )
	json_list=[]
	for i in p:
		start_order=i[0]
		end_order=i[1]
		stc_order=i[2]
		start_map=i[3]
		end_map=i[4]
		stc_map=i[5]
		template=i[6]
		surfaceText=i[7]
		tmp_map={}
		tmp_start=[]
		tmp_end=[]
		tmp_stc=[]
		tmp_template=''
		for tok in start_order:
			tmp_start.append(tok+'_'+start_map[tok])
		tmp_map['start']=tmp_start
		for tok in end_order:
			tmp_end.append(tok+'_'+end_map[tok])
		tmp_map['end']=tmp_end
		for tok in stc_order:
			tmp_stc.append(tok+'_'+stc_map[tok])
		for i in template:
			tmp_template=tmp_template+i
		tmp_map['sentence']=tmp_stc
		tmp_map['template']=tmp_template
		tmp_map['surfaceText']=surfaceText
		json_list.append(tmp_map)
	json.dump(json_list,fp_out)

#load_json_file: read the pos result(in json format)
#input: given relation
#output: the tag map of data {start,end,sentence,template,surfaceText}
#	start: pos of start part; 
#	end: pos of end part;
#	sentence: pos of the whole sentence
def load_json_file(relation):
        fp_in=open('../output/'+relation+'_pos.txt')
        json_file=json.load(fp_in)
        return json_file

def print_format(rows_json):
	rows=[]
        for data in rows_json:
		row=[]
		for tok in data['start']:
                        row.append(tok.encode('utf-8'))
                row.append(data['template'].encode('utf-8'))
                for tok in data['end']:
                        row.append(tok.encode('utf-8'))
                rows.append(row)
	return rows

#dump_file: dump the data into csv file
#input: relation, rows(data, maybe filtered)
def dump_file(relation,rows):
        fp_out=open('../output/'+relation+'_filter.txt','w')
        file_writer=csv.writer(fp_out)
        for row in rows:
                file_writer.writerow(row)
