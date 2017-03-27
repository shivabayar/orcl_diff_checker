'''
	This monster eats two files containing oracle schemas and 
	shits the difference in columns between two schemas.
	That's all folks :p haha just kidding

	The script expects that each table's schema
	is in one single line with a semicolon at the end exactly like the example 
	eg: CREATE TABLE "ACCOUNT_BALANCE"     (	"COMPANY" VARCHAR2(5 BYTE),  	"COSTCENTRECODE" VARCHAR2(10 BYTE),  	"SUBCOSTCENTRECODE" VARCHAR2(10 BYTE),  	"PARTYID" NUMBER,  	"PARTYSUBACCOUNT" NUMBER,  	"ACCOUNTCATEGORY" VARCHAR2(5 BYTE),  	"ACCOUNTSUBCATEGORYCODE" VARCHAR2(5 BYTE),  	"CURRENCY" VARCHAR2(3 BYTE),  	"BUSINESSDATE" TIMESTAMP (6),  	"VALUEDATEBALANCE" NUMBER,  	"UNCLEARCHEQUEBALANCE" NUMBER,  	"HOLDFUNDBALANCE" NUMBER,  	"LSTUPDDTETME" TIMESTAMP (6),  	"EARMARKBALANCE" NUMBER    ) ;
'''

import sys
import re

		
def convert_to_obj(table):
	full_pattern = r'^(\s+)([aA-zZ]+\s[aA-zZ]+)\s\"(([aA-zZ]+\_|[aA-zZ]+)+)\"\s+(\(.*\))\s+\;$'
	col_pat = r'.*"(.*)"(.*)'
	total_result = re.compile(full_pattern).match(table)
	col_comp = re.compile(col_pat)

	if total_result:
		table_name = re.sub(r"\s+", "", total_result.group(3))
		table_name = table_name.lower()
		cols = str(total_result.group(5)).split(',')
		final_cols = list()
		for col in cols:
			res = col_comp.match(col)
			if res:
				tup = (res.group(1).lower(), re.sub(r"\s+", "",res.group(2)).lower())
				final_cols.append(tup)

		table_obj = {'name': table_name, 'property':final_cols}

		return table_obj


if __name__ == '__main__':
	print "Starting...."
	try:
		file1 = open(sys.argv[1], "r+")
		file2 = open(sys.argv[2], "r+")
		lines1 = file1.readlines()
		lines2 = file2.readlines()

		original_sql = dict()
		new_sql = dict()

		for line in lines1:
			temp = convert_to_obj(line)
			if temp:
				original_sql.__setitem__(temp['name'], {'property': temp['property'], 'create_stat': line})

		for line in lines2:
			temp = convert_to_obj(line)
			if temp:
				new_sql.__setitem__(temp['name'], {'property': temp['property'], 'create_stat': line})

		for key in original_sql.keys():
			
			if new_sql.has_key(key):
				new_cols = [str(k[0]+" "+k[1]).replace('byte','') for k in new_sql[key]['property']]
				original_cols = [str(k[0]+" "+k[1]).replace('byte','') for k in original_sql[key]['property']]
				diff_cols = set(new_cols) - set(original_cols)
				if diff_cols:
					for i in diff_cols:
						print "alter table " + key + " add (" + i + " );"

	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass
