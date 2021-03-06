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



### 社名取得
def getName(driver):
    #企業情報取得
    kData = driver.find_elements_by_class_name('cassetteRecruit__heading')

    # 企業ループ
    name_list=[]
    for index in range(len(kData)):
        kName=kData[index].find_elements_by_class_name('cassetteRecruit__name')
        name_list.append(kName[0].text)
        
    return name_list

### セールスコピー取得
def getCopy(driver):
    #企業情報取得
    kData = driver.find_elements_by_class_name('cassetteRecruit__heading')

    # 企業ループ
    copy_list=[]
    for index in range(len(kData)):
        copy=kData[index].find_elements_by_class_name('cassetteRecruit__copy')
        copy_list.append(copy[0].text)
        
    return copy_list

### 契約形態取得
def getStatus(driver):
    #企業情報取得
    kData = driver.find_elements_by_class_name('cassetteRecruit__heading')

    # 企業ループ
    status_list=[]
    for index in range(len(kData)):
        status=kData[index].find_elements_by_class_name('labelEmploymentStatus')
        status_list.append(status[0].text)
        
    return status_list

### 年収取得
def getNensyu(driver):
    #テーブル情報取得
    tableData = driver.find_elements_by_class_name('cassetteRecruit__main')

    # 企業ループ
    nensyu_list=[]
    for index in range(len(tableData)):
        head_list=tableData[index].find_elements_by_class_name('tableCondition__head')
        body_list=tableData[index].find_elements_by_class_name('tableCondition__body')

        # テーブル項目ループ
        for head,body in zip(head_list,body_list):
            if head.text=='初年度年収':
                str=body.text
            else:
                str=''
        nensyu_list.append(str)
        
    return nensyu_list



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
    name_list=getName(driver)  #社名
    copy_list=getCopy(driver)   #コピー
    status_list=getStatus(driver) #契約形態
    nensyu_list=getNensyu(driver)  #初年度年収
        
    # 1ページ分繰り返し
    print("{},{},{},{}".format(len(name_list),len(copy_list),len(status_list),len(nensyu_list)))
    for name,copy,status,nensyu in zip(name_list,copy_list,status_list,nensyu_list):
        print(name)
        print(copy)
        print(status)
        print(nensyu)

### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
