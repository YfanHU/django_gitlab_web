from selenium.webdriver import Chrome, ChromeOptions
from requests import post
from json import loads
from urllib.request import urlretrieve
from os.path import exists
from os import mkdir

# formats = ['m4a', 'mp3_l', 'mp3_h']
# format = formats[2]
def download_song(search_song,format='mp3_l',download=False):
    search_url = 'https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w={}'.format(
        search_song)
    search_download_url_url = 'http://www.douqq.com/qqmusic/qqapi.php'

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = Chrome('files/server/driver/chromedriver.exe', options=chrome_options)
    driver.get(search_url)
    driver.implicitly_wait(5)
    try:
        element = driver.find_element_by_xpath('//*[@id="song_box"]/div[2]/ul[2]/li[1]/div/div[2]/span/a')
        input_url = element.get_attribute('href')
    except:
        return False, '歌曲名未查询到！'
    finally:
        driver.close()

    try :
        info_dict = loads(loads(post(search_download_url_url, data={'mid': input_url}).text).replace('\/', '/'))
    except:
        return False, '破解大法失败，大侠还是购买正版吧！'

    if 'mp3' in format:
        file_name = '.'.join([info_dict['songname'], 'mp3'])
    else:
        file_name = '.'.join([info_dict['songname'], format])

    download_url = info_dict[format]
    print('download_url',download_url)
    if download:
        FILE_PATH = 'files/music/'
        if not exists(FILE_PATH):
            mkdir(FILE_PATH)
        try :
            urlretrieve(download_url, FILE_PATH+file_name)
        except :
            return False,'似乎无权作弊，你可以试试选择别的格式哟！'
        return True, FILE_PATH+file_name
    else :
        return True, download_url
