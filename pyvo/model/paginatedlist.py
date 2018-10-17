
try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs


class PaginatedListBase:
    def __init__(self):
        self.__elements = list()

    def __getitem__(self, index):
        assert isinstance(index, (int, slice))
        if isinstance(index, (int, long)):
            self.__fetchToIndex(index)
            return self.__elements[index]
        else:
            return self._Slice(self, index)

    def __iter__(self):
        for element in self.__elements:
            yield element
        while self._couldGrow():
            newElements = self._grow()
            for element in newElements:
                yield element

    def _isBiggerThan(self, index):
        return len(self.__elements) > index or self._couldGrow()

    def __fetchToIndex(self, index):
        while len(self.__elements) <= index and self._couldGrow():
            self._grow()

    def _grow(self):
        newElements = self._fetchNextPage()
        self.__elements += newElements
        return newElements

    class _Slice:
        def __init__(self, theList, theSlice):
            self.__list = theList
            self.__start = theSlice.start or 0
            self.__stop = theSlice.stop
            self.__step = theSlice.step or 1

        def __iter__(self):
            index = self.__start
            while not self.__finished(index):
                if self.__list._isBiggerThan(index):
                    yield self.__list[index]
                    index += self.__step
                else:
                    return

        def __finished(self, index):
            return self.__stop is not None and index >= self.__stop


class PaginatedList(PaginatedListBase):
    """
    You can simply enumerate through instances of this class::

        for repo in user.get_repos():
            print(repo.name)

    If you want to know the total number of items in the list::

        ...
    """

    def __init__(self, response, request, method=method, response_type=response_type, contentClass=None, requester=None, firstUrl=None, firstParams=None, headers=None, list_item="items", **kwargs):
        PaginatedListBase.__init__(self)
        self.__response = response
        self.__request = request
        self.__method = method
        self.__response_type = response_type
        self.__send_kwargs = kwargs

        self.__limit = 100
        self.__offset = 0
        self.__total = None
        self.__returned = None

        self.__requester = requester
        self.__contentClass = contentClass
        self.__firstUrl = firstUrl
        self.__firstParams = firstParams or ()
        self.__headers = headers
        self.__list_item = list_item
        # if self.__requester.per_page != 30:
        #    self.__nextParams["per_page"] = self.__requester.per_page
        self.__totalCount = None

    def _couldGrow(self):
        # TODO check the math
        if self.__total is None:
            return True
        return self.__offset < self.__total

    def _fetchNextPage(self):
        # TODO increment offset and limit on request?

        self.__request.augment_queryparts({'offset': self.__offset, 'limit': self.__limit})

        response = self.__request._send(
            self.__method, self.__response_type, **self.__send_kwargs
        )
        data = response.json()
        headers = response.headers

        data = data if data else []

        # if len(data) > 0:
        limit, offset, total = self.__parseHeader(headers)

        self.__limit = limit
        self.__total = total
        self.__offset += self.__limit

        return data

        """
        self.__nextUrl = None
        if len(data) > 0:
            self.__parseHeader(headers)
            if self._reversed:
                if "prev" in links:
                    self.__nextUrl = links["prev"]
            elif "next" in links:
                self.__nextUrl = links["next"]
        self.__nextParams = None

        if self.__list_item in data:
            self.__totalCount = data.get('total_count')
            data = data[self.__list_item]

        content = [
            self.__contentClass(self.__requester, headers, element, completed=False)
            for element in data if element is not None
        ]
        return content
        """

    def __parseHeader(self, headers):
        limit = headers.get('X-Tracker-Pagination-Limit')
        offset = headers.get('X-Tracker-Pagination-Offset')
        total = headers.get('X-Tracker-Pagination-Total')
        # self.__returned = headers.get('X-Tracker-Pagination-Returned')
        return limit, offset, total
