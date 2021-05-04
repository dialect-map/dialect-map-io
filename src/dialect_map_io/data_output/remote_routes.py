# -*- coding: utf-8 -*-

from ..models import APIRoute


# -------- Dialect Map: Category routes -------- #

DM_CATEGORY_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/category",
    model_name="Category",
)
DM_CATEGORY_MEMBER_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/category/membership",
    model_name="CategoryMembership",
)
DM_CATEGORY_METRICS_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/category-metrics",
    model_name="JargonCategoryMetrics",
)


# -------- Dialect Map: Jargon routes -------- #

DM_JARGON_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/jargon",
    model_name="Jargon",
)
DM_JARGON_GROUP_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/jargon-group",
    model_name="JargonGroup",
)


# -------- Dialect Map: Paper routes -------- #

DM_PAPER_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/paper",
    model_name="Paper",
)
DM_PAPER_AUTHOR_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/paper/author",
    model_name="PaperAuthor",
)
DM_PAPER_METRICS_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/paper-metrics",
    model_name="JargonPaperMetrics",
)


# -------- Dialect Map: Reference routes -------- #

DM_REFERENCE_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/reference",
    model_name="PaperReference",
)
DM_REFERENCE_COUNTERS_ROUTE = APIRoute(
    api_name="dialect-map",
    api_path="/paper/reference/counters",
    model_name="PaperReferenceCounters",
)
