# Natalia Brochocka, 171659
# Stanisław Ebertowski, 171919
# Michał Stachowski, 171570

from pyspark.sql import SparkSession
import boto3
import re
from io import BytesIO
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

spark_session = SparkSession.builder.getOrCreate()
input_bucket = 's3://commoncrawl/cc-index/table/cc-main/warc/'
dataframe = spark_session.read.parquet(input_bucket)
dataframe.createOrReplaceTempView("ccindex")
sql_dataframe = spark_session.sql("""SELECT url, warc_filename, warc_record_offset, warc_record_length
FROM ccindex
WHERE crawl='CC-MAIN-2020-16' 
AND subset='warc' 
AND url_host_tld='pl' """)
# sql_dataframe.show()

# MAIN-2020-16 marzec kwiecień 2020
# MAIN-2019-13 marzec 2019
# MAIN-2019-18 kwiecień  2019
warc_records = sql_dataframe.select("url", "warc_filename", "warc_record_offset", "warc_record_length").rdd

word_pattern = re.compile('\w+', re.UNICODE)


def html_to_text(page):
    try:
        encoding = EncodingDetector.find_declared_encoding(page, is_html=True)
        soup = BeautifulSoup(page, "lxml", from_encoding=encoding)
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(" ", strip=True)
    except:
        return ""


def process_word(rows):
    s3client = boto3.client('s3')
    for row in rows:
        warc_path = row['warc_filename']
        warc_offset = int(row['warc_record_offset'])
        warc_length = int(row['warc_record_length'])
        range_request = 'bytes={}-{}'.format(warc_offset, (warc_offset + warc_length - 1))
        response = s3client.get_object(Bucket='commoncrawl',
                                       Key=warc_path,
                                       Range=range_request)
        record_stream = BytesIO(response["Body"].read())
        for record in ArchiveIterator(record_stream):
            content = ''
            data = record.rec_headers.get_header('WARC-Date').split('T')
            page = record.content_stream().read()
            try:
                soup = BeautifulSoup(page, 'html.parser')
                meta_list = soup.find_all("meta")
                for meta in meta_list:
                    if 'name' in meta.attrs:
                        name = meta.attrs['name']
                        if name == 'keywords':
                            content = meta.attrs['content']
            except:
                pass
            text = html_to_text(page)
            words = map(lambda w: w.lower(), word_pattern.findall(text))
            words = filter(lambda w: w == "wirus" or w == "covid19" or w == "covid" or w == "pandemia", words)
            for word in words:
                yield (data[0], content, word), 1


word_counts = warc_records.mapPartitions(process_word).reduceByKey(lambda a, b: a + b)
output = word_counts.collect()
print("================\n\n\n\n\n\n\n\n\n")
str_output = '\n'.join([str(elem[0][0]) + ',' + str(elem[0][1]).replace('\n', ' ').replace('\r', ' ') + ',' + str(
    elem[0][2]) + ',' + str(elem[1]) for elem in output])
s3 = boto3.resource('s3')
s3_object = s3.Object('ase-bucket', 'file.txt')
s3_object.put(Body=str.encode(str_output))
print('===========================File saved to bucket!================================')

spark_session.stop()
