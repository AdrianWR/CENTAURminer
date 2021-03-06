def TagList(str_list, tag="item"):
    '''
    Tags a list and converts to a string - avoids data corruption by using a more complex tag.

    Arguments
    ---------
    str_list : list
        List of strings to be joined with tags.
    tag : str, optional
        Tag to use for the list. This tag will be wrapped in `<...>` and `</...>` to close.
    '''
    result = ""
    for string in str_list:
        result += "<item>" + string + "</item>"
    return result


def CollectURLs(start_url, link_elem, next_elem=None):
    '''
    Collects a list of URLs from a search of the site.

    Arguments
    ---------
    start_url : str
        URL for the first page of a site search.
    link_elem : :class:`centaurminer.Element`
        An Element indicating where individual URL links can be found on the search page.
    next_elem : :class:`centaruminer.Element`, optional
        Indicates where on the page the "next page" button is, to navigate through search pages.
    '''
    from .DOM_elements import PageLocations
    from .Engine import MiningEngine

    urls = []
    pageNum = 1
    # Get access to a webdriver and load the page
    miner = MiningEngine(PageLocations)
    miner.wd.get(start_url)

    # Load all the links on this page
    elems = miner.get(link_elem, several=True)
    if next_elem is None:
        return elems

    # Repeatedly gather links from several pages
    while len(elems) > 0:
        print("Appending URLs from page", pageNum)
        urls.extend(elems)
        if len(urls) > 50:
            break

        # Go to next page
        try:
            print("Going to page", pageNum + 1)
            next_button = miner.wd.find_element(next_elem.method, next_elem.selector)
            next_button.click()
        except Exception:
            break
        elems = miner.get(link_elem, several=True)
        pageNum += 1
    return urls
