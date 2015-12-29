from bs4 import BeautifulSoup
import urllib3

def main():
	link = 'https://answers.yahoo.com/dir/index?sid=396545433'
	soup = BeautifulSoup(urllib3.urlopen(link).read())
	
	questions = soup.findAll('h3')
	for question in questions:
		for item in question:
			print(item['href'])
			break
	
	
	print(soup)
	
if __name__ == '__main__':
	main()