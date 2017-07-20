from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process_index),
    url(r'^add_process$', views.add_process),
    url(r'^delete_process$', views.delete_process),
    url(r'^edit_process$', views.editar_process),


    #fail
    url(r'^fail$', views.fail_index),
    url(r'^fail_process$', views.fail_process),
    url(r'^add_fail$', views.add_fail),
    url(r'^delete_fail$', views.delete_fail),
    url(r'^edit_fail$', views.edit_fail),

    #solution
    url(r'^solutions$', views.solutions_index),
    url(r'^solutions_fail$', views.solutions_fail),
    url(r'^add_solution$', views.add_solution),
    url(r'^delete_solution$', views.delete_solution),
    url(r'^edit_solution$', views.edit_solution),

    #simulator
    url(r'^simulator_process$', views.simulator_process),
    url(r'^fail_simulator$', views.fail_simulator),
    url(r'^similator$', views.view_simulator),
    url(r'^eject_fail$', views.eject_fail),
    url(r'^off_fail$', views.off_fail),

    #Pasos de solucion
    url(r'^step$', views.view_step),
    url(r'^solution_step$', views.solution_step),
    url(r'^add_step$', views.add_step),
    url(r'^edit_step$', views.edit_step),

    #detector
    url(r'^detector_process$', views.detector_process),
    url(r'^fail_detection$', views.fail_detection),
    url(r'^detector$', views.view_detector),
    url(r'^get_fails_detection$', views.get_fails_detection),
    

    #alarma
    url(r'^off_alarm$', views.off_alarm),

    #auxiliar
    
    url(r'^on_auxiliar$', views.on_auxiliar),
    url(r'^off_auxiliar$', views.off_auxiliar),
    url(r'^on_auxiliar2$', views.on_auxiliar2),
    url(r'^off_auxiliar2$', views.off_auxiliar2),

    
    url(r'^get_estado_alarma$', views.get_estado_alarma),


]
