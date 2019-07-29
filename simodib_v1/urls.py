from django.urls import include, path
from .views import company, kurir, manager

urlpatterns = [
	path('', company.home, name='home'),
    path('closed/', company.closedPortal, name='closed'),

    path('kurir/', include(([
        path('', kurir.DistributionView.as_view(), name='distribution_list'),
        # path('interests/', kurir.StudentInterestsView.as_view(), name='student_interests'),
        # path('taken/', kurir.TakenQuizListView.as_view(), name='taken_quiz_list'),
        # path('quiz/<int:pk>/', kurir.take_quiz, name='take_quiz'),
    ], 'company'), namespace='kurir')),

    path('manager/', include(([
        path('', manager.dashboard, name='dashboard_view'),
        path('kurir/', manager.viewKurir, name='viewKurir'),
        path('kurir/<int:pk>/', manager.viewKurirDetail, name='viewKurirDetail'),
        path('kurir/<int:pk>/validate/', manager.validateKurir, name='validateKurir'),
        path('kurir/<int:pk>/unvalidate/', manager.unvalidateKurir, name='unvalidateKurir'),
        path('kurir/delete/', manager.deleteKurir, name='deleteKurir'),
        path('setting/portal/', manager.viewPortal, name='viewPortal'),
        path('beras/', manager.viewBeras, name='viewBeras'),
        path('beras/delete/', manager.deleteBeras, name='deleteBeras'),
        path('distribusi/', manager.viewDistribusi, name='viewDistribusi'),
        path('distribusi/add', manager.addPesanan, name='addPesanan'),
        path('distribusi/delete/', manager.deleteDistribusi, name='deleteDistribusi'),
        path('distribusi/unfinished/', manager.viewUnfinished, name='viewUnfinished'),
        path('distribusi/<int:pk>/', manager.viewDistribusiDetail, name='viewDistribusiDetail'),
        # path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        # path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        # path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        # path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        # path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'company'), namespace='manager')),
]