from codecs import namereplace_errors
from flask import Flask, render_template, request, url_for
import brand as br
import pandas as pd
app=Flask(__name__)

#function to remove duplicates
def remove_consec_duplicates(s):
    new_s = ""
    prev = ""
    for c in s:
        if len(new_s) == 0:
            new_s += c
            prev = c
        if c == prev:
            continue
        else:
            new_s += c
            prev = c
    return new_s
@app.route('/')
def hello_world():
    return render_template("index.html")
@app.route("/predict", methods=["GET","POST"])
def brand():
        seed = request.form["seed"]
        membership = request.form["membership"]
        df=pd.read_csv(r'62fdbb2cc8ccc_Brand_name_generator_Data__1_.csv')
        df.dropna(inplace=True)
        df.isna().sum()
        df.drop_duplicates(keep='first', inplace=True)

        # df2.head(2)

        import re
        
        # initialising string
        ini_string = seed

        # function to demonstrate removal of characters
        # which are not numbers and alphabets using re
        getVals = list([val for val in ini_string
                    if val.isalpha()])
        
        result = "".join(getVals)
        seed=result
        
        ctry=list(df['Country'].unique())
        # using stemming to extract the root word to follow the convention according to countries

        from nltk.stem import LancasterStemmer
        ls=LancasterStemmer()
        crw=[]
        dftemp=df[df['Country']==membership]
        for w in dftemp['Drugname']:
            rtw=ls.stem(w)  
            crw.append(rtw)
        country_name=max(crw,key=crw.count)

        # seed=br.generate_names(seed)
        brand_name=br.generate_names(seed+country_name+membership[0:2])[1:]

        if seed and membership:

            # using selenium to automate web browser to check the generated word on IPIndia site


            from selenium import webdriver
            # chrome_driver = webdriver.Chrome('C:\path\to\chromedriver.exe')
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome(ChromeDriverManager().install())
            # webdriver.Chrome(executable_path=r'C:\Desktop\chromedriver.exe')
            from selenium.webdriver.support.ui import Select
            from selenium.webdriver.common.by import By
            from selenium.webdriver.chrome.options import Options
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--no-sandbox')
            # chrome_options.add_argument('--disable-dev-shm-usage')
            # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            # driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
            import time

            driver.get("https://ipindiaonline.gov.in/tmrpublicsearch/frmmain.aspx")
            sel = Select(driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_DDLSearchType']"))
            sel.select_by_visible_text("Phonetic")

            ml=driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_TBPhonetic']")
            x=(brand_name).upper()
            ml.send_keys(x)


            mll=driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_TBClass']")
            mll.send_keys('5')

            driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_BtnSearch']").click()
            newURl = driver.window_handles[0]

            driver.switch_to.window(newURl)
            get_source = driver.page_source
            search_text = x


            # print True if text is present else False
            print(search_text in get_source)

            while search_text in get_source :
                x=br.generate_names(search_text).upper()
                print(search_text)

                driver.get("https://ipindiaonline.gov.in/tmrpublicsearch/frmmain.aspx")
                sel = Select(driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_DDLSearchType']"))
                sel.select_by_visible_text("Phonetic")

                ml=driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_TBPhonetic']")
                search_text=x
                ml.send_keys(x)


                mll=driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_TBClass']")
                mll.send_keys('5')

                driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_BtnSearch']").click()
                newURl = driver.window_handles[0]

                driver.switch_to.window(newURl)
                get_source = driver.page_source
                print(search_text in get_source)

                print(search_text.lower())
            driver.close()

        brand_name=remove_consec_duplicates(brand_name)
        return render_template("index.html",pred="Your brand name - {}".format(brand_name.upper()),text="{}".format("Not found on IpIndia"))


if __name__ == "__main__":
    app.run(debug=True)