from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# BLOG MODEL
# -----------------------------
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Optional image

    class Meta:
        ordering = ['-created_at']  # Newest blogs first

    def __str__(self):
        return f"{self.title} by {self.author.username}"


# -----------------------------
# COMMENT MODEL
# -----------------------------
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Oldest comments first

    def __str__(self):
        return f"Comment by {self.author.username} on {self.blog.title}"