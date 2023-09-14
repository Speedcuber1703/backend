from datetime import datetime, date, time, timedelta
from django import template
from django.db.models import Count, Q
from taggit.models import Tag
from django.utils import timezone

from ..models import Comment, Article

register = template.Library()

@register.simple_tag
def popular_tags():
    tags = Tag.objects.annotate(num_times=Count('article', filter=Q(article__status='published'))).order_by('-num_times')
    tag_list = list(tags.values('name', 'num_times', 'slug'))
    return tag_list

@register.inclusion_tag('includes/latest_comments.html')
def show_latest_comments(count=5):
    comments = Comment.objects.select_related('author')\
        .filter(status='published').order_by('-time_create')[:count]
    return {'comments': comments}

@register.simple_tag
def popular_articles():
    now = timezone.now()
    start_date = now - timedelta(days=7)
    today_start = timezone.make_aware(datetime.combine(date.today(), time.min))

    articles = Article.objects.annotate(
        total_view_count=Count('views', filter=Q(views__viewed_on__gte=start_date)),
        today_view_count=Count('views', filter=Q(views__viewed_on__gte=today_start))
    ).prefetch_related('views')

    popular_articles = articles.order_by('-total_view_count', '-today_view_count')[:10]
    return popular_articles
