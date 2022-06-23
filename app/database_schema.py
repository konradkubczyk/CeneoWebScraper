DB_NAME = 'ceneo_web_scraper'

TABLES = {}

TABLES['products'] = (
    "CREATE TABLE `products` ("
    "  `product_id` int(15) NOT NULL,"
    "  `product_name` varchar(50) NOT NULL,"
    "  `opinions_count` int(4) NOT NULL,"
    "  `pros_count` int(5) NOT NULL,"
    "  `cons_count` int(5) NOT NULL,"
    "  `average_score` float NOT NULL,"
    "  PRIMARY KEY (`product_id`)"
    ") ENGINE=InnoDB")

TABLES['opinions'] = (
    "CREATE TABLE `opinions` ("
    "  `opinion_id` int(15) NOT NULL,"
    "  `author` varchar(20) NOT NULL,"
    "  `recommendation` varchar(20) NOT NULL,"
    "  `stars` varchar(3) NOT NULL,"
    "  `content` varchar(2000) NOT NULL,"
    "  `useful` int(3) NOT NULL,"
    "  `useless` int(3) NOT NULL,"
    "  `published` varchar(19) NOT NULL,"
    "  `purchased` varchar(19) NOT NULL,"
    "  `pros` varchar(500) NOT NULL,"
    "  `cons` varchar(500) NOT NULL,"
    "  `verified_purchase` varchar(30) NOT NULL,"
    "  PRIMARY KEY (`opinion_id`)"
    ") ENGINE=InnoDB")
