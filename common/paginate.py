"""
This module deals all pagination related functions
"""
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from LMSSystem import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


"""
this method input query set and creates pages based on request
this function input queryset and return page wise model object
input : object_set is  QuerySet 
        pages: number of pages , if pages is empty take takes value from settings
        page_index: index page number
return: page_details
    """


def get_page(object_set,page_count,page):
    page_details = {}
    if object_set:
        if  page_count==0:
            page_count = settings.PAGE_COUNT
        paginator = Paginator(object_set,page_count)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        page_index = pages.start_index()
        page_details['page_index'] = page_index-1
        page_details['page'] = pages
        page_details['total_count']=object_set.count()
    return page_details
