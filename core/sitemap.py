from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):

    def items(self):
        return [
            'index',
            'download',
            'change_lang']

    def location(self, item):
        return reverse(item)