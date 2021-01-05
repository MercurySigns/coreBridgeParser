import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import pandas as pd

load_dotenv('secrets.env')


chrome_options = webdriver.ChromeOptions()

driver=webdriver.Chrome(chrome_options=chrome_options)

def init(cbURL, d1, d2):
    driver.get("https://mercurysigns.corebridge.net/Login.aspx")
    user = driver.find_element_by_id('txtUsername')
    pas = driver.find_element_by_id('txtPassword')

    user.send_keys(os.getenv('COREBRIDGE_USERNAME'))
    pas.send_keys(os.getenv('COREBRIDGE_PASSWORD'))

    driver.find_element_by_id('btnLogin').click()

    driver.get(cbURL)

    select = Select(driver.find_element_by_id('rvMainReportView_ctl08_ctl03_ddValue'))
    select.select_by_visible_text('Free Date Range')


    WebDriverWait(driver,20).until(EC.invisibility_of_element((By.ID,'rvMainReportView_AsyncWait_Wait')))

    script = """
        document.getElementById('rvMainReportView_ctl08_ctl07_txtValue').value = '{}';
        document.getElementById('rvMainReportView_ctl08_ctl09_txtValue').value = '{}';
    """.format(d1,d2)

    driver.execute_script(script)

    script2 = """
    for(i=0;i<document.getElementById('rvMainReportView_ctl08_ctl11_ddValue').options.length;i++){
    if(document.getElementById('rvMainReportView_ctl08_ctl11_ddValue').options[i].innerHTML.replace('&nbsp;',' ') == 'Created Date'){
        document.getElementById('rvMainReportView_ctl08_ctl11_ddValue').selectedIndex = i
        console.log(i)
        }
    }
    """

    driver.execute_script(script2)

    driver.find_element_by_id('rvMainReportView_ctl08_ctl00').click()

    WebDriverWait(driver,20).until(EC.invisibility_of_element((By.ID,'rvMainReportView_AsyncWait_Wait')))

    script3 = """
        document.getElementById('rvMainReportView_ctl09_ctl00_Last_ctl00_ctl00').click();
        console.log('ran');
    """

    time.sleep(2)

    driver.execute_script(script3)

    WebDriverWait(driver,20).until(EC.invisibility_of_element((By.ID,'rvMainReportView_AsyncWait_Wait')))

    script4 = """
        document.getElementById('rvMainReportView_ctl09_ctl00_First_ctl00_ctl00').click();
        console.log('went back to first');
    """

    time.sleep(2)
    
    driver.execute_script(script4)

    tList = []
    script5 = """
        document.getElementById('rvMainReportView_ctl09_ctl00_Next_ctl00_ctl00').click();
        console.log('next');
    """

    for i in range(int(driver.find_element_by_id('rvMainReportView_ctl09_ctl00_TotalPages').get_attribute('innerHTML'))):
        
        table = driver.find_element_by_xpath('//div[@id="rvMainReportView_ctl13"]/div/div/table/tbody/tr/td/table/tbody/tr/td/table').get_attribute('outerHTML')
        
        tList.append(table)

    driver.quit()
    df = pd.DataFrame()

    nList = []
    for i in tList:
        x = pd.read_html(i)
        y = x[1]
        nList.append(y)



    print(pd.concat(nList))


init("https://mercurysigns.corebridge.net/ReportModule/ReportPages/GenericReportViewerPage.aspx?ReportName=InvoiceSummaryForExport&ReportTypeId=1009", "1/12/2020", "2/12/2021")