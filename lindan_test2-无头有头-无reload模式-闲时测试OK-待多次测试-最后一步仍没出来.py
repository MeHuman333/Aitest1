import asyncio
from pyppeteer import launch
import time
from datetime import datetime, timedelta

#当前程序主要需要调整几个参数，包括场地、执行时间、两次滚动操作前等待时间、一次下一次操作前等待时间、两次操作之间的等待时间
#林丹场地无周末区别，简上场地周末有区别
async def click_weekday():
    # 获取当前日期
    current_date = datetime.now()
    # 计算4天后的日期
    four_days_later = current_date + timedelta(days=4)
    one_days_later = current_date + timedelta(days=1)
    # 将日期格式化为 "mm-dd" 形式的字符串
    #formatted_date = current_date.strftime("%m-%d")
    formatted_date = four_days_later.strftime("%m-%d")
    print(formatted_date) 

    #browser = await launch(defaultViewport=None,executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe', headless=True,userDataDir='C:/Users/bradliu/AppData/Local/Google/Chrome/User Data',)
    browser = await launch(
    defaultViewport=None, 
    executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe', 
    headless=False, 
    userDataDir='C:/Users/bradliu/AppData/Local/Google/Chrome/User Data', 
    )

    page = await browser.newPage()
    # 导航到网页
    #await page.goto('https://szwld.ydmap.cn/booking/schedule/105272')
    #await asyncio.sleep(1.8)
    await page.goto('https://szwld.ydmap.cn/booking/schedule/105272', waitUntil='networkidle0')

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
    target_time = now.replace(hour=8, minute=59, second=40, microsecond=0)
    # 如果当前时间已经过了今天的9点2分10秒，那么将目标时间设置为明天的9点2分10秒
    if now > target_time:
        target_time += datetime.timedelta(days=1)

    # 计算现在到目标时间的秒数
    seconds_to_wait = (target_time - now).total_seconds()
    print(f"Waiting {seconds_to_wait} seconds...")
    # 等待相应的秒数#############################################################
    
    time.sleep(seconds_to_wait)
    
    # 到达目标时间，执行操作
    await page.reload()
    print("Page reloaded!")
    await asyncio.sleep(0.25)  

    while True:
        # 获取元素
        element = await page.querySelector('td[data-v-3bebe490]')
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
    await asyncio.sleep(0.37)  # 等待0.4秒是无头模式的测试极限！（闲时,workday,家中及公司)，也是简上workday忙时测试验证过的值。0.37是前面增加await判读后的极限。
        # 选择元素并滚动到右侧底部
    await page.evaluate("""
        let element1 = document.querySelector('#app > div > div > section > div > div:nth-child(3) > div > div.schedule__body-wrapper');
        element1.scrollLeft = element1.scrollWidth;
    """)
    await asyncio.sleep(0.01)
    # 在新的页面使用XPath选择器查找并点击包含"9号羽毛球场"的元素
    elements = await page.xpath('//*[contains(text(), "9号羽毛球场")]')
    if elements:
        box = await elements[0].boundingBox()
        offset1 = 54.4 * 2  # 设置偏移量
        offset2 = 54.4 * 3  # 设置偏移量        
        await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2 + offset1)
        print("Element 2 clicked.")
        #await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2 + offset2)
        #print("Element 3 clicked.")
    else:
        print("Element not found.")
    # 在新的页面使用XPath选择器查找并点击包含"10号羽毛球场"的元素
    
    elements = await page.xpath('//*[contains(text(), "10号羽毛球场")]')
    if elements:
        box = await elements[0].boundingBox()
        offset1 = 54.4 * 2  # 设置偏移量
        offset2 = 54.4 * 3  # 设置偏移量        
        await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2 + offset1)
        print("Element 4 clicked.")
        await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2 + offset2)
        print("Element 5 clicked.")
    else:
        print("Element not found.")
    # await asyncio.sleep(0.1)  # 等待2秒让JavaScript加载完成
    
    # 在新的页面使用XPath选择器查找并点击包含"下一步"的元素
    elements = await page.xpath('//*[contains(text(), "下一步")]')
    if elements:
        # 点击"下一步"
        box = await elements[0].boundingBox()
        await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        print("Element 6 clicked.")
        
    else:
        print("Element not found.")
    # 选择元素并滚动到底部
    #await asyncio.sleep(1.0) # 等待0.9秒是无头模式测试的极限(闲时,workday，家中only,公司变为1.0秒，遂改为await后等0.91秒)
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))  
    await page.waitForSelector('body > div.el-message-box__wrapper > div > div.el-message-box__content > div.el-message-box__container > div')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")) 
    await asyncio.sleep(0.91)
    await page.evaluate("""
       let element2 = document.querySelector('body > div.el-message-box__wrapper > div > div.el-message-box__content > div.el-message-box__container > div');
       element2.scrollTop = element2.scrollHeight;
    """)
    print("Element scrolled!原来后面要停顿2秒.")
    #await asyncio.sleep(0.01)  # 等待2秒让JavaScript加载完成
    await asyncio.sleep(1.50)  # 等待1.4秒是无头模式测试的极限(闲时,workday,家中only,公司变1.5秒)
    # 在新的页面使用selector查找并点击包含"接受"的元素,这个比用xpath查找的要更稳定，不会导致页面变化后找不到元素
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))  
    await page.waitForSelector('body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")) 
    selector = 'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary'
    element = await page.waitForSelector(selector)
    if element:
      box = await element.boundingBox()
      await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
      print("接受Element5 clicked.")
    else:
      print("Element not found.")

    #await asyncio.sleep(0.8)  # 等待0.5秒是无头模式的测试极限！（闲时,workday，家中only,公司变0.6秒，之后又变0.8秒！很不稳定,遂改为await + 0.29秒时延模式！)
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    #await page.waitForSelector('#app > div > div > div > section > div.fixed-bt.basic-fixed-bt > div.wrapper-right > button')  
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    # 获取第一个时间点
    start_time = datetime.now()

    #print(start_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
    await page.waitForSelector('#app > div > div > div > section > div.fixed-bt.basic-fixed-bt > div.wrapper-right > button')  

    # 获取第二个时间点
    end_time = datetime.now()

    # 计算时间差
    time_diff = end_time - start_time
    print(f'Time difference: {time_diff}')

    #print(end_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

    #await asyncio.sleep(0.29)
    seconds = time_diff.total_seconds()
    await asyncio.sleep(max(0.34, seconds - 0.01))

    # 在新的页面使用JS路径查找并点击包含"下一步"的元素
    # await page.waitForSelector('#app > div > div > div > section > div.fixed-bt.basic-fixed-bt > div.wrapper-right > button')
    await page.evaluate('''() => {
        let button = document.querySelector(".el-button.primary-button");
        button.click();
    }''')

    #q:将当前时间记录到变量 time2 中
    time2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    time2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S.%f")
    # 计算 time2 - time1 的值，赋值给变量 time3
    time3 = time2 - time1
    print('时间差',time3.total_seconds())
    #q:输出到文件log.txt中，如果log.txt文件已经存在，就追加写入，否则就创建新文件并写入
    with open('log.txt','a') as f:
        f.write(str(time3.total_seconds())+'\n')
        #q:写入当前时间
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+'\n')

    # 等待30秒，预防最后的点击不能成功
    await asyncio.sleep(10)
    # 关闭浏览器
    await browser.close()

asyncio.get_event_loop().run_until_complete(click_weekday())
   
    

