from app_portfolio.models import Institution, Category


def institution_and_category_context(request):
    ctx = {
        "categories": Category.objects.all(),
        "institutions": Institution.objects.all(),
    }
    return ctx