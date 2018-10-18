
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

    def __init__(self, request, method=None, response_type=None, contentClass=None, requester=None, firstUrl=None, firstParams=None, headers=None, list_item="items", **kwargs):
        PaginatedListBase.__init__(self)
        self.__request = request
        self.__method = method
        self.__response_type = response_type
        self.__send_kwargs = kwargs

        self.__limit = 100
        self.__offset = 0
        self.__total = None
        self.__returned = None

        # TODO cleanup
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
        # XXX check the math
        if self.__total is None:
            return True
        return self.__offset < self.__total

    def _fetchNextPage(self):
        self.__request.augment_queryparts({'offset': self.__offset, 'limit': self.__limit})

        response = self.__request._send(
            # XXX use ResponseType.RAW
            self.__method, 'raw', **self.__send_kwargs
        )
        data = response.json()
        headers = response.headers

        data = data if data else []
        print(data)

        self.__parseHeader(headers)

        return data

    def __parseHeader(self, headers):
        def parseInt(header):
            value = headers.get(header)
            return int(value) if value else value

        limit = parseInt('X-Tracker-Pagination-Limit')
        offset = parseInt('X-Tracker-Pagination-Offset')
        total = parseInt('X-Tracker-Pagination-Total')
        returned = parseInt('X-Tracker-Pagination-Returned')

        # handle non paginated apis being called
        if not any([limit, offset, total]):
            self.__offset = self.__total
        else:
            self.__limit = limit or self.__limit
            self.__total = total or self.__total
            self.__offset = offset or self.__offset
            self.__offset += self.__limit

        print(f'{limit}, {offset}, {total}')
