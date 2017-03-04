from lxml import html
import requests

dsp_main_page = requests.get('http://uczestnicy.dajsiepoznac.pl/lista')
dsp_tree = html.fromstring(dsp_main_page.content)

github_links = dsp_tree.xpath('.//a[text()="kod"]/@href')

print('There are %d repositories' % len(github_links))

licence_count = {'[EMPTY REPOSITORY]': 0, '[NO LICENCE]': 0}

for link in github_links:
    contestant_page = requests.get(link + '/raw/master/LICENSE')
    if contestant_page.status_code == 404:
        licence_count['[NO LICENCE]'] += 1
        print (link + ': no licence')
    else:
        licence = contestant_page.content.decode('utf8').strip().split('\n')[0].strip()
        if licence == '<!DOCTYPE html>':
            licence_count['[EMPTY REPOSITORY]'] += 1
        elif licence in licence_count:
            licence_count[licence] += 1
        else:
            licence_count[licence] = 1
        print(link + ': ' + licence)

print(licence_count)


