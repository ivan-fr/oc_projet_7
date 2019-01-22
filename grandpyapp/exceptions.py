class WikipediaException(Exception):
    """Base Wikipedia exception class."""

    def __init__(self, error):
        self.error = error

    def __unicode__(self):
        return "An unknown error occured: \"{0}\"." \
               " Please report it on GitHub!".format(self.error)

    def __str__(self):
        return self.__unicode__()


class PageError(WikipediaException):
    """Exception raised when no Wikipedia matched a query."""

    def __init__(self, title=None, pageid=None):
        if pageid:
            self.pageid = pageid
        else:
            self.title = title

    def __unicode__(self):
        if hasattr(self, 'title'):
            return "\"{0}\" does not match any pages." \
                   " Try another query!".format(self.title)
        else:
            return "Page id \"{0}\" does not " \
                   "match any pages. Try another id!".format(self.pageid)


class RedirectError(WikipediaException):
    """Exception raised when a page title
     unexpectedly resolves to a redirect."""

    def __init__(self, title):
        self.title = title

    def __unicode__(self):
        return "\"{0}\" resulted in a redirect. Set the redirect property" \
               " to True to allow automatic redirects.".format(self.title)


class HTTPTimeoutError(WikipediaException):
    """Exception raised when a request to the Mediawiki servers times out."""

    def __init__(self, query):
        self.query = query

    def __unicode__(self):
        return "Searching for \"{0}\" resulted in a timeout." \
               " Try again in a few" \
               " seconds, and make sure you have" \
               " rate limiting set to True.".format(self.query)
