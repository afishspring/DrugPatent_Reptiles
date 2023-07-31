from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from Reptiles import Reptiles_XHR, Reptiles_DOM
import json
import time
import re


class DrugPatent_Info_Reptiles(Reptiles_XHR):
    def __init__(self, website, next_page_xpath="", bar_xpath="", bar_child_tag_name="", n_page_offset=0, total_num_xpath="",
                 xhr_pattern="page", tab_xpath=""):
        super(DrugPatent_Info_Reptiles, self).__init__(website, next_page_xpath, bar_xpath, bar_child_tag_name, n_page_offset, total_num_xpath, xhr_pattern)
        self.tab_path = tab_xpath
    def start(self):
        self.openWebSite(self.website)
        self.selectTab()
        self.data = self.collectData()
        self.data = self.data.explode(['权利要求编号', '备注'])
        self.data = self.data.explode('专利权人')
        print(self.data)
        self.br.quit()
    def selectTab(self):
        self.br.find_element(By.XPATH, self.tab_path).click()
    def getDetail(self):
        rows_of_page = len(self.br.find_elements(By.XPATH, "//span[contains(text(),'查 看')]"))
        rows_of_lastpage = self.getTotalNum() % rows_of_page
        n_page = self.getTotalNum() / rows_of_page
        real_rows = rows_of_page if self.curr_page < n_page else rows_of_lastpage
        print(real_rows)
        for index in range(1, real_rows+1):
            while(True):
                try:
                    deep1 = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[7]/div[1]/button[1]")
                except exceptions.NoSuchElementException:
                    continue
                else:
                    break
            self.br.execute_script("arguments[0].click()", deep1)
            while (True):
                try:
                    deep2 = self.br.find_element(By.XPATH, "//tbody/tr[1]/td[6]/div[1]/button[1]")
                except exceptions.NoSuchElementException:
                    continue
                else:
                    break
            self.br.execute_script("arguments[0].click()", deep2)
            time.sleep(0.1)
            back2 = self.br.find_element(By.XPATH, "//body/div[3]/div[1]/div[3]/span[1]/button[1]")
            self.br.execute_script("arguments[0].click()", back2)
            back1 = self.br.find_element(By.XPATH,
                                         "/html[1]/body[1]/div[1]/div[1]/section[1]/div[1]/div[6]/div[1]/div[1]/div[3]/span[1]/button[1]")
            self.br.execute_script("arguments[0].click()", back1)


    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data['zlInfoList'])
        data_json = []
        for index in range(0, patent_info_cnt):
            grant_drug_relation = data['zlInfoList'][index]['zldjDygxList']
            grant_index = []
            grant_note = []
            for grant in grant_drug_relation:
                grant_index.append(grant['qlyqxbh'])
                grant_note.append(grant.get('bz', ''))
            data_json.append({
                '批准文号/注册证号': data['main']['pzwh'],
                '药品名称': data['main']['ypmc'],
                '上市许可持有人': data['main']['ypsscyr'],
                '剂型': data['main']['ypjx'],
                '规格': data['main']['ypgg'],
                '药品类型': data['main']['yplx'],
                '专利号': data['zlInfoList'][index]['zlh'],
                '专利名称': data['zlInfoList'][index]['zlmc'],
                '专利权人': re.split(r"[；，、;,/|]", data['zlInfoList'][index]['zlqr']),
                '专利被许可人': data['zlInfoList'][index].get('zlbxkr',''),
                '授权日期': data['zlInfoList'][index]['zlsxr'],
                '权利要求编号': grant_index,
                '备注': grant_note,
                '创建时间': data['main']['cjsj']
            })
        return data_json

class DrugPatent_Cite_Reptiles(Reptiles_DOM):
    def start(self):
        self.openWebSite(self.website)
        self.data = self.collectData()
        self.data = self.data.explode(['登录的专利号', '登录的权利要求项编号', '专利声明类型', '备注'])
        print(self.data)
        self.br.quit()
    def getTuple(self, index):
        data_json = {
            '药品名称': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[2]/div[1]").text,
            '受理号': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[3]/div[1]").text,
            '药品类型': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[4]/div[1]").text,
            '注册分类': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[5]/div[1]").text,
            '申请人名称': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[6]/div[1]").text,
            '批准文号/注册证号': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[7]/div[1]").text,
            '持有人名称': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[8]/div[1]").text,
            '受理日期': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[10]/div[1]").text,
            '公开时间': self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[11]/div[1]").text
        }
        while (True):
            try:
                deep = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[9]/div[1]/button[1]")
            except exceptions.NoSuchElementException:
                continue
            else:
                break
        self.br.execute_script("arguments[0].click()", deep)

        table_xpath = "//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[5]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/form[1]/div[10]/div[1]/div[1]/div[3]/table[1]"
        while (True):
            try:
                detail_table = self.br.find_element(By.XPATH, table_xpath)
            except exceptions.NoSuchElementException:
                continue
            else:
                break

        login_patent_id = []
        login_grant_index = []
        patent_cite_type = []
        note = []
        n_tuple = len(detail_table.find_elements(By.TAG_NAME, "tr"))
        for i in range(1, n_tuple+1):
            login_patent_id.append(self.br.find_element(By.XPATH, table_xpath + "/tbody[1]/tr[" + str(i) + "]/td[2]/div[1]").text)
            login_grant_index.append(self.br.find_element(By.XPATH, table_xpath + "/tbody[1]/tr[" + str(i) + "]/td[3]/div[1]").text)
            patent_cite_type.append(self.br.find_element(By.XPATH, table_xpath + "/tbody[1]/tr[" + str(i) + "]/td[4]/div[1]").text)
            note.append(self.br.find_element(By.XPATH, table_xpath + "/tbody[1]/tr[" + str(i) + "]/td[5]/div[1]").text)
        data_json['登录的专利号'] = login_patent_id
        data_json['登录的权利要求项编号'] = login_grant_index
        data_json['专利声明类型'] = patent_cite_type
        data_json['备注'] = note
        back = self.br.find_element(By.XPATH,
                                    "//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[5]/div[1]/div[1]/div[3]/span[1]/button[1]")
        self.br.execute_script("arguments[0].click()", back)
        return data_json

    def getRowNum(self, page_i, n_page):
        rows_of_page = len(self.br.find_elements(By.XPATH, "//span[contains(text(),'查看')]"))
        rows_of_lastpage = self.getTotalNum() % rows_of_page
        return rows_of_page if page_i < n_page else rows_of_lastpage
