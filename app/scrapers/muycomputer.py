"""
Scraper para MuyComputerPRO
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def get_muycomputer_news() -> List[Dict]:
    """Obtiene noticias de MuyComputerPRO sobre telecomunicaciones"""
    try:
        url = 'https://www.muycomputerpro.com/tag/telecomunicaciones/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_list = []
        articles = soup.find_all('article')
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for article in articles[:5]:
            try:
                title_element = article.find('h2', class_='entry-title')
                if not title_element:
                    continue
                    
                link_element = title_element.find('a')
                if not link_element:
                    continue
                
                title = title_element.text.strip()
                url = link_element['href']
                
                summary = ''
                summary_element = article.find('div', class_='entry-summary')
                if summary_element:
                    summary = summary_element.text.strip()
                
                news = {
                    'title': title,
                    'url': url,
                    'content': summary,
                    'source': 'MuyComputerPRO',
                    'category': 'Telecomunicaciones',
                    'date': current_date
                }
                news_list.append(news)
                
            except Exception as e:
                logger.error(f'Error procesando noticia de MuyComputerPRO: {str(e)}')
                continue
                
        return news_list
        
    except Exception as e:
        logger.error(f'Error obteniendo noticias de MuyComputerPRO: {str(e)}')
        return []
