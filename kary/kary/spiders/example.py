import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["kari.com"]
    start_urls = [f"https://kari.com/catalog/detskie-tovaryi/igrushki/konstruktoryi/?page={page}" for page in
                  range(1, 12)]

    def parse(self, response):
        heads = response.xpath('//div[@class="css-1cjptlq e1aj9z0o5"]/div[@class="css-8atqhb e1i0l88z31"]')
        for head in heads:
            product_url = 'https://kari.com' + head.xpath('.//a[@class="aqa-item"]/@href').get()
            yield response.follow(product_url, self.parse_product)

            # Handle pagination
        next_page = response.xpath(
            '//a[@class="css-1x6q3cl e1aj9z0o6"]/@href').get()  # Adjust based on actual pagination link
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        data = {
            'name': response.xpath('.//h1[@class="css-1qgty7c e1e0ha990"]/span/text()').get(),
            'price': response.xpath('.//p[@class="css-ku5rxg e1e2j8lt1"]/text()').get(),
            'photo': response.xpath('.//img[@alt="slider_image"]/@src').get(),
            'params': []
        }
        rows = response.xpath('//ul[@class="css-181mfsf ebq90a96"]/li')
        for row in rows:
            key = row.xpath('./span[1]/text()').get()  # Убрана запятая
            value = row.xpath('./span[2]//text()').getall()
            value = " ".join(value).strip()
            if key and value:  # Проверка на наличие key и value
                all_params = f"{key}: {value}"  # Формирование строки параметров
                data['params'].append(all_params.strip())  # Добавление в список
        yield data
