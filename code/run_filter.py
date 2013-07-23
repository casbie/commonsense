#-*-coding:utf-8-*-

import filter_rule as rule
import pos_rw
import sys

def filter_all(wrong,rows,relation):
        filter_rows=[]
	for data in rows:
		result=1
                result=rule.filter_relation(relation,data['start'],data['end'])
		if result == wrong:
			filter_rows.append(data)
	return filter_rows

if __name__=='__main__':
	relation=sys.argv[1]
	wrong=sys.argv[2] #0: correct data; 1:wrong data
	rows=pos_rw.load_json_file(relation)
	filter_rows=filter_all(wrong,rows,relation)

	#do some analysis of the filtered data or just dump them
	pos_rw.dump_file( relation , pos_rw.print_format(filter_rows) )

