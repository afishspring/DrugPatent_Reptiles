from DrugPatent import DrugPatent_Info_Reptiles, DrugPatent_Cite_Reptiles

if __name__=='__main__':
    # app1 = DrugPatent_Info_Reptiles(
    #     website='https://zldj.cde.org.cn/list?listType=PublicInfoList',
    #     next_page_xpath="//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[5]/div[1]/button[2]",
    #     bar_xpath="//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[5]/div[1]/ul[1]",
    #     bar_child_tag_name="li",
    #     xhr_pattern="getDetail",
    #     total_num_xpath="//div[@id='mainIndex']/section[@class='detailContent']/div//span[@class='el-pagination__total']",
    #     tab_xpath="/html//div[@id='tab-中药']"
    # )
    # app1.start()
    # app1.exportData("data/上市药品专利信息采集-中药-0730.xlsx")
    #
    # app2 = DrugPatent_Info_Reptiles(
    #     website='https://zldj.cde.org.cn/list?listType=PublicInfoList',
    #     next_page_xpath="//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[5]/div[1]/button[2]",
    #     bar_xpath="//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[5]/div[1]/ul[1]",
    #     bar_child_tag_name="li",
    #     xhr_pattern="getDetail",
    #     total_num_xpath="//div[@id='mainIndex']/section[@class='detailContent']/div//span[@class='el-pagination__total']",
    #     tab_xpath="/html//div[@id='tab-化药']"
    # )
    # app2.start()
    # app2.exportData("data/上市药品专利信息采集-化药-0730.xlsx")
    #
    # app3 = DrugPatent_Info_Reptiles(
    #     website='https://zldj.cde.org.cn/list?listType=PublicInfoList',
    #     next_page_xpath="//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[5]/div[1]/button[2]",
    #     bar_xpath="//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[5]/div[1]/ul[1]",
    #     bar_child_tag_name="li",
    #     xhr_pattern="getDetail",
    #     total_num_xpath="//div[@id='mainIndex']/section[@class='detailContent']/div//span[@class='el-pagination__total']",
    #     tab_xpath="/html//div[@id='tab-生物制品']"
    # )
    # app3.start()
    # app3.exportData("data/上市药品专利信息采集-生物制品-0730.xlsx")

    app4 = DrugPatent_Cite_Reptiles(
        website='https://zldj.cde.org.cn/list?listType=PatentStatementList',
        next_page_xpath="//body/div[@id='app']/div[@id='mainIndex']/section[1]/div[1]/div[4]/div[1]/button[2]",
        bar_xpath="//div[@id='mainIndex']/section[@class='detailContent']/div//ul[@class='el-pager']",
        bar_child_tag_name="li",
        total_num_xpath="//div[@id='mainIndex']/section[@class='detailContent']/div//span[@class='el-pagination__total']"
    )
    app4.start()
    app4.exportData("data/上市药品专利声明采集-0809.xlsx")