from selenium import webdriver
import selenium
import time
import csv

def run(name):

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=/Users/seisuke/Library/Application Support/Google/Chrome/')

    browser = webdriver.Chrome(options=options)

    csv_file = open('result.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)


    url = 'https://j-net21.smrj.go.jp/snavi/support/'
    #url = 'https://j-net21.smrj.go.jp/snavi/support/40026'
    browser.get(url)
    browser.implicitly_wait(3)
    #time.sleep(3)

    #next_button = browser.find_element_by_xpath('/html/body/div[1]/main/article/div[2]/div[2]/ul[3]/li[2]/a')

    #browser.implicitly_wait(3)

    csv_writer.writerow(['タイトル', '種類', '分野', '地域', '実施機関', 'お知らせ', '募集機関', 'リンク先', 'URL'])

    page = 1
    while True:

        browser.get('https://j-net21.smrj.go.jp/snavi/support?order=DESC&perPage=10&page=' + str(page))
        browser.implicitly_wait(3)

        detail_url_list = get_detail_url_list(browser)
        if len(detail_url_list) == 0:
            break



        for detail_url in detail_url_list:
            browser.get(detail_url)
            browser.implicitly_wait(3)

            title = None
            kind = None
            field = None
            area = None
            institute = None
            content = None
            period = None
            link_url = None
            link_text = None

            try:
                title = browser.find_element_by_xpath('/html/body/div[1]/main/article/h1').text
                kind = browser.find_element_by_xpath('/html/body/div[1]/main/article/section[1]/dl[1]/dd').text
                field = browser.find_element_by_xpath('/html/body/div[1]/main/article/section[1]/dl[2]/dd').text
                area = browser.find_element_by_xpath('/html/body/div[1]/main/article/section[1]/dl[3]/dd').text
                institute = browser.find_element_by_xpath('/html/body/div[1]/main/article/section[1]/dl[4]/dd').text
                content = browser.find_element_by_xpath('/html/body/div[1]/main/article/section[2]/p').text
                link_url = browser.find_element_by_xpath('/html/body/div[1]/main/article/section[3]/ul/li/a').get_attribute('href')
                link_text = browser.find_element_by_xpath('/html/body/div[1]/main/article/section[3]/ul/li/a').text

                print('--------------------')
                print(title)
                print(kind)
                print(field)
                print(area)
                print(institute)
                print(content)
                print(link_url)
                print(link_text)

                # 記載がない可能性があるため最後に取得を試みる
                period = browser.find_element_by_xpath('/html/body/div[1]/main/article/div[1]/dl/dd').text


            except selenium.common.exceptions.NoSuchElementException:
                period = '記載なし'

            data = [title, kind, field, area, institute, content, period, link_text, link_url]
            csv_writer.writerow(data)

        page += 1

    csv_file.close()
    print('終了')

# 1ページに表示されている詳細ページへのURLのリストを取得(最大10件)
def get_detail_url_list(browser):
    detail_url_list = []

    for i in range(10):
        try:
            detail_url = browser.find_element_by_xpath('/html/body/div[1]/main/article/div[2]/ul/li[' + str(i + 1) + ']/div[2]/a').get_attribute('href')
            detail_url_list.append(detail_url)
            # detail_url_list.append(browser.find_element_by_xpath('/html/body/div[1]/main/article/div[2]/ul/li[' + str(i) + ']/div[2]/a').get_attribute('href'))
        except selenium.common.exceptions.NoSuchElementException:
            break

    return detail_url_list








# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
