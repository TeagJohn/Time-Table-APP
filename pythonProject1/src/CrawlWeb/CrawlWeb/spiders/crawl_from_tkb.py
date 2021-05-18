import scrapy


class Crawling(scrapy.Spider):
    name = "get_timetable"
    start_urls = ["http://112.137.129.115/tkb/listbylist.php"]

    def parse(self, response):
        for line in response.xpath("//tr"):
            yield {
                "order": line.xpath(".//td[1]/text()").extract_first(),
                "subject_id": line.xpath(".//td[2]/text()").extract_first(),
                "subject_name": line.xpath(".//td[3]/text()").extract_first(),
                "credit": line.xpath(".//td[4]/text()").extract_first(),
                "class_id": line.xpath(".//td[5]/text()").extract_first(),
                "teacher_name": line.xpath(".//td[6]/text()").extract_first(),
                "number_of_students": line.xpath(".//td[7]/text()").extract_first(),
                "time": line.xpath(".//td[8]/text()").extract_first(),
                "weekday": line.xpath(".//td[9]/text()").extract_first(),
                "lesson": line.xpath(".//td[10]/text()").extract_first(),
                "place": line.xpath(".//td[11]/text()").extract_first(),
                "type" : line.xpath(".//td[12]/text()").extract_first(),
            }
