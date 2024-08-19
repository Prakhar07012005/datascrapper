import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QuotesSpider(scrapy.Spider):
    name = 'quotes_'
    start_urls = ['https://talentedge.com/browse-courses']
    max_courses = 10

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url,
                callback=self.parse,
                wait_time=10,
            )

    def parse(self, response):
        driver = response.meta['driver']
        
        # Wait for the courses to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col-md-6 a'))
        )

        # Extracting course links
        course_links = driver.find_elements(By.CSS_SELECTOR, 'div.col-md-6 a')
        course_links = [link.get_attribute('href') for link in course_links]

        # first 10 course links
        first_10_links = course_links[:self.max_courses]

        # Follow the first 10 links and parse their details
        for link in first_10_links:
            yield SeleniumRequest(
                link,
                callback=self.parse_course,
                wait_time=10,
            )

    def parse_course(self, response):
        driver = response.meta['driver']

        # Extract title
        title = response.css('h1.pl-title::text').get()

        # Extract description
        description_paragraphs = response.css('div.desc p::text').getall()
        description = ' '.join(description_paragraphs)

        # Extract duration, hours per week, and start date
        duration = response.css('div.duration-of-course li p strong::text').get()
        start_date = response.css('div.duration-of-course li:nth-child(2) p strong::text').get()

        # Extract key skills
        key_skills = response.css('div.key-skills-sec ul li::text').getall()

        # Extract "Most suited for" text
        most_suited_for_section = response.css('div.clinent-speaks div.cs-card')
        most_suited_for_texts = []
        for card in most_suited_for_section:
            tagline = card.css('h5.cs-tagline::text').get()
            if tagline and tagline.strip() == 'Most suited for':
                text = card.css('h4.cs-titlec::text').get()
                if text:
                    most_suited_for_texts.append(text.strip()) 

        # Extract eligibility section
        eligibility_section = response.css('div.eligible-div.eligible-div-new-design')
        eligibility_texts = eligibility_section.css('div.eligible-right-inner div.level-of-education p::text').getall()
        eligibility_text = ' '.join(text.strip() for text in eligibility_texts)

        # Extract content
        foundation_text = response.css('#syl-tab1 ul li::text').getall()
        concentration_text = response.css('#syl-tab2 ul li::text').getall()
        dissertation_text = response.css('#syl-tab3 ul li::text').getall()

        foundation_text = ' '.join(text.strip() for text in foundation_text)
        concentration_text = ' '.join(text.strip() for text in concentration_text)
        dissertation_text = ' '.join(text.strip() for text in dissertation_text)

        syllabus_content = f"Foundation (12 Credits): {foundation_text} Concentration (12 Credits): {concentration_text} Final Dissertation (32 Credits): {dissertation_text}"
        
        yield {
            'titletext ': title,
            'descriptiontext': description,
            'duration': duration,
            'start_date': start_date,
            'key_skills': key_skills,
            'most_suited_for': most_suited_for_texts,
            'eligibility': eligibility_text,
            'content': syllabus_content
        }
