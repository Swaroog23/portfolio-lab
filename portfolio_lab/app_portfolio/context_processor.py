from app_portfolio.models import Institution, Category


def institution_and_category_context(request):
    categories = Category.objects.all()
    institutions = Institution.objects.all()
    foundations = institutions.filter(type=1)
    non_gov_organisations = institutions.filter(type=2)
    local_collections = institutions.filter(type=3)
    ctx = {
        "categories": categories,
        "institutions": institutions,
        "foundations": foundations,
        "non_gov_organisations": non_gov_organisations,
        "local_collections": local_collections,
    }
    return ctx