# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from scrapy.http import Request

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/63247-westworld/']

    def parse(self, response):
        """
        This method finds the hyperlink to the next webpage and 
        passes it to another parser function.
        """

        # this command finds the url to the next page
        next_page = response.css('#media_v4 .new_button a::attr(href)').get()
        # joins the initial link to the url found above
        yield response.follow(next_page, callback=self.parse_full_credit)

    def parse_full_credit(self, response):
        """
        This function extracts the links to each cast member and 
        calls parse_actor_page function for further parsing.
        """
        # gets the links to the cast members
        # it limits only to the first 50 cast members
        cast_links=response.css('.panel.pad > ol > li > a::attr(href)').getall()[:50]

        # makes a full url link
        #next_pages = ["https://www.themoviedb.org" + link for link in cast_links]

        # loops over actor pages
        for next_page in cast_links:
            yield Request("https://www.themoviedb.org" + next_page, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        """
        This function yields a dictionary 
        {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name},
        which is a dictionary of the movies or TV shows that 
        the actor has played in.
        """
        
        # getting the actor's name
        actor_name=response.css("h2 a::text").get()
        # getting a list of movies that the actor played in
        movie_or_TV_names=response.css("table bdi::text").getall()

        # iterating through movies and yielding a dictionary
        for movie_or_TV_name in movie_or_TV_names:
            yield {
                "actor": actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }
        