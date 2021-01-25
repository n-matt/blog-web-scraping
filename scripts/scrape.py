import requests
from bs4 import BeautifulSoup
from dateutil import parser
from textstat.textstat import textstat


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/56.0.2924.87 Safari/537.36',
    'referrer': 'https://google.com'
}


def get_author(blog_header):
    if blog_header is not None:
        author = blog_header.find(class_='author-name')
        return author.find('a').contents[0].strip()
    return None


def get_title(blog_header):
    if blog_header is not None:
        title = blog_header.find(class_='post-meta-title')
        print(type(title))
        return title.contents[0].strip()
    return None


def get_read_time(blog_header):
    if blog_header is not None:
        read_time = blog_header.find(class_='read-time')
        return int(read_time.contents[0].strip().lower().split()[0])
    return None


def get_post_date(blog_header):
    if blog_header is not None:
        str_date = parser.parse(blog_header.find(class_='single-post-date post-date small').contents[0].strip())
        return str_date.strftime('%B'), str_date.strftime('%Y'), str_date.strftime('%d')
    return None


def parse_url(url):
    if url is None or url == '':
        return None

    r = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(r.text.strip(), 'lxml')

    header = soup.find(class_='entry-header')
    print(type(header))
    print(dir(header))

    month, year, date, = get_post_date(header)

    body = soup.find(class_='entry-content')

    links = body.find_all("a")

    images = body.find_all('img')

    return {
        'title': get_title(header),
        'author': get_author(header),
        'post_date': date + ' ' + month + ' ' + year,
        'month': month,
        'year': year,
        'day': date,
        'reading_time': get_read_time(header),
        'word_count': len(body.text.strip()),
        'reading_level': textstat.flesch_kincaid_grade(body.text),
        'links_count': len(links),
        'images_count': len(images)
    }


if __name__ == '__main__':
    URL = 'https://blog.frame.io/2018/10/01/womans-experience-cutting-blockbusterrs/'
    print(parse_url(URL))
