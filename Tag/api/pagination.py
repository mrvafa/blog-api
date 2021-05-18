from rest_framework.pagination import PageNumberPagination


class TagPageNumberPagination(PageNumberPagination):
    page_size = 10
