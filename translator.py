import requests
import time
import glob

def get_secret_key():
	with open('iciba.secret','r') as f:
		k = f.read()
	return k

k = get_secret_key()
query_url = 'http://dict-co.iciba.com/api/dictionary.php'

sess = requests.session()
def query(word):
	p = {'w':word,'key':k,'type':'json'}
	print('querying:',word)
	try:
		r = sess.get(query_url,params=p)
		if r and r.ok:
			parts = r.json()['symbols'][0]['parts']
			return '    '.join(['#{}{}'.format(x['part'],str(x['means'])) for x in parts])
	except:
		pass
	return 'ERROR->' + word

		
def test():
	print(query('forbidden'))
		
def main():
	filelist = ['{}.part.txt'.format(x) for x in range(1,8)]
	for n in filelist:
		lines = []
		with open(n,'r',encoding='utf-8') as f:
			lines = f.readlines()
		
		rs = []
		for line in lines:
			line = line.strip()
			if line:
				ss = line.split()
				word = ss[0]
				if word.startswith('['):#词根或词缀
					rs.append(word+'\n')
				else:
					time.sleep(0.5)
					r = query(word)
					rs.append('{}{}\n'.format(word.ljust(25),r))
		with open('x-{}'.format(n),'w',encoding='utf-8') as f:
			f.writelines(rs)
			
if __name__ == '__main__':
	main()
	