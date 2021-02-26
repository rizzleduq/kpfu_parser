from ildar import get_link_from_menu_list_left, gather_name_link_of_employees, gather_name_link_of_cathedras_of_ivmiit
from bs4 import BeautifulSoup

import tools


def gather_name_link_of_cathedras_of_chill(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    uls = soup.find_all('ul', class_='menu_list')
    cathedras = []
    for ul in uls:
        lis = ul.find_all('li')
        for li in lis:
            a = li.find('a')
            if a.text.startswith('Кафедра'):
                cathedras.append((a.text, a.get('href')))
    return cathedras



def parse_chill(link):
    struct_link = get_link_from_menu_list_left(link, 'Структура института')

    cathedras = gather_name_link_of_cathedras_of_chill(struct_link)
    result = {}

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left(link, 'Сотрудники и преподаватели')
        if not stuff_link:
            stuff_link = get_link_from_menu_list_left(link, 'Преподаватели и сотрудники')
        result[name] = stuff_link

    for name, stuff_link in result.items():
        result[name] = gather_name_link_of_employees(stuff_link)

    return result