import requests
from bs4 import BeautifulSoup
import json
url = 'https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&text=python&enable_snippets=false&L_save_area=true'
keywords = ['Django', 'Flask']
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    vacancies = soup.find_all(class_='vacancy-serp-item')
    results = []
    for vacancy in vacancies:
        link = vacancy.find('a', class_='bloko-link')['href']
        company = vacancy.find('a', class_='bloko-link').text
        city = vacancy.find(class_='vacancy-serp-item__meta-info').text
        salary = vacancy.find(class_='vacancy-serp-item__compensation')
        if salary:
            salary = salary.text.strip()
        else:
            salary = 'Не указана'
        description = vacancy.find(class_='g-user-content').text
        if any(keyword.lower() in description.lower() for keyword in keywords):
            vacancy_info = {
                'link': link,
                'company': company,
                'city': city,
                'salary': salary
            }
            results.append(vacancy_info)

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print('Парсинг завершен. Результаты сохранены в файле vacancies.json.')
else:
    print('Ошибка при выполнении запроса.')