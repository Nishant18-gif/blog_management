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
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=[('draft', 'Draft'), ('published', 'Published')],
        default='draft'
    )

    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']  # Newest blogs first

    def __str__(self):
        return self.title


# -----------------------------
# LIKE MODEL
# -----------------------------
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'blog')  # one like per user per blog

    def __str__(self):
        return f"{self.user.username} likes {self.blog.title}"


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