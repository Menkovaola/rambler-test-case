import schedule
import time
import vk_scraping
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--vk-service-token', metavar='path', required=False,
                        help='service token to access data via VK API')
    parser.add_argument('--input-file', metavar='path', required=False,
                        help='input file name')
    parser.add_argument('--db-name', metavar='path', required=False,
                        help='sqlite db name')
    args = parser.parse_args()

    schedule.every(1).day.do(vk_scraping.scrape, args.vk_service_token, args.input_file, args.db_name)
    schedule.run_all()

    while True:
        pending = schedule.run_pending()
        time.sleep(1)
