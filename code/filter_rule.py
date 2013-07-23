#-*-coding:utf-8-*-

import json
import csv
import sys

#the template for all filter
def filter_temp(start,end):
	start_wrong=1
	end_wrong=1
	for tok in start:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		#check the pos tag

	for tok in end:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		#check the pos tag
	
	if start_wrong==1 or end_wrong==1:
		return 1
	else:
		return 0

#rule1: no verb in start position
#rule2: no Nc, Nd in start position
#rule3: no non-verb in end position
#rule4: VH13 is adj.
def filter_CapableOf(start,end):
	start_wrong=0
	end_wrong=1
	vt_vi=0 #0: vt, 1:vi
	has_noun=0
	for tok in start:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos[0]=='N':
			has_noun=1
		if vt_vi==1:
			if pos[0]=='N' and (pos[1]!='c' or pos[1]!='d'):
				start_wrong=0
				break
			else:
				vt_vi=0
			break
		if pos=='DM' or pos=='-None-':
			return 0
		if pos[0]=='V' and pos[1]!='H':
			if pos[0:2]=='VC':
				start_wrong=1
				break
			if pos[0:2]=='VA':
				vt_vi=1
				continue
			else:
				start_wrong=1
				continue
		if pos[0:2]=='Nc' or pos[0:2]=='Nd':
			start_wrong=1
			break
	if has_noun==0:
		start_wrong=1
	for tok in end:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return 0
		if pos[0]=='V' and pos[1]!='H':
			end_wrong=0
			break

	if start_wrong==1 or end_wrong==1:
		return 1
	else:
		return 0

def filter_HasProperty(start,end):
	start_wrong=0
	end_wrong=0
	has_verb=0
	has_Nad=0
	for tok in start:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return 0
		
	for tok in end:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos[0]=='V':
			has_verb=1
		if pos=='Nad':
			has_Nad=1
		if pos=='DM' or pos=='-None-':
			return 0
		if pos[0:2]=='Nh':
			end_wrong=1
			break
		if pos[0:2]=='VA' or pos[0:2]=='VH':
			end_wrong=0
			break
	if has_verb==0 and has_Nad==0:
		end_wrong=1

	if start_wrong==1 or end_wrong==1:
		return 1
	else:
		return 0

def filter_HasSubevent(start,end):
	start_wrong=1
	end_wrong=1
	for tok in start:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		if pos[0]=='V' and pos[1]!='H':
			start_wrong=0
			break

	for tok in end:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		if pos[0]=='V' and pos[1]!='H':
			end_wrong=0
			break
	
	if start_wrong==1 or end_wrong==1:
		return 1
	else:
		return 0

#same rule as HasSubevent
def filter_HasFirstSubevent(start,end):
	result=filter_HasSubevent(start,end)
	return result

def filter_AtLocation(start,end):
	start_wrong=1
	end_wrong=1
	for tok in start:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		if pos[0]=='N':
			start_wrong=0
			break

	for tok in end:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		if pos[0]=='N':
			end_wrong=0
			break
	
	if start_wrong==1 or end_wrong==1:
		return 1
	else:
		return 0

#same rule as UsedFor
def filter_CausesDesire(start,end):
	result=filter_UsedFor(start,end)
	return result

def filter_NotDesires(start,end):
	start_wrong=1
	end_wrong=0
	for tok in start:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		if pos[0]=='N':
			start_wrong=0
			break

	for tok in end:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
	
	if start_wrong==1 or end_wrong==1:
		return 1
	else:
		return 0

#same rule as NotDesires
def filter_Desires(start,end):
	result=filter_NotDesires(start,end)
	return result

def filter_UsedFor(start,end):
	start_wrong=1
	end_wrong=1
	for tok in start:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		if pos[0]=='N':
			start_wrong=0
			break

	for tok in end:
		tmp=tok.split('_')
		if len(tmp)==2:
			[word,pos]=tmp
		else:
			[word,pos]=[tmp[0],tmp[1]+'_'+tmp[2]]
		if pos=='DM' or pos=='-None-':
			return -1
		if pos[0]=='V' and pos[1]!='H':
			end_wrong=0
			break

	if start_wrong==1 or end_wrong==1:
		return 1
	else:
		return 0

#same rule as HasSubevent
def filter_Causes(start,end,template):
	result=filter_HasSubevent(start,end)
	return result

#same rule as AtLocation
def filter_PartOf(start,end):
	result=filter_AtLocation(start,end)
	return result

#both noun or both verb
#(AtLocation) (HasSubevent)
def filter_SymbolOf(start,end):
	result1=filter_AtLocation(start,end)
	result2=filter_HasSubevent(start,end)
	if result1==0 or result2==0:
		return 0
	else:
		return 1

#same rule as HasSubevent
def filter_MotivatedByGoal(start,end):
	result=filter_HasSubevent(start,end)
	return result

#same rule as AtLocation
def filter_IsA(start,end):
	result=filter_AtLocation(start,end)
	return result

#same rule as AtLocation
def filter_MadeOf(start,end):
	result=filter_AtLocation(start,end)
	return result

def filter_relation(relation,start,end,template):
	if relation == 'CapableOf':
		result=filter_CapableOf(start,end)
	elif relation == 'HasSubevent':
		result=filter_HasSubevent(start,end)
	elif relation == 'HasProperty':
		result=filter_HasProperty(start,end)
	elif relation == 'AtLocation':
		result=filter_AtLocation(start,end)
	elif relation == 'CausesDesire':
		result=filter_CausesDesire(start,end)
	elif relation == 'NotDesires':
		result=filter_NotDesires(start,end)
	elif relation == 'UsedFor':
		result=filter_UsedFor(start,end)
	elif relation == 'Causes':
		result=filter_Causes(start,end,template)
	elif relation == 'PartOf':
		result=filter_PartOf(start,end)
	elif relation == 'Desires':
		result=filter_Desires(start,end)
	elif relation == 'IsA':
		result=filter_IsA(start,end)
	elif relation == 'HasFirstSubevent':
		result=filter_HasFirstSubevent(start,end)
	elif relation == 'MadeOf':
		result=filter_MadeOf(start,end)
	elif relation == 'SymbolOf':
		result=filter_SymbolOf(start,end)
	elif relation == 'MotivatedByGoal':
		result=filter_MotivatedByGoal(start,end)
	else:
		result=1
	return result
