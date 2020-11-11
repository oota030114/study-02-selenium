import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import selenium.webdriver as aa
import pandas as pd
import logging
from _stat import filemode

fmt='[%(asctime)s]  %(filename)s(%(lineno)d): %(message)s'
DISCONNECTED_MSG = 'Unable to evaluate script: disconnected: not connected to DevTools\n'

logging.basicConfig(
    filename='mynavi.log',			# ログファイル名
    filemode='w', 					# w：上書き a：追記
    format=fmt		, 				# 出力フォーマット
    datefmt='%Y-%m-%d %H:%M:%S', 	# 日付フォーマット
    level=logging.INFO)			    # INFO以上を出力

### Chromeを起動する関数
def set_driver(driver_path,headless_flg):
    try:
        # Chromeドライバーの読み込み
        options = ChromeOptions()

        # ヘッドレスモード（画面非表示モード）の設定
        if headless_flg==True:
            options.add_argument('--headless')

        # 起動オプションの設定
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        #options.add_argument('log-level=3')
        options.add_argument('--ignore-certificate-errors')     # 証明書警告画面を回避
        options.add_argument('--ignore-ssl-errors')             # SSLエラー画面を回避
        options.add_argument('--incognito')                     # シークレットモードの設定を付与
    except:
        print('error:set_driver')
        return

    # ChromeのWebDriverオブジェクトを作成する。(chromedriver.exeのパスにPythonソースのパスを使用)
    return Chrome(executable_path=os.getcwd() + "\\" + driver_path,options=options)

### 社名取得
def getName(driver):
    try:
        #企業情報取得
        kData = driver.find_elements_by_class_name('cassetteRecruit__heading')

        # 企業ループ
        name_list=[]
        cnt=1
        for index in range(len(kData)):
            kName=kData[index].find_elements_by_class_name('cassetteRecruit__name')
            name_list.append(kName[0].text)
            logging.info('社名 ' + str(cnt) + '件目取得')
            cnt = cnt + 1
    except:
        print('社名取得エラー {}件目'.format(str(cnt)))
        logging.error('社名取得エラー {}件目'.format(str(cnt)))
    finally:
        return name_list

### コピー取得
def getCopy(driver):
    try:
        #企業情報取得
        kData = driver.find_elements_by_class_name('cassetteRecruit__heading')

        # 企業ループ
        copy_list=[]
        cnt=1
        for index in range(len(kData)):
            copy=kData[index].find_elements_by_class_name('cassetteRecruit__copy a')
            copy_list.append(copy[0].text)
            logging.info('コピー ' + str(cnt) + '件目取得')
            cnt = cnt + 1
    except:
        print('コピー取得エラー {}件目'.format(str(cnt)))
        logging.error('コピー取得エラー {}件目'.format(str(cnt)))
    finally:
        return copy_list

### 契約形態取得
def getStatus(driver):
    try:
        #企業情報取得
        kData = driver.find_elements_by_class_name('cassetteRecruit__heading')

        # 企業ループ
        status_list=[]
        cnt=1
        for index in range(len(kData)):
            status=kData[index].find_elements_by_class_name('labelEmploymentStatus')
            status_list.append(status[0].text)
            logging.info('契約形態 ' + str(cnt) + '件目取得')
            cnt = cnt + 1
    except:
        print('契約形態取得エラー {}件目'.format(str(cnt)))
        logging.error('契約形態取得エラー {}件目'.format(str(cnt)))
    finally:
        return status_list

### 応募条件取得
def getZyoken(driver):
    try:
        #応募条件取得
        zData = driver.find_elements_by_class_name('cassetteRecruit__attribute')
        # 企業ループ
        zyoken_list=[]
        cnt=1
        for index in range(len(zData)):
            zyoken=zData[index].find_elements_by_class_name('labelCondition')
            strZyoken=''
            for data in zyoken:
                if strZyoken == '':
                    strZyoken = data.text
                else:
                    strZyoken = strZyoken + " " + data.text
            zyoken_list.append(strZyoken)
            logging.info('応募条件 {}件目取得'.format(str(cnt)))
            cnt = cnt + 1
    except:
        print('応募条件取得エラー {}件目'.format(str(cnt)))
        logging.error('応募条件取得エラー {}件目'.format(str(cnt)))
    finally:
        return zyoken_list


### テーブル情報取得
def getTable(driver,colName):
    try:
        #テーブル情報取得
        tableData = driver.find_elements_by_css_selector('div[class^="cassetteRecruit__main"]')
        # ループ：企業
        table_list=[]
        cnt=1
        for index in range(len(tableData)):
            head_list=tableData[index].find_elements_by_class_name('tableCondition__head')
            body_list=tableData[index].find_elements_by_class_name('tableCondition__body')
            # ループ：テーブル項目
            strZyoken=''
            for head,body in zip(head_list,body_list):
                if head.text==colName:
                    strZyoken=body.text
            table_list.append(strZyoken)
            logging.info(colName + ' ' + str(cnt) + '件目取得')
            cnt = cnt + 1
    except Exception:
        print('{}取得エラー}'.format(colName))
        logging.error('getTable colName=' + colName)
    else:
        return table_list


def outFirstPage(driver, search_keyword):
    try:
        # Webサイトを開く
        driver.get("https://tenshoku.mynavi.jp/")
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(2)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        # 検索窓に入力
        driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword.strip())
        # 検索ボタンクリック
        driver.find_element_by_class_name("topSearch__button").click()

        # 検索結果を取得
        name_list=getName(driver)       #社名
        copy_list=getCopy(driver)       #コピー
        status_list=getStatus(driver)   #契約形態
        zyoken_list=getZyoken(driver)   #応募条件
        work_list=getTable(driver,'仕事内容')
        taisyo_list=getTable(driver,'対象となる方')
        kinmu_list=getTable(driver,'勤務地')
        kyuyo_list=getTable(driver,'給与')
        nensyu_list=getTable(driver,'初年度年収')

        # CSV ファイル出力
        csvData=[]
        csvData={"社名":name_list,"コピー":copy_list,"契約形態":status_list,"応募条件":zyoken_list,"仕事内容":work_list,"対象となる方":taisyo_list,"勤務地":kinmu_list,"給与":kyuyo_list,"初年度年収":nensyu_list}
        df = pd.DataFrame(csvData)
        df.to_csv("mynavi.csv", index=False)
    except Exception:
        return False
    else:
        return True

def outNextPage(driver, url):
    try:
        # Webサイトを開く
        driver.get(url)
        time.sleep(10)

        # 検索結果を取得
        name_list=getName(driver)       #社名
        copy_list=getCopy(driver)       #コピー
        status_list=getStatus(driver)   #契約形態
        zyoken_list=getZyoken(driver)   #応募条件

        work_list=getTable(driver,'仕事内容')
        taisyo_list=getTable(driver,'対象となる方')
        kinmu_list=getTable(driver,'勤務地')
        kyuyo_list=getTable(driver,'給与')
        nensyu_list=getTable(driver,'初年度年収')

        # CSV ファイル出力
        csvData=[]
        csvData={"社名":name_list,"コピー":copy_list,"契約形態":status_list,"応募条件":zyoken_list,"仕事内容":work_list,"対象となる方":taisyo_list,"勤務地":kinmu_list,"給与":kyuyo_list,"初年度年収":nensyu_list}
        df = pd.DataFrame(csvData)
        df.to_csv("mynavi.csv", index=False, mode='a')
    except Exception:
        return False
    else:
        return True
    
### main処理
def main():
    try:
        logging.info('main 処理開始')
        
        # 検索キーワード入力
        keyWord = input('検索キーワードを入力してください: ')
        
        print('main 開始')

        # driverを起動
        driver=set_driver("chromedriver.exe",False)

        # 検索結果出力（先頭ページ）
        logging.info('main 先頭ページ 出力開始')
        pageCnt=1
        logging.info('outFirstPage {} ページ目の出力開始'.format(str(pageCnt)))
        if outFirstPage(driver, keyWord):
            logging.info('outFirstPage {} ページ目の出力終了'.format(str(pageCnt)))
        else:
            logging.info('outFirstPage {} ページ目で出力エラー'.format(str(pageCnt)))

        # 検索結果出力（次ページ）
        while True:
            if driver.find_elements_by_class_name('iconFont--arrowLeft'):
                element=driver.find_element_by_class_name('iconFont--arrowLeft')
                url=element.get_attribute("href")
                pageCnt=pageCnt+1
                logging.info('outNextPage {} ページ目の出力開始'.format(str(pageCnt)))
                if outNextPage(driver, url):
                    logging.info('outNextPage {} ページ目の出力終了'.format(str(pageCnt)))
                else:
                    logging.info('outNextPage {} ページ目で出力エラー'.format(str(pageCnt)))
            else:
                break
    except Exception as e:
        if driver.get_log('driver')[-1]['message'] == DISCONNECTED_MSG:
            print('Browser window closed by user')
            logging.error('main Browser window closed by user')
        print('main 異常終了')
        logging.info('main 異常終了')
    else:
        driver.close()
        print('main 正常終了')
        logging.info('main 正常終了')
        
    

### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
