from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import textwrap
import csv
import requests
import re
import numpy as np
import pandas as pd
import json
import pprint

REQUEST_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
APP_ID="1064925935909133632"

serch_keyword = '洗濯機' #検索ワード

stop_word = ["福袋","スタンド","収納","バッテリー","フィルター","置き台","ラック","カバー","部品","ケース","容器","マット"] #除外する商品名（動作不安定・適宜追加）

#sort = "-reviewCount" #レビュー件数順
sort = "standard" #楽天標準ソート

serch_params = {
    "format" : "json",
    "keyword" : serch_keyword,
    "applicationId" : [APP_ID],
    "availability" : 0,
    "hits" : 30, #取ってくる商品の数　最大30
    "page" : 1,
    "sort" : sort
}

response = requests.get(REQUEST_URL, serch_params)
result = response.json()

print(type(result))
i_id = result['Items'][0]['Item']['itemCode'] #商品ID
i_image = result['Items'][0]['Item']['mediumImageUrls'][0] #商品画像
i_name = result['Items'][0]['Item']['itemName'] #商品名
i_url = result['Items'][0]['Item']['itemUrl'] #商品ページURL
count = result['Items'][0]['Item']['reviewCount'] #レビュー数

flag = 0
for i in range(100):
    for w in stop_word:
        if w in i_name or count > 10:
            i_id = result['Items'][i+1]['Item']['itemCode']
            i_name = result['Items'][i+1]['Item']['itemName']
            i_image = result['Items'][i+1]['Item']['mediumImageUrls'][0]
            i_url = result['Items'][i+1]['Item']['itemUrl']
            flag = flag + 1
        else:
            flag = 0

    if flag == 0:
        i = 0 #初期化
        break

print(i_url)


#商品ページ　
product_url = "https://item.rakuten.co.jp/kadenrand/516583/?iasid=07rpp_10095___eb-lcycb3p0-7x-a766b221-11c9-4c35-927b-2db7ec34a673"

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
        
        if i == 4:
            break
             

        #次のページ取得
        browser.get(url)

        elem_tag_name = browser.find_elements(By.TAG_NAME, "a") #aタグを全て取得

        elem = []

        for ii in elem_tag_name:
            elem.append(ii.get_attribute('href')) #URLを全て取得

        with open('data.txt', 'w') as f:
            for j in elem:
                f.writelines(str(j)+"\n")
        f.close

        with open('data.txt', 'r') as ff:
            next_url = []
            for line in ff:
                if review_base in line:
                    next_url.append(line) #レビューページにつながるURLを探す
        f.close


        for k in next_url:
            if str(k).endswith('/'+str(num+1)+'.1/\n'): #次の15件のリンクを探す
                next_page = k
                count += 1
        
        if count == 0:
            next_page = [] #次へがなければ終了
        
        
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
    with open('レビューcsv/'+serch_keyword+'.csv','w',encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([i_name])
        writer.writerow([i_url])
        writer.writerow(["id","review"])

        # 全データを表示
        for i in range(len(review_list)):
            csvlist=[]
            review_text = textwrap.fill(review_list[i].text, 500)
            #データ作成
            #csvlist.append('No.{} : '.format(i+1))      #　便宜上「No.XX」の文字列を作成
            csvlist.append(i_id+",")
            csvlist.append(review_text.strip())         #　レビューテキストの先頭・末尾の空白文字を除去
            # 出力    
            writer.writerow(csvlist)                    
        # ファイルクローズ
        f.close()