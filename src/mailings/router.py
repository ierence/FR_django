from rest_framework.routers import SimpleRouter

from .views import MailingListStatsViewSet, MailingListViewSet

router = SimpleRouter()

router.register("mailing-lists", MailingListViewSet, basename='mailing-lists')
router.register("mailing-lists-stats", MailingListStatsViewSet,
                basename='mailing-lists')
urlpatterns = router.urls
