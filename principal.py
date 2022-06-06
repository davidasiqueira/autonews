import imp
import requests
from configparser import ConfigParser
import logging

def main():
    config = read_conf()
    write_news(get_news(config))

def read_conf():
    conf_dict = {}
    config = ConfigParser()
    config.read('autonews/config.ini')
    
    for key in config['default']:
        conf_dict[key] = config['default'][key]

    return conf_dict    
 

def get_news(conf):
    logging.basicConfig(filename="app.log", level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Sending HTTP GET")
   

    query_params = {
        'apiKey': conf['apikey'],
        'country': 'br',
        'category': conf['categoria'],
        'q': conf['palavrachave'],
        'pageSize': int(conf['numerodenoticias'])

    }
    response = requests.get('https://newsapi.org/v2/top-headlines', params=query_params)
    if response.status_code == 200:
        return response.json()
    else :
        logger.error("Error: %s" % response.status_code)
        return None    


def write_news(json):
    with open('autonews/news.txt', 'w') as f:
        f.write(str(json))


if __name__ == "__main__":
    main()   