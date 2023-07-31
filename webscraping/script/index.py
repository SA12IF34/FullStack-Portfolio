import requests
from bs4 import BeautifulSoup


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
p ={
    'http': 'http://35.222.50.197:80',
    'http': 'http://134.209.189.42:80'
}


home = 'https://openlibrary.org'
subjects_page = 'https://openlibrary.org/subjects/'


def get_trending():
    page = requests.get(home+'/').text
    doc = BeautifulSoup(page, 'html.parser')

    trending = doc.find('h2', string="Trending Books").parent.parent.find_all('div', class_='book')

    books = []

    for book in trending:
        img = book.find('img')
        if img and img.has_attr('src') and img.has_attr('title'):
            if img['src'].startswith("data"):
                if img.has_attr('data-lazy'):
                    img_data = img['data-lazy']
            else :
                img_data = img['src']
            
            books.append({'name': img['title'].split(" by ")[0], 'img': img_data})



    return books

def get_subjects():

    page = requests.get(subjects_page).text
    doc = BeautifulSoup(page, 'html.parser')

    subjects_list = doc.find('div', id='subjectsPage').find_all('li')
    subject_names = []
    subject_urls = []

    for subject in subjects_list:

        s = subject.find('a')
        if s.has_attr('href'):
            if 'search?q' not in s['href'] and 'language' not in s['href']:
                subject_names.append(s.string)
                subject_urls.append(s['href'])

    return subject_names, subject_urls

def get_subject(subject):
    link = subjects_page+subject
    
    page = requests.get(link).text
    doc = BeautifulSoup(page, 'html.parser')

    books_list = doc.find('div', class_='contentBody').find_all('div', class_='book')
    books = []

    subject_name = doc.find('div', class_='page-heading-search-box').find('h1', class_='inline').string

    for book in books_list:
        img = book.find('img')
        if img and img.has_attr('src'):
            if img['src'].startswith('data'):
                cover = img['data-lazy']
            else:
                cover = img['src']
            name = img['title'].split(" by ")
            title = name[0]
            author = name[1] 

            books.append({'cover': cover, 'title': title, 'author': author})

    return books, subject_name
