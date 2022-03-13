from users import views
from core.routers import ViewAPIRouter

router = ViewAPIRouter(prefix='/users', tags=["users"])

router.add_api_view_route("/me/details", views.MyUserDetailsView)
router.add_api_view_route("/{model_id}/details", views.UserDetailsView)
router.add_api_view_route("/me/update", views.UserUpdateView)
