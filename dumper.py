from json5 import loads
import os
from leetscrape import GetQuestionsList

def parse(folder, fname):
	with open(f'{folder}/{fname}', 'r') as f:
		data = f.read()
	splitted = data.split('"""')
	front_matter = loads('{\n' + splitted[0].split('= {\n')[1].split('\n}\n')[0] + '\n}')
	md = splitted[1]
	md = '\n'.join(map(lambda line: line.removeprefix(' ' *4), md.split('\n')))

	difficulty_dict = {
		"Easy": "${\\color{green}Easy}$",
		"Medium": "${\\color{orange}Medium}$",
		"Hard": "${\\color{red}Hard}$"
	}
	difficulty = difficulty_dict[front_matter['difficulty']]

	header = f'''
	# {front_matter['qid']}. {front_matter['title']}
	Difficulty: {difficulty} \\
	Tags: {' '.join(front_matter['tags'])}
	\n\n
	'''[1:].replace('\t', '')

	with open(f'{folder}/README.md', 'w') as f:
		f.write(header + md)



ls = GetQuestionsList()
ls.scrape()
questions = ls.questions

START = 0 # of 3338

for q in range(START-1, len(questions)):
	question = questions.loc[q]
	qid = str(question["QID"]).rjust(4, '0')
	title = question["titleSlug"]
	d = f'{qid}_{title}'
	print(d)
	try:
		os.mkdir(d)
	except FileExistsError:
		pass

	res = os.system(f'leetscrape question {qid} -o {d}')
	if res != 0:
		print(f'Error: {res} (QID: {qid})')
		with open('err.log', 'a') as f:
			f.write(f'{qid}: {res}\n')
		os.system(f'rm -rf {d}')
		continue

	os.system(f'mv {d}/q_{qid}_*.py {d}/solve.py')
	os.system(f'mv {d}/test_q_{qid}_*.py {d}/test.py')

	parse(d, 'solve.py')

print('Done')
