from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import textwrap
import csv
import requests
import re
import time

#商品ページ　
product_url = 'https://item.rakuten.co.jp/nakata/3690/'

#変えなくていい
review_base = "https://review.rakuten.co.jp/item/"



#　amazonのレビュー情報をseleniumで取得する_引数：amazonの商品URL
def get_amazon_page_info(url):
    text = ""                               #　初期化
    #　chromedriverのパスとパラメータを設定
    driver = webdriver.Chrome()
    driver.get(url)                         #　chromeブラウザでurlを開く
    driver.implicitly_wait(10)              #　指定したドライバの要素が見つかるまでの待ち時間を設定
    text = driver.page_source               #　ページ情報を取得
    
    driver.quit()                           #　chromeブラウザを閉じる
    
    return text                             #　取得したページ情報を返す

# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    i = 1                                   #　ループ番号の初期化
    num = 1                                 #レビューページ数の指定
    while True:
        print(i,'page_search')              #　処理状況を表示
        i = i + 1                              #　ループ番号を更新
        count = 0
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        rakuten_bs = BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        reviews = rakuten_bs.select('.revRvwUserEntryCmt')          #　ページ内の全レビューのテキストを取得
        
        for review in reviews:                              #　取得したレビュー数分だけ処理を繰り返す
            review_list.append(review)                      #　レビュー情報をreview_listに格納
             

        #次のページ取得
        browser.get(url)

        elem_tag_name = browser.find_elements(By.TAG_NAME, "a")

        elem = []

        for ii in elem_tag_name:
            elem.append(ii.get_attribute('href'))

        with open('data.txt', 'w') as f:
            for j in elem:
                f.writelines(str(j)+"\n")
        f.close

        with open('data.txt', 'r') as ff:
            next_url = []
            for line in ff:
                if review_base in line:
                    next_url.append(line)
        f.close


        for k in next_url:
            if str(k).endswith('/'+str(num+1)+'.1/\n'):
                next_page = k
                count += 1
        
        if count == 0:
            next_page = []
        
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成    
            url = next_page  # 次のページのURLをセットする
            num = num + 1   #レビューページの番号更新
            
            sleep(5)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list

#インポート時は実行されないように記載
if __name__ == '__main__':

    browser = webdriver.Chrome()
     

    browser.get(product_url)

    elem_tag_name = browser.find_elements(By.TAG_NAME, "a")

    review = "https://review.rakuten.co.jp/item/"

    elem = []

    for i in elem_tag_name:
        elem.append(i.get_attribute("href"))

    with open('data.txt', 'w') as f:
        for j in elem:
            f.writelines(str(j)+"\n")   
    f.close

    with open('data.txt', 'r') as ff:
        review_url = []
        for line in ff:
            if review in line:
                review_url.append(line)
    f.close
    

    # レビュー情報の取得
    review_list = get_all_reviews(review_url[0])    
 
    #CSVにレビュー情報の書き出し
    #with open('data/sample.csv','w') as f:　#Windowsでエンコードエラーになる場合があるため下の行に変更
    with open('sample.csv','w',encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')

        # 全データを表示
        for i in range(len(review_list)):
            csvlist=[]
            review_text = textwrap.fill(review_list[i].text, 500)
            #データ作成
            csvlist.append('No.{} : '.format(i+1))      #　便宜上「No.XX」の文字列を作成
            csvlist.append(review_text.strip())         #　レビューテキストの先頭・末尾の空白文字を除去
            # 出力    
            writer.writerow(csvlist)                    
        # ファイルクローズ
        f.close()