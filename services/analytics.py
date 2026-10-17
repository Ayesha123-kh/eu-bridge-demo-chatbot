import logging

log = logging.getLogger("analytics")


def track_search(user_email, query):
    log.info(f"search query from {user_email}: {query}")


def track_page_view(path):
    log.info("page view %s", path)
