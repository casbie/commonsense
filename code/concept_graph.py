#-*- coding: utf-8 -*-
import json
import networkx as nx
#import matplotlib.pyplot as plt

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

def edge_set(concept_rel):
    edge_list=[]
    for rec in concept_rel:
        rel=rec[0]
        start=unicode(rec[1],'utf-8')
        end=unicode(rec[2], 'utf-8')
        edge=(start, end, {'relation':rel})
        edge_list.append(edge)
    return edge_list

def filter_subNet(concept1, concept2, forward_table, backward_table):
    subNet=[]
    two_layer=[]
    #check sub_graph of concept1 for forward direction
    con_list=forward_table[concept1]
    for assr in con_list:
        if assr[2] in forward_table:
            tmp_list=forward_table[assr[2]]
            for tmp in tmp_list:
                if concept2 == tmp[2]:
                    subNet.append(concept1)
		    subNet.append(assr[2])
		    subNet.append(concept2)
		    two_layer.append(assr)
		    two_layer.append(tmp)
	if assr[2] in backward_table:
            tmp_list=backward_table[assr[2]]
            for tmp in tmp_list:
                if concept2 == tmp[1] and tmp[1]!=concept1:
                    subNet.append(concept1)
                    subNet.append(assr[2])
		    subNet.append(concept2)
		    two_layer.append(assr)
		    two_layer.append(tmp)
    #check sub_graph of concept1 for backward direction
    con_list=backward_table[concept1]
    for assr in con_list:
        if assr[1] in forward_table:
            tmp_list=forward_table[assr[1]]
            for tmp in tmp_list:
                if concept2 == tmp[2]:
                    subNet.append(concept1)
		    subNet.append(assr[1])
		    subNet.append(concept2)
		    two_layer.append(assr)
		    two_layer.append(tmp)
	if assr[1] in backward_table:
            tmp_list=backward_table[assr[1]]
            for tmp in tmp_list:
                if concept2 == tmp[1] and tmp[1]!=concept1:
                    subNet.append(concept1)
                    subNet.append(assr[1])
		    subNet.append(concept2)
		    two_layer.append(assr)
		    two_layer.append(tmp)
    seen=set()
    subNet=[x for x in subNet if x not in seen and not seen.add(x)]
    seen=[]
    two_layer=[x for x in two_layer if x not in seen and not seen.append(x)]
    return subNet,two_layer

def set_link_table(conceptNet):
    forward_table={}
    backward_table={}
    for assr in conceptNet:
        start=assr[1]
        end=assr[2]
        
        if start not in forward_table:
            forward_table[start]=[assr]
        else:
            forward_table[start].append(assr)
        
        if end not in backward_table:
            backward_table[end]=[assr]
        else:
            backward_table[end].append(assr)

    return (forward_table, backward_table)

def create_network(edges):
    DG=nx.DiGraph()
    DG.add_edges_from(edges)
    #nx.draw(DG)
    pos=nx.spring_layout(DG)
    nx.draw_networkx_nodes(DG, pos, nodesize=5000)
    nx.draw_networkx_edges(DG, pos)
    nx.draw_networkx_labels(DG, pos, fontsize=8)
    nx.draw_networkx_edge_labels(DG, pos)
    plt.savefig("graph.png")
    plt.axis('off')
    plt.savefig("graph.png", dpi=1000)
    plt.show()
    
def create_net(subNet, two_layer):
    fp_g=open('../graph_output/graph_reault.txt','w')
    fp_t=open('../graph_output/text_reault.txt','w')
    for rec in subNet:
	fp_g.write('"'+rec+'",')

    fp_g.write('\n')
    for rec in two_layer:
	fp_g.write('['+str(subNet.index(rec[1]))+','+str(subNet.index(rec[2]))+',"'+rec[0]+'"],')
	fp_t.write(rec[0]+' '+rec[1]+' '+rec[2]+'\n')
    
def add_link(subNet,two_layer,forward_table,backward_table):
    new_two_layer=[]
    for word in subNet:
	tmp_list=forward_table[word]
	for tmp in tmp_list:
	    if tmp[2] in subNet:
		new_two_layer.append(tmp)
	tmp_list=backward_table[word]
	for tmp in tmp_list:
	    if tmp[1] in subNet:
		new_two_layer.append(tmp)
    two_layer=two_layer+new_two_layer
    seen=[]
    two_layer=[x for x in two_layer if x not in seen and not seen.append(x)]
    return two_layer

if __name__=='__main__':
    concept1='學校'
    concept2='考試'
    
    conceptNet=load_conceptNet('../conceptnet_json/conceptnet4_zh.json')
    (forward_table, backward_table)=set_link_table(conceptNet)
    (subNet,two_layer)=filter_subNet(concept1,concept2,forward_table,backward_table)
    two_layer=add_link(subNet,two_layer,forward_table,backward_table)
    #edges=edge_set(subNet)
    #create_network(edges)
    create_net(subNet,two_layer)
