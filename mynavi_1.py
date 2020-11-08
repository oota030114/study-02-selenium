import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import selenium.webdriver as aa

### Chromeを起動する関数
def set_driver(driver_path,headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）の設定
    if headless_flg==True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    #options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')    # 証明書警告画面を回避
    options.add_argument('--ignore-ssl-errors')    # SSLエラー画面を回避
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。(chromedriver.exeのパスにPythonソースのパスを使用)
    return Chrome(executable_path=os.getcwd() + "\\" + driver_path,options=options)

### 年収取得
def getNensyu(driver):

    str=''
    kInfo = driver.find_elements_by_class_name('cassetteRecruit__main')
    index=0
    # 企業ループ
    while index < len(kInfo):
        cnt=0
        # テーブル項目ループ
        while cnt < len(kInfo[index].find_elements_by_class_name('tableCondition__head')):
            hNensyu=kInfo[index].find_elements_by_class_name('tableCondition__head')
            kInfo=kInfo[index].find_elements_by_class_name('tableCondition__body')
            if hNensyu[4]=='初年度年収':
                str=kInfo[4]
            else:
                str=''
            rnensyuet.append(str)

    # elem21 = elem1[0].find_elements_by_class_name('tableCondition__head')
    # elem22 = elem1[0].find_elements_by_class_name('tableCondition__body')
    # print("elem1[0].text=", elem1[0].text)
    # print("elem21[4].text=", elem21[4].text)  # 初年度年収
    # print("elem22[4].text=", elem22[4].text)  # 初年度年収

    return ret



### main処理
def main():
    search_keyword="高収入"
    # driverを起動
    driver=set_driver("chromedriver.exe",False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(2)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    

    # 検索結果の一番上の会社名を取得
    name_list=driver.find_elements_by_class_name("cassetteRecruit__name")   #社名
    copy_list=driver.find_elements_by_class_name("cassetteRecruit__copy")   #タイトル
    status_list=driver.find_elements_by_class_name("labelEmploymentStatus") #契約形態

    #年収取得
    nensyu_list=[]
    kInfo = driver.find_elements_by_class_name('cassetteRecruit__main')

    # 企業ループ
    for index in  range(len(kInfo)):
        head=kInfo[index].find_elements_by_class_name('tableCondition__head')
        body=kInfo[index].find_elements_by_class_name('tableCondition__body')

        # テーブル項目ループ
        for cnt in range(len(kInfo[index].find_elements_by_class_name('tableCondition__head'))):
            if head[cnt].text=='初年度年収':
                str=body[cnt].text
            else:
                str=''
        nensyu_list.append(str)
        
    # 1ページ分繰り返し
    print("{},{},{},{}".format(len(copy_list),len(status_list),len(name_list),len(nensyu_list)))
    for name,copy,status,nensyu in zip(name_list,copy_list,status_list,nensyu_list):
        print(name.text)
        print(copy.text)
        print(status.text)
        print(nensyu)


### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
