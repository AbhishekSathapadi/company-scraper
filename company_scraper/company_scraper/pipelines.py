# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CompanyScraperPipeline:
    def process_item(self, item, spider):
        return item

# class ExcelExportPipeline:
#     def __init__(self):
#         self.items = []

#     def process_item(self, item, spider):
#         import html
#         cleaned_item = {
#             key: html.unescape(value) if isinstance(value, str) else value
#             for key, value in item.items()
#         }
#         self.items.append(cleaned_item)
#         return item

#     def close_spider(self, spider):
#         import pandas as pd
#         df = pd.DataFrame(self.items)
#         df.to_excel("company_data.xlsx", index=False)


from azure.storage.blob import BlobServiceClient
import pandas as pd
import html
import io
import os

class ExcelExportPipeline:
    def __init__(self):
        self.items = []

        # Azure Blob Storage configuration
        self.connection_string = os.getenv("")
        self.container_name = "acig-company-scraper-blob"
        self.blob_name = "company_data.xlsx"

        # Initialize BlobServiceClient
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def process_item(self, item, spider):
        cleaned_item = {
            key: html.unescape(value) if isinstance(value, str) else value
            for key, value in item.items()
        }
        self.items.append(cleaned_item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)

        # Save Excel file to a BytesIO stream
        excel_stream = io.BytesIO()
        df.to_excel(excel_stream, index=False)
        excel_stream.seek(0)

        # Upload to Azure Blob Storage
        self.container_client.upload_blob(
            name=self.blob_name,
            data=excel_stream,
            overwrite=True
        )

