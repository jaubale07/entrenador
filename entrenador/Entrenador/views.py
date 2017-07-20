# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Process, Fail, Solution, Step
from django.core import serializers
from gpiozero import LED, Button
from threading import Thread
import os
from time import sleep

ruta_alarma = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#0 es el auxiliar, 1 es la alarma
leds = 0
alarma =  [False, False, LED(26), False, False, False, LED(27), False]
classes = []
pines_in = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
pines_out = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]


class Fallo():
    def __init__(self, index):
        self.pin = pines_out[index]
        self.led = LED(pines_out[index])
        self.button = Button(pines_in[index])
        self.estado = False
        self.swich = True

    def run(self):
        while self.swich:
            if self.button.is_pressed:
                if not self.estado:
                    self.estado = True
                    fails = Fail.objects.filter(pin=self.pin)
                    for f in fails:
                        f.activo = True
                        f.save()
            else:
                if self.estado:
                    fails = Fail.objects.filter(pin=self.pin)
                    for f in fails:
                        f.activo = False
                        f.save()
                    self.estado = False
            self.button.wait_for_press()
            self.press()
        


    def press(self):
        print('press: ' + str(self.pin))
        self.led.on()
        sleep(3)
        self.led.off()


def iniciar_fallos():
    if not alarma[4]:
        for i in range(0, 12):
            fallo = Fallo(i)
            classes.append(fallo)
            th = Thread(target=fallo.run)
            th.start()
        alarma[4] = True


def index(request):    
    return render(request, 'index.html', {})


def process_index(request):
    process = Process.objects.all()
    if 'msg' in request.session:
        msg = request.session['msg']
        del request.session['msg']
        return render(request, 'process.html', {'process': process, 'msg': msg})

    return render(request, 'process.html', {'process': process})


def add_process(request):
    if request.method == 'POST' and 'name' in request.POST:
        process = Process()
        process.name = request.POST['name']
        process.save()
        request.session['msg'] = 'Proceso registrado exitosamente'
        return HttpResponseRedirect('/')


def delete_process(request):
    if 'id' in request.GET:
        try:
            process = Process.objects.get(id=request.GET['id'])
            process.delete()
            request.session['msg'] = 'Proceso Eliminado exitosamente'
            return HttpResponseRedirect('/')
        except Process.DoesNotExist:
            return HttpResponseRedirect('/')


def editar_process(request):
    if request.method == 'POST':
        try:
            process = Process.objects.get(id=request.POST['id'])
            process.name = request.POST['name']
            process.save()
            request.session['msg'] = 'Proceso editado exitosamente'
            return HttpResponseRedirect('/')
        except Process.DoesNotExist:
            return HttpResponseRedirect('/')


def fail_index(request):
    if 'process' in request.session:
        process = Process.objects.get(id=request.session['process'])
        fails = Fail.objects.filter(process=process)
        if 'msg' in request.session:
            msg = request.session['msg']
            del request.session['msg']
            return render(request, 'fail.html', {'process': process, 'fails': fails, 'msg': msg.encode('utf-8')})
        return render(request, 'fail.html', {'process': process, 'fails': fails})
    else:
        return HttpResponseRedirect('/')


def fail_process(request):
    if 'id' in request.GET:
        request.session['process'] = request.GET['id']
        return HttpResponseRedirect('fail')        


def add_fail(request):
    if request.method == 'POST' and (request.session['process'] == request.POST['process']):
        pines_out = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        process = Process.objects.get(id=request.POST['process'])
        fails = Fail.objects.filter(process=process)
        if len(fails) >= len(pines_out):
            request.session['msg'] = 'Lo sentimos se superaron las 22 fallas posiblres a registrar'
            return HttpResponseRedirect('fail')
        fail = Fail()
        fail.process = process
        fail.name = request.POST['name']
        fail.pin = pines_out[len(fails)]
        fail.save()
        request.session['msg'] = 'Fallo agregado con exito'
        return HttpResponseRedirect('fail')
    else:
        return HttpResponseRedirect('/')


def delete_fail(request):
    if 'id' in request.GET:
        try:
            fail = Fail.objects.get(id=request.GET['id'])
            fail.delete()
            request.session['msg'] = 'Fallo eliminado con exito'
            return HttpResponseRedirect('fail')
        except Fail.DoesNotExist:
            return HttpResponseRedirect('/')


def edit_fail(request):
    if request.method == 'POST':
        try:
            fail = Fail.objects.get(id=request.POST['id'])
            fail.name = request.POST['name']
            fail.save()
            request.session['msg'] = 'Fallo editado con exito'
            return HttpResponseRedirect('fail')
        except Fail.DoesNotExist:
            return HttpResponseRedirect('/')


def solutions_index(request):
    if 'fail' in request.session:
        fail = Fail.objects.get(id=request.session['fail'])
        solutions = Solution.objects.filter(fail=fail)

        if 'msg' in request.session:
            msg = request.session['msg']
            del request.session['msg']
            return render(request, 'solutions.html', {'fail': fail, 'solutions': solutions, 'msg': msg.encode('utf-8')})
        return render(request, 'solutions.html', {'fail': fail, 'solutions': solutions})


def solutions_fail(request):
    if 'id' in request.GET:
        request.session['fail'] = request.GET['id']
        return HttpResponseRedirect('solutions')


def add_solution(request):
    if request.method == 'POST':
        try:
            fail = Fail.objects.get(id=request.POST['fail'])
            solution = Solution()
            solution.fail = fail
            solution.name = request.POST['name']
            solution.save()
            request.session['msg'] = 'Solución agregado con exito'
            return HttpResponseRedirect('solutions')
        except Fail.DoesNotExist:
            return HttpResponseRedirect('/')


def delete_solution(request):
    if 'id' in request.GET:
        try:
            solution = Solution.objects.get(id=request.GET['id'])
            solution.delete()
            request.session['msg'] = 'Solución eliminado con exito'
            return HttpResponseRedirect('solutions')
        except Fail.DoesNotExist:
            return HttpResponseRedirect('/')


def edit_solution(request):
    if request.method == 'POST':
        try:
            solution = Solution.objects.get(id=request.POST['id'])
            solution.name = request.POST['name']
            solution.save()
            request.session['msg'] = 'Solución editado con exito'
            return HttpResponseRedirect('solutions')
        except Fail.DoesNotExist:
            return HttpResponseRedirect('/')


def simulator_process(request):
    process = Process.objects.all()
    return render(request, 'process_simulator.html', {'process': process})


def fail_simulator(request):
    if 'id' in request.GET:
        request.session['process'] = request.GET['id']
        return HttpResponseRedirect('similator')


def view_simulator(request):
    iniciar_fallos()
    process = Process.objects.get(id=request.session['process'])
    fails = Fail.objects.filter(process=process)
    solutions = Solution.objects.all()
    steps = Step.objects.all().order_by('id')
    return render(request, 'fail_simulator.html', {'process': process, 'fails': fails, 'solutions': solutions,
                                                   'steps': steps, 'alarma': alarma[1], 'salida_auxiliar': alarma[0], 'salida_auxiliar2': alarma[7]
                                                   })


#ejecuta la falla presentada en la vista
def eject_fail(request):
    if 'id' in request.GET:
        fail = Fail.objects.get(id=request.GET['id'])
        fail.activo = True
        fail.save()
        for i in range(0, 12):
            try:
                if classes[i].pin == fail.pin:
                    classes[i].led.on()
                    break
            except UnboundLocalError:
                pass
            except IndexError:
                pass
        
        if not alarma[0]:
            alarma[0] = True
            alarma[1] = True
            alarma[2].on()
            alarma[7] = True
            alarma[6].on()
            th = Thread(target=run_alarm)
            th.start()

        return HttpResponseRedirect('similator')


#apaga la falla
def off_fail(request):
    if 'id' in request.GET:
        fail = Fail.objects.get(id=request.GET['id'])
        fail.activo = False
        fail.save()        
        for i in range(0, 12):
            try:
                if classes[i].pin == fail.pin:
                    classes[i].led.off()
                    break
            except UnboundLocalError:
                pass
            except IndexError:
                pass
        if len(Fail.objects.filter(activo=True)) == 0:
            alarma[1] = False
            alarma[0] = False
            alarma[2].off()
            alarma[7] = False
            alarma[6].off()
        return HttpResponseRedirect('similator')


def view_step(request):
    if 'solution' in request.session:
        solution = Solution.objects.get(id=request.session['solution'])
        steps = Step.objects.filter(solution=solution)

        if 'msg' in request.session:
            msg = request.session['msg']
            del request.session['msg']
            return render(request, 'step.html', {'solution': solution, 'steps': steps, 'msg': msg.encode('utf-8')})

        return render(request, 'step.html', {'solution': solution, 'steps': steps})


def solution_step(request):
    if 'id' in request.GET:
        request.session['solution'] = request.GET['id']
        return HttpResponseRedirect('step')


def add_step(request):
    if request.method == 'POST':
        solution = Solution.objects.get(id=request.POST['solution'])
        step = Step()
        step.solution = solution
        step.name = request.POST['name']
        step.save()
        request.session['msg'] = 'Paso guardado con exito'
        return HttpResponseRedirect('step')


def edit_step(request):
    if request.method == 'POST':
        step = Step.objects.get(id=request.POST['id'])
        step.name = request.POST['name']
        step.save()
        request.session['msg'] = 'Paso editado con exito'
        return HttpResponseRedirect('step')


def detector_process(request):    
    process = Process.objects.all()
    return render(request, 'process_detection.html', {'process': process})


def fail_detection(request):
    if 'id' in request.GET:
        request.session['process'] = request.GET['id']
        return HttpResponseRedirect('detector')


def view_detector(request):
    iniciar_fallos()
    process = Process.objects.get(id=request.session['process'])
    fails = Fail.objects.filter(process=process)
    solutions = Solution.objects.all()
    steps = Step.objects.all().order_by('id')
    return render(request, 'fail_detection.html',
                  {'process': process, 'fails': fails, 'solutions': solutions, 'steps': steps, 'alarma': alarma[1], 'salida_auxiliar': alarma[0], 'salida_auxiliar2': alarma[7]})


def get_fails_detection(request):
    if 'id' in request.GET:
        process = Process.objects.get(id=request.GET['id'])
        fails = Fail.objects.filter(process=process)
        if len(Fail.objects.filter(process=process, activo=True)) > 0:
            if not alarma[1] and not alarma[0] and not alarma[3]:
                alarma[0] = True
                alarma[7] = True
                alarma[1] = True
                alarma[3] = True
                alarma[2].on()
                alarma[6].on()
                th = Thread(target=run_alarm)
                th.start()
        else:
            if alarma[1] or alarma[0] or alarma[5]:
                alarma[1] = False
                if not alarma[5]:
                    alarma[0] = False
                    alarma[7] = False
                    alarma[2].off()
                    alarma[6].off()
            alarma[3] = False

        if len(fails) > 0:
            data = serializers.serialize('json', fails, fields=('activo'))
            return HttpResponse(data, content_type='application/json')
        else:
            return HttpResponse('not')


def get_estado_alarma(request):
    if alarma[0] and alarma[1] and alarma[7]:
        return HttpResponse('on')#prendidas las tres
    elif alarma[0] and alarma[7]:
        return HttpResponse('0')#prendida los dos auxiliares
    elif alarma[1] and alarma[0]:
        return HttpResponse('1')#prendida la alarma y el aux 1
    elif alarma[7] and alarma[1]:
        return HttpResponse('2')#prendida la alarma y el aux 2
    elif alarma[1]:
        return HttpResponse('3')#prendida la alarma
    elif alarma[0]:
        return HttpResponse('4')#prendida aux1
    elif alarma[7]:
        return HttpResponse('5')#prendida aux2    
    else:
        return HttpResponse('off')#apagadas las tes


def run_alarm():
    while alarma[1]:
        #os.system('aplay '+ ruta_alarma + '/Entrenador/static/audio/alarm3.wav')
        #sleep(8)
        pass
    print 'se apago la alarma'


def off_alarm(request):
    alarma[1] = False
    return HttpResponse('ok') 
    

def on_auxiliar(request):
    alarma[5] = True
    alarma[0] = True
    alarma[2].on()
    return HttpResponse('ok')


def off_auxiliar(request):
    if not alarma[7]:
        alarma[5] = False
    alarma[0] = False
    alarma[2].off()
    return HttpResponse('off')


def on_auxiliar2(request):
    alarma[5] = True
    alarma[7] = True
    alarma[6].on()
    return HttpResponse('ok')


def off_auxiliar2(request):
    if not alarma[0]:
        alarma[5] = False
    alarma[7] = False
    alarma[6].off()
    return HttpResponse('off')
