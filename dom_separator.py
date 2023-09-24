"""DO NOT RUN"""

import os
import pandas as pd

class CSVTextFileExporter:
    def __init__(self):
        self.df = pd.read_csv('oldUrlViolations.csv')
        self.unique_urls = None  # Initialize as None

    # drop rows where the 'DOM' column contains potential issues
    def drop_potential_issues(self):
        indices_to_drop = [31, 54, 55, 56, 57, 62, 178, 383, 413, 421]
        self.df = self.df.drop(indices_to_drop)
        self.df = self.df[self.df['webURL'] != 'https://snacknation.com/']
        
        """
        self.df = self.df[self.df['webURL'] != 'https://colab.research.google.com/']
        self.df = self.df[self.df['webURL'] != 'https://creativecommons.org/']
        self.df = self.df[self.df['webURL'] != 'https://discord.com/']
        self.df = self.df[self.df['webURL'] != 'https://girlswhocode.com/']
        self.df = self.df[self.df['webURL'] != 'https://github.com/']
        self.df = self.df[self.df['webURL'] != 'https://huggingface.co/']
        self.df = self.df[self.df['webURL'] != 'https://info.flip.com/en-us.html']
        self.df = self.df[self.df['webURL'] != 'https://mail.google.com/']
        self.df = self.df[self.df['webURL'] != 'https://medium.com/']
        self.df = self.df[self.df['webURL'] != 'https://myap.collegeboard.org/']
        
        self.df = self.df[self.df['webURL'] != 'https://news.google.com/']
        self.df = self.df[self.df['webURL'] != 'https://padlet.com/']
        self.df = self.df[self.df['webURL'] != 'https://partakefoods.com/']
        self.df = self.df[self.df['webURL'] != 'https://playwright.dev/']
        self.df = self.df[self.df['webURL'] != 'https://shop.lonelyplanet.com/']
        self.df = self.df[self.df['webURL'] != 'https://slack.com/']
        self.df = self.df[self.df['webURL'] != 'https://soundcloud.com/']
        self.df = self.df[self.df['webURL'] != 'https://stackoverflow.com/']
        self.df = self.df[self.df['webURL'] != 'https://symbolic.com/']
        self.df = self.df[self.df['webURL'] != 'https://translate.google.com/']
        
        self.df = self.df[self.df['webURL'] != 'https://travel.state.gov/content/travel/en/passports.html']
        self.df = self.df[self.df['webURL'] != 'https://twitter.com/']
        self.df = self.df[self.df['webURL'] != 'https://us.delsey.com/']
        self.df = self.df[self.df['webURL'] != 'https://vimeo.com/']
        self.df = self.df[self.df['webURL'] != 'https://weather.com/']
        self.df = self.df[self.df['webURL'] != 'https://wordpress.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.allsaints.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.apple.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.audible.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.baidu.com/']
        
        self.df = self.df[self.df['webURL'] != 'https://www.bankofamerica.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.barclays.co.uk/']
        self.df = self.df[self.df['webURL'] != 'https://www.bbc.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.belkin.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.bluesmoke.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.capitalone.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.cdc.gov/']
        self.df = self.df[self.df['webURL'] != 'https://www.dailymotion.com/us']
        self.df = self.df[self.df['webURL'] != 'https://www.dcshoes.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.dextel.agency/']
        
        self.df = self.df[self.df['webURL'] != 'https://www.disneyplus.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.dmv.ca.gov/portal/']
        self.df = self.df[self.df['webURL'] != 'https://www.docusign.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.dropbox.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.ebay.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.eventbrite.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.facebook.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.forbes.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.gap.com/']
        self.df = self.df[self.df['webURL'] != 'https://calendar.google.com/']
        
        self.df = self.df[self.df['webURL'] != 'https://www.geeksforgeeks.org/']
        self.df = self.df[self.df['webURL'] != 'https://www.glassesusa.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.google.com/maps']
        self.df = self.df[self.df['webURL'] != 'https://www.grubhub.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.guestreservations.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.healthcare.gov/']
        self.df = self.df[self.df['webURL'] != 'https://www.ieee.org/']
        self.df = self.df[self.df['webURL'] != 'https://www.instagram.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.itcorp.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.kaggle.com/']
        
        self.df = self.df[self.df['webURL'] != 'https://www.marcforgione.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.mayoclinic.org/']
        self.df = self.df[self.df['webURL'] != 'https://www.mightynetworks.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.mobileye.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.nature.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.netflix.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.nih.gov/']
        self.df = self.df[self.df['webURL'] != 'https://www.nike.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.nordstrom.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.npr.org/']
        
        self.df = self.df[self.df['webURL'] != 'https://www.nytimes.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.onepercentfortheplanet.org/']
        self.df = self.df[self.df['webURL'] != 'https://www.pacificlife.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.patagonia.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.patreon.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.quora.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.reddit.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.researchgate.net/']
        self.df = self.df[self.df['webURL'] != 'https://www.roblox.com/']
        
        self.df = self.df[self.df['webURL'] != 'https://www.scope.org.uk/']
        self.df = self.df[self.df['webURL'] != 'https://www.shybird.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.slideshare.net/']
        self.df = self.df[self.df['webURL'] != 'https://www.smythandtheloyalist.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.stanford.edu/']
        self.df = self.df[self.df['webURL'] != 'https://www.stepstonegroup.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.taylorguitars.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.thebazaar.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.theguardian.com/us']
        self.df = self.df[self.df['webURL'] != 'https://www.vortex.com/']
        
        self.df = self.df[self.df['webURL'] != 'https://www.waze.com/live-map/']
        self.df = self.df[self.df['webURL'] != 'https://www.whatsapp.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.weebly.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.wikipedia.org/']
        self.df = self.df[self.df['webURL'] != 'https://www.wordreference.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.yahoo.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.yokohamatire.com/']
        self.df = self.df[self.df['webURL'] != 'https://www.youtube.com/']
        self.df = self.df[self.df['webURL'] != 'https://zoom.us/']
        """
    def create_unique_urls(self):
        self.unique_urls = self.df['webURL'].unique()

    def save_text_files(self):

        # Create a directory to store the text files
        os.makedirs('DOM', exist_ok=True)

        # Call create_unique_urls to populate unique_urls
        self.create_unique_urls()

        # Create a mapping of unique webURL to numbers
        url_to_number = {url: idx for idx, url in enumerate(self.unique_urls, start=1)}

        # Create a mapping of unique DOMs to numbers
        url_to_dom_number = {}

        # Iterate through each row in the CSV
        for index, row in self.df.iterrows():
            url = row['webURL']
            dom_content = row['DOM']

            # Get the assigned number for this URL
            url_number = url_to_number[url]

            # Check if the DOM content has been assigned a number before
            if url in url_to_dom_number:
                number = url_to_dom_number[url]
            else:
                # If not, assign a new number
                number = len(url_to_dom_number) + 1
                url_to_dom_number[url] = number
            
             # Update the 'DOM' column with the assigned number
            self.df.at[index, 'DOM'] = number

            # Create a file for this URL with the assigned number as the filename
            file_path = os.path.join('DOM', f'{url_number}.txt')
            with open(file_path, 'w') as text_file:
                text_file.write(dom_content)
        
        # Save the updated DataFrame to a new CSV file
        self.df.to_csv('urlViolations.csv')

exporter = CSVTextFileExporter()
exporter.drop_potential_issues()
exporter.save_text_files()