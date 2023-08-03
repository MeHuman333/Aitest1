import time
import cv2
import numpy as np
import asyncio
import os
from pyppeteer import launch
from datetime import datetime, timedelta

#当前程序主要需要调整几个参数，包括场地、执行时间、两次滚动操作前等待时间、一次下一次操作前等待时间、两次操作之间的等待时间
#工作日和周末的场地数不同，需要调整场地参数；workday 晚8点/9点分别是11和13行;workday抢票的人估计偏少，7.31日抢票reload从1.43秒生效；
async def workday():

    # 获取当前日期
    current_date = datetime.now()

    # 计算两天后的日期
    two_days_later = current_date + timedelta(days=2)
    one_days_later = current_date + timedelta(days=1)
    # 将日期格式化为 "mm-dd" 形式的字符串
    #formatted_date = current_date.strftime("%m-%d")
    formatted_date = two_days_later.strftime("%m-%d")

    print(formatted_date)
    
    with open('jianshang_log.txt','a') as f:
            #q:写入当前时间
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+'\n')
    #browser = await launch(defaultViewport=None,executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe', headless=False,userDataDir='C:/Users/bradliu/AppData/Local/Google/Chrome/User Data',)
    browser = await launch(defaultViewport=None, executablePath='C:/Users/Brad/AppData/Local/Google/Chrome/Application/chrome.exe', headless=False, userDataDir='C:/Users/Brad/AppData/Local/Google/Chrome/User Data')

    page = await browser.newPage()
    await page.goto('https://lhqkl.ydmap.cn/booking/schedule/103909?salesItemId=102914', waitUntil='networkidle0')
    await asyncio.sleep(0.1)
    # 使用XPath选择器
    #elements = await page.xpath('//*[contains(text(), "{formatted_date}")]')
    elements = await page.xpath(f'//*[contains(text(), "{formatted_date}")]')

    if elements:
        # 获取元素的位置
        box = await elements[0].boundingBox()
        # 模拟鼠标点击
        await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        print("Element clicked.")
    else:
        print("Element not found.")

    await asyncio.sleep(0.1)  # 等待2秒让JavaScript加载完成
    # 获取当前的时间
    now = datetime.now()
    # 创建一个目标时间（今天的9点2分10秒）
    target_time = now.replace(hour=19, minute=59, second=35, microsecond=0)
    # 如果当前时间已经过了今天的9点2分10秒，那么将目标时间设置为明天的9点2分10秒
    if now > target_time:
        target_time += datetime.timedelta(days=1)

    # 计算现在到目标时间的秒数
    seconds_to_wait = (target_time - now).total_seconds()
    print(f"Waiting {seconds_to_wait} seconds...")
    # 等待相应的秒数
    time.sleep(seconds_to_wait)

    # 到达目标时间，执行操作
    await page.reload()
    print("Page reloaded!")
    await asyncio.sleep(0.1)  
    
    while True:
        # 获取元素
        element = await page.querySelector('td[data-v-66884ab0]')
        if element is None:
            print('reload后元素还不可读取，等待0.01秒后再次尝试...')
            print('打印None元素:',element)
            await asyncio.sleep(0.01)
            continue
        print('元素开始可读了，打印column_1元素:',element)
        class_attr = await page.evaluate('(element) => element.className', element)

        print('打印出class_attr值：',class_attr)
        if 'noOpen' in class_attr:
            # 这里的代码会在元素未开放预订时执行
            await asyncio.sleep(0.01)
            #await page.reload()
            print("noOpen状态，等待0.01秒!")
            continue
        else:
            # 这里的代码会在元素开放预订后执行
            print('现在可以进行正式预订程序了！')
            break
        
    #q:将当前时间记录到变量 time1 中   
    time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    time1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S.%f")
    #q:打印变量 time1 的值
    #print(time1)    
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))  
    await page.waitForSelector('#app > div > div > section > div > div:nth-child(3) > div > div.schedule__body-wrapper')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))     
    # 选择元素并向右滚动200像素，向下滚动到底
    #await asyncio.sleep(0.4)
    await asyncio.sleep(0.37)  # 等待0.4秒是无头模式的测试极限！（闲时,workday,家中及公司)，也是简上workday忙时测试验证过的值。0.37是前面增加await判读后的极限。
    await page.evaluate("""
        let element1 = document.querySelector('#app > div > div > section > div > div:nth-child(3) > div > div.schedule__body-wrapper');
        element1.scrollLeft = element1.Width;
        

    """)
        #element1.scrollTop = element1.scrollHeight
    print("Element scrolled!")
        # element1.scrollLeft = element1.scrollLeft - 100
    # 在新的页面位置使用JS路径查找并点击xx号场xx点的元素
    selector = '#app > div > div > section > div > div:nth-child(3) > div > div.schedule__body-wrapper > table > tbody > tr:nth-child(5) > td.schedule-table_column_23'
    element = await page.waitForSelector(selector)
    await element.click()

    selector = '#app > div > div > section > div > div:nth-child(3) > div > div.schedule__body-wrapper > table > tbody > tr:nth-child(7) > td.schedule-table_column_23'
    element = await page.waitForSelector(selector)
    await element.click()

    # 在新的页面位置使用JS路径查找并点击xx号场xx点的元素
    selector = '#app > div > div > section > div > div:nth-child(3) > div > div.schedule__body-wrapper > table > tbody > tr:nth-child(5) > td.schedule-table_column_24'
    element = await page.waitForSelector(selector)
    await element.click()

    selector = '#app > div > div > section > div > div:nth-child(3) > div > div.schedule__body-wrapper > table > tbody > tr:nth-child(7) > td.schedule-table_column_24'
    element = await page.waitForSelector(selector)
    await element.click()
    
    # 在新的页面使用JS路径查找并点击包含"下一步"的元素
    selector = '#app > div > div > section > div > div.fixed-bt.basic-fixed-bt > div.wrapper-right'
    element = await page.waitForSelector(selector)
    await element.click()
    #await asyncio.sleep(1.0) 
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))  
    await page.waitForSelector('body > div.el-message-box__wrapper > div > div.el-message-box__content > div.el-message-box__container > div')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")) 
    await asyncio.sleep(0.90)
    # 选择元素并滚动到底部
    await page.evaluate("""
       let element = document.querySelector('body > div.el-message-box__wrapper > div > div.el-message-box__content > div.el-message-box__container > div');
       element.scrollTop = element.scrollHeight;
    """)
    print("Element scrolled!原来后面要停顿2秒.")
    await asyncio.sleep(0.1)  # 等待2秒让JavaScript加载完成

    # 在新的页面使用selector查找并点击包含"接受"的元素,这个比用xpath查找的要更稳定，不会导致页面变化后找不到元素

    selector = 'button.el-button.el-button--default.el-button--small.el-button--primary'
    element = await page.waitForSelector(selector)
    await element.click()
    print("接受clicked.")
    #await asyncio.sleep(1.1)  # 等待2秒让JavaScript加载完成
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    #await page.waitForSelector('#app > div > div > div > section > div.fixed-bt.basic-fixed-bt > div.wrapper-right')  
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    #await asyncio.sleep(0.70) #闲时设置0.56 部分时间OK，网络较差时需要0.65
    
    # 获取第一个时间点
    start_time = datetime.now()
    #print(start_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
    await page.waitForSelector('#app > div > div > div > section > div.fixed-bt.basic-fixed-bt > div.wrapper-right')  
    # 获取第二个时间点
    end_time = datetime.now()
    # 计算时间差
    time_diff = end_time - start_time
    print(f'Time difference: {time_diff}')
    #print(end_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
    #await asyncio.sleep(0.29)
    seconds = time_diff.total_seconds()
    await asyncio.sleep(max(0.56, seconds + seconds -0.01))
    # 通过选择器选择“下一步”按钮元素并模拟鼠标点击
    element = await page.querySelector('#app > div > div > div > section > div.fixed-bt.basic-fixed-bt > div.wrapper-right')
    await element.click()

    #await click_until_successful(page, '#app > div > div > div > section > div.fixed-bt.basic-fixed-bt > div.wrapper-right')

    #await asyncio.sleep(1.1)  # 等待2秒让JavaScript加载完成
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    await page.waitForSelector('.el-checkbox__original')  
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    await asyncio.sleep(0.29)
    # 点击复选框

    await page.evaluate('''() => {
         document.querySelector('.el-checkbox__original').click();
    }''')

    await asyncio.sleep(0.01)

    # 通过button_selector 选择“下一步”按钮元素
    selector = 'button.el-button.full-width.primary-button.el-button--text'
    element = await page.waitForSelector(selector)
    # 点击按钮
    await element.click()
    
    #await page.evaluate('''() => {
    #let button = document.querySelector(".el-button.full-width.primary-button.el-button--text");
    #button.click();
    #}''')
    
    
    time2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    # 转换为 datetime 对象
    #time1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S.%f")
    time2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S.%f")

    # 计算 time2 - time1 的值，赋值给变量 time3
    time3 = time2 - time1
    #q:打印变量 time3 , 按精确到微秒的格式打印
    print('时间差',time3.total_seconds())
    with open('jianshang_log.txt','a') as f:
            f.write(str(time3.total_seconds())+'\n')
            #q:写入当前时间
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+'\n')
    
    await asyncio.sleep(15)

    await browser.close()

asyncio.get_event_loop().run_until_complete(workday())
   


