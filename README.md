commonsense
===========
##main files:
* pos_all.py: do POS for all relations
  * usage: python pos_all.py
* run_filter.py: filter the data with POS tag for given relation
  * usage: python run_filter.py relation_name correct_or_wrong
  * correct_or_wrong: 0 --> correct; 1 --> wrong, (default wrong)

##method files:
* pos_rw.py: some methods for read data, write data, do POS(used for pos_all, run_filter)
* filter_rule: filter data for all relation(used for run_filter)
