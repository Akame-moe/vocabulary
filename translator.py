import requests
import time
import glob
import os

def get_secret_key():
	with open('iciba.secret','r') as f:
		k = f.read()
	return k

k = get_secret_key()
query_url = 'http://dict-co.iciba.com/api/dictionary.php'

sess = requests.session()

src_dir = './original'
dest_dir = './generated'

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
	filelist = os.listdir(src_dir)
	for n in filelist:
		d = '{}/{}'.format(dest_dir,n)
		if os.path.exists(d):
			print('exist ',d,',passed.')
			continue
		print('processing ',d)
		lines = []
		with open('{}/{}'.format(src_dir,n),'r',encoding='utf-8') as f:
			lines = f.readlines()
		
		rs = []
		for line in lines:
			line = line.strip()
			if line:
				word,a,b = line.partition(' ')
				if word.startswith('[') or word.startswith('#'):#词根或词缀
					rs.append(word+'\n')
				else:
					time.sleep(0.5)
					r = query(word)
					rs.append('{}{}\n'.format(word.ljust(25),r))
		print('writting',d)
		with open(d,'w',encoding='utf-8') as f:
			f.writelines(rs)
			
if __name__ == '__main__':
	main()
	