from django.core.management.base import BaseCommand, CommandError
from scrapper import tasks


class Command(BaseCommand):
    help = "Scrape news from news sites"

    def add_arguments(self, parser):
        parser.add_argument("--site", nargs="+", type=str)

    def handle(self, *args, **options):
        sites = options["site"] or ["https://www.nytimes.com/", "https://edition.cnn.com/", "https://www.bbc.com/"]
        print(sites)
        try:
            self.stdout.write(
                self.style.SUCCESS("Scrapping from %s ..." % ", ".join(sites))
            )
            tasks.scrape_news(sites)
        except Exception as e:
            raise CommandError('Error scraping news: "%s"' % str(e))

        self.stdout.write(
            self.style.SUCCESS("Successfully scraped news from %s" % ", ".join(sites))
        )