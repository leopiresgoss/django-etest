from django.urls import path

from .views import (
    TestsListView,
    test_creation,
    questions_creation,
    end_test,
    progress_test,
    delete_test
)

app_name = 'tests'

urlpatterns = [
    path('', TestsListView.as_view(), name='index'),
    path('create', test_creation, name='create'),
    path('<slug:test_code>/<int:num>', questions_creation, name='questions'),
    path('<slug:test_code>/end-test', end_test, name='end-test'),
    path('<slug:test_code>/progress', progress_test, name='progress-test'),
    path('<slug:test_code>/delete', delete_test, name='delete-test'),
]
