from zameen_scraper import PlotScraper

plotscraper = PlotScraper("https://www.zameen.com/new-projects/search.html")
plotscraper.open_page()
plotscraper.search_parser()

