# -*- coding: utf-8 -*-

# Scrapy settings for pixiv_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pixiv_spider'

SPIDER_MODULES = ['pixiv_spider.spiders']
NEWSPIDER_MODULE = 'pixiv_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pixiv_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES = [400]
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'pixiv_spider.middlewares.RequestMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'pixiv_spider.middlewares.RequestMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# DOWNLOADER_MIDDLEWARES = {
#     'pixiv_spider.middlewares.RequestMiddleware': 543,
# }
# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'pixiv_spider.pipelines.ImagePipeline': 300,
}
IMAGES_STORE = './images'
IMAGE_ORIGINAL = False

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

COOKIE = '__cfduid=d2351997c5b464216ce7f46533ef6bc931595587628; first_visit_datetime_pc=2020-07-24+19%3A47%3A09; p_ab_id=6; p_ab_id_2=1; p_ab_d_id=1646478660; yuid_b=GUVzKQQ; _ga=GA1.2.1051181453.1595587636; PHPSESSID=19274869_M2LD8GBA5fJRGW7PCBAJY5JlI97ck8Ug; device_token=00bc11c3fcef99fd46e379d6b16ff357; c_type=20; privacy_policy_agreement=2; a_type=0; b_type=1; __utmz=235335808.1595651410.3.2.utmcsr=accounts.pixiv.net|utmccn=(referral)|utmcmd=referral|utmcct=/login; _fbp=fb.1.1595651458786.140744553; ki_r=; ki_s=208879%3A0.0.0.0.0; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=19274869=1^9=p_ab_id=6=1^10=p_ab_id_2=1=1^11=lang=zh=1; __gads=ID=978ac719fa9e4b0e:T=1595651681:S=ALNI_MY-jUzjNICI-Qi1ueMaWvdG8KcJaQ; stacc_mode=unify; __utmc=235335808; _gid=GA1.2.775098661.1596733037; __utma=235335808.1051181453.1595587636.1596733012.1596737058.25; ki_t=1595651496977%3B1596725950518%3B1596737075045%3B7%3B21; __utmt=1; __utmb=235335808.4.10.1596737058; tag_view_ranking=0xsDLqCEW6~MM6RXH_rlN~hRkZZnS6_e~jImOpI7tih~RTJMXD26Ak~r9KLLtm3OI~Mp-0OZE3a7~2QTW_H5tVX~aKhT3n4RHZ~_bee-JX46i~K8esoIs2eW~RcahSSzeRf~wjW5Y25gNH~NE-E8kJhx6~kGYw4gQ11Z~yPNaP3JSNF~Lt-oEicbBr~FqVQndhufZ~ujS7cIBGO-~q3eUobDMJW~isq3YRjJST~aLBjcKpvWL~nAtxkwJ5Sy~X4Eo-DdiUB~P5-w_IbJrm~-7ZTNQgdHv~h9fEA3tOFb~FgYArp6riX~CiSfl_AE0h~uC2yUZfXDc~QzKFCsGzn-~gtCILpPR9I~rGL2M8Jtgs~OgdypjrwdX~lQdVtncC-e~ePN3h1AXKX~_hSAdpN9rx~fWCK3-i_Fl~MWsPQsH1zi~ZBoVMjk2oM~2XSW7Dtt5E~J5hwvO5aFP~ctVZDT3sJK~WBevMnRO5F~4i9bTBXFoE~moGH48WbdM~bcAbumoPKA~gFY3XTihBM~LjHBwm3QmE~-bMa1UG3vE~VbPCYJXdEP~5mzv1EsHcE~5oPIfUbtd6~KN7uxuR89w~dzUQ-UDpYR~UfOZya7vqn~urcsq7fSsP~EZQqoW9r8g~ORA_C6YTOW~Ltq1hgLZe3~m-t9tha8UL~RthHN5LPvq~o8dzxSm6-F~PgeKPkeNFT~868PO22OrF~q_J28dYJ9d~QYP1NVhSHo~UBwhLy7Ngq~D9BseuUB5Z~2oy09JOeaJ~NsbQEogeyL~sRQy4rKivk~vdbd7LdFLQ~aC55Umcfh1~aqEioPF-VG~-oGijJmC5S~bWOtF0h5eA~sq68XTJrzi~9s62wUfVkX~52-15K-YXl~WcTW9TCOx9~jlDvv4Zu_K~r_Jjn6Ua2V~fUS-Ay2M9Z~3W4zqr4Xlx~ARZHSD6_B8~PHsucBd84t~ESbJLjiODP~Hvc3ekMyyh~LJo91uBPz4~EnqYNzLSIs~jH0uD88V6F~aU1t5sGM1S~RolC8IrBVO~HLWLeyYOUF~abgLj5TdiI~LsibVjl_VV~iWYAidoiGx~UR3UZdHtim~MUQoS0sfqG'
HEADERS = {
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Referer": "https://www.pixiv.net/login.php",
    "Origin": "https://accounts.pixiv.net",
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    'Cookie': COOKIE
}
FEED_EXPORT_ENCODING = 'UTF-8'
USER_ID = 19274869
MAX_PAGES = 1