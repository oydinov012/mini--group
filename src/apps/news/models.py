from django.db import models

class NewsType(models.Model):
    name = models.CharField(max_length=200, verbose_name='newsType')


    def __str__(self):
        return self.name
    



class News(models.Model):
    news_type = models.ForeignKey(to=NewsType, on_delete=models.CASCADE, related_name='news_type')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    

class NewsImage(models.Model):
    news = models.ForeignKey(to=News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/')

    def __str__(self):
        return self.news.title

    
    

