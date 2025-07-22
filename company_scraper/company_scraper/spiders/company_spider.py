import scrapy

class CompanySpider(scrapy.Spider):
    name = "company_spider"
    start_urls = [
        "https://en.wikipedia.org/wiki/Tata_Consultancy_Services",
        "https://en.wikipedia.org/wiki/Accenture",
        "https://en.wikipedia.org/wiki/Deloitte",
        "https://en.wikipedia.org/wiki/Capgemini"
    ]

    def parse(self, response):
        url_to_company = {
            "Tata_Consultancy_Services": "TCS",
            "Accenture": "Accenture",
            "Deloitte": "Deloitte",
            "Capgemini": "Capgemini"
        }

        company_key = response.url.split("/")[-1]
        company_name = url_to_company.get(company_key, "Unknown")

        info_box = response.css("table.infobox")
        founded = ceo = revenue_local = revenue_usd = operating_margin = None

        for row in info_box.css("tr"):
            header = row.css("th::text").get()
            data = row.css("td").xpath("string()").get()
            if header and data:
                header = header.strip()
                data = data.strip()
                if "Founded" in header and not founded:
                    founded = data
                elif "CEO" in header or "Chief executive officer" in header:
                    ceo = data
                elif "Revenue" in header:
                    if "US$" in data:
                        revenue_usd = data
                    else:
                        revenue_local = data
                elif "Operating income" in header or "Operating margin" in header:
                    operating_margin = data

        yield {
            "Company Name": company_name,
            "Founded": founded,
            "CEO": ceo,
            "Revenue (Local Currency)": revenue_local,
            "Revenue (USD Currency)": revenue_usd,
            "Operating Margin": operating_margin,
            "Source URL": response.url
        }
