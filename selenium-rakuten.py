from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap
import csv
import requests
import re
import time

#windows(chromedriver.exeのパスを設定)
chrome_path = r':C:\Users\Tomoyuki\Documents\chrome'

#mac
#chrome_path = 'C:/Users/デスクトップ/python/selenium_test/chromedriver'

#　amazonのレビュー情報をseleniumで取得する_引数：amazonの商品URL
def get_amazon_page_info(url):
    text = ""                               #　初期化
    options = Options()                     #　オプションを用意
    options.add_argument('--incognito')     #　シークレットモードの設定を付与
    #　chromedriverのパスとパラメータを設定
    driver = webdriver.Chrome(executable_path=chrome_path,options=options)
    driver.get(url)                         #　chromeブラウザでurlを開く
    driver.implicitly_wait(10)              #　指定したドライバの要素が見つかるまでの待ち時間を設定
    text = driver.page_source               #　ページ情報を取得
    
    driver.quit()                           #　chromeブラウザを閉じる
    
    return text                             #　取得したページ情報を返す

# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        rakuten_bs = BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        reviews = rakuten_bs.select('.revRvwUserEntryCmt')          #　ページ内の全レビューのテキストを取得
        
        for review in reviews:                              #　取得したレビュー数分だけ処理を繰り返す
            review_list.append(review)                      #　レビュー情報をreview_listに格納
             
        next_page = rakuten_bs.select('.revPagerSec')         # 「次へ」ボタンの遷移先取得
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = next_page[4].attrs['href']    
            url = next_url  # 次のページのURLをセットする
            
            sleep(5)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list

#インポート時は実行されないように記載
if __name__ == '__main__':
     
    #　商品ページ
    url = 'https://item.rakuten.co.jp/chokyuan/blossom/'

    # URLをレビューページのものに書き換える
    #review_url = url.replace('dp', 'product-reviews')

    #レビューページURLの取得
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    elems = []


    #https://review.rakuten.co.jp　を含むクラスをとってくる
    elems = soup.find_all(href=re.compile("https://review.rakuten.co.jp"))

    i = 1
    while elems == []:
        
        print(str(i)+"回目")
        i += 1
        time.sleep(15)
        elems = soup.find_all(href=re.compile("https://review.rakuten.co.jp"))


    if elems == []:
        print("kara")

    #elemsはリスト型　2つ目のhref属性をもつurlを取得
    review_url = elems[1].attrs["href"]

    # レビュー情報の取得
    review_list = get_all_reviews(review_url)    
 
    #CSVにレビュー情報の書き出し
    #with open('data/sample.csv','w') as f:　#Windowsでエンコードエラーになる場合があるため下の行に変更
    with open('seleniumtest/sample.csv','w',encoding='utf-8') as f:
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