
flipkart = [
{
    'name': 'URL-Extractor',
    'description': 'Get all url and product base details',
    'id': 1,
    'parent_id': -1,
    'start_url': {
    'urls': None,
    'file': None,
    'column': None
    },
    'path': {
    'type': 'xpath',
    'value': '//*[@id="container"]/div/div[3]/div[1]/div[2]/div//div[@data-id]'
    },
    'base_url': 'https://www.flipkart.com',
    'pagination':  {
    'type': 'xpath',
    'value': '//*[@id="container"]/div/div[3]/div[1]/div[2]/div//nav/a/span/text()[ . = "Next"]/ancestor::a/@href',
    'route': None
    },
    'entity_list':  [
    {
    'name': 'product',
    'value': 'div/a[position()=2]/text()',
    'type': 'xpath',
    },{
    'name': 'url',
    'value': 'div/a[position()=1]/@href',
    'type': 'xpath',
    }
    ],
    'add_base_url' :  ['url'],
    'file': 'url_extractor_flipkart',
    'scraping_type': 'scrapy'
},
{
    'name': 'Reviews',
    'description': 'Get Comments and Reviews',
    'id': 3,
    'parent_id': 2,
    'start_url': {
        'urls': None,
        'file': 'redirector_flipkart',
        'column': 'url'
    },
    'path': {
        'type': 'xpath',
        'value':  '//*[@id="container"]/div/div[3]/div/div/div[last()]/div[position()> 2 and position ()< last()]'
    },
    'base_url': 'https://www.flipkart.com',
    'pagination':  {
        'type': 'xpath',
        'value' : '//span/text()[ . = "Next"]/ancestor::a/@href',
        'route': None
    },
    'entity_list':  [
        {
        'name': 'ratings',
        'value': 'div//div[@class="row"]//img/parent::div/text()',
        'type': 'xpath',
        },
        {
        'name': 'comments',
        'value': 'div//div[@class="row"]//img/parent::div/following-sibling::*/descendant-or-self::*/text()',
        'type': 'xpath',
        },
    
    ],
    'add_base_url' :  ['url'],
    'file': 'comments_flipkart',
    'scraping_type': 'scrapy'
},
{
    'name': 'Product Page',
    'description': 'Get Product Data and Redirect URL',
    'id': 2,
    'parent_id': 1,
    'start_url': {
        'urls': None,
        'file': 'url_extractor_flipkart',
        'column': 'url'
    },
    'path': {
        'type': 'xpath',
        'value': '//*[@id="container"]/div/div[3]/div[1]/div[2]'
    },
    'base_url': 'https://www.flipkart.com',
    'pagination':  {
        'type': None,
        'value' : None,
        'route': None
    },
    'entity_list':  [
        {
        'name': 'url',
        'value': "//span[substring(text(), string-length(text()) - string-length('reviews') + 1)  = 'reviews' and starts-with(text(), 'All')]//ancestor::a/@href",
        'type': 'xpath',
        }
    ],
    'add_base_url' :  ['url'],
    'file': 'redirector_flipkart',
    'scraping_type': 'scrapy'
}
]
