#-*-coding:utf-8-*-
import pos_rw

if __name__=='__main__':
    	relation_list=['CapableOf']
	#relation_list=['AtLocation','Causes','HasSubevent','NotDesires','Desires','IsA','PartOf','CapableOf','HasFirstSubevent','MadeOf','SymbolOf','CausesDesire','HasProperty','MotivatedByGoal','UsedFor']
	for rel in relation_list:
		pos_rw.pos_all(rel)
