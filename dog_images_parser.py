from pinscrape import pinscrape
details = pinscrape.scraper.scrape("cute dog photos", "/home/xdido/PycharmProjects/facemash/media", {}, 50, 55)

if details["isDownloaded"]:
    print("\nDownloading completed !!")
else:
    print("\nNothing to download !!")
