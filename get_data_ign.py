from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_raw_html(url: str):
    """
    Get Verdict raw text from the page.
    """
    driver.get(url)
    article = driver.find_element(By.XPATH, '//section[@class="article-page"]').find_elements(By.TAG_NAME, 'p')
    article_text = ''
    for paragraph in article:
        article_text += paragraph.text
    return article_text.replace('\n', ' ').replace('|', ' ')


def get_videogames_review(data_file: str = 'data/switch-games-titles.txt'):
    with open(data_file) as file:
        videogames = file.readlines()
    reviews = []
    for ind, videogame in enumerate(videogames):
        videogame = videogame.strip('\n').split('|')
        print(ind, videogame[0])
        if len(videogame) == 2:
            try:
                # if ind > 15:
                #     raise
                reviews.append('|'.join([videogame[0], videogame[1], get_raw_html(videogame[1])]))
            except:
                reviews.append('|'.join(videogame))
        else:
            reviews.append('|'.join(videogame))
    with open(data_file, 'w') as file:
        file.write('\n'.join(reviews))


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # get_raw_html('https://www.ign.com/articles/thymesia-review')
    get_videogames_review()
    driver.close()