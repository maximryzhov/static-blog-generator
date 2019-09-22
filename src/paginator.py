import math


class Paginator(object):

    def __init__(self, page_size, page_name):
        self.page_size = page_size
        self.page_num = 0
        self.page_count = 0
        self.page_name = page_name

    def paginate(self, query):
        self.page_count = math.ceil(len(query) / self.page_size)
        for i in range(0, len(query), self.page_size):
            self.page_num += 1
            yield query[i:i + self.page_size]

    @property
    def next_page(self):
        if self.page_num < self.page_count:
            return self.page_num + 1

    @property
    def prev_page(self):
        if self.page_num >= 1:
            return self.page_num - 1
