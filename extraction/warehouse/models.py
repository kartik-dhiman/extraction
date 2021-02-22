from django.db import models
from django.contrib.auth.models import User



class UserRequest(models.Model):

    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    input_url = models.URLField(max_length=2000, unique=True)

    def __str__(self):
        return self.input_url

    class Meta:
        verbose_name = 'User Request'  

    def _fetched_url_count(self):
        return self.crawledurls_set.count()


class CrawledUrls(models.Model):

    url = models.URLField(max_length=2000)
    user_request = models.ForeignKey(UserRequest, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Crawled Url'

    def shortUrl(self):
        return str(self.url)[:70]
