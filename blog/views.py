from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal
from .models import Equipement

def animal_list(request):
    animaux = Animal.objects.all()
    return render(request, 'animalerie/animal_list.html', {'animaux' : animaux})

def animal_detail(request, id_animal):
    message = ''
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    ancien_etat = animal.etat
    form=MoveForm(request.POST, instance = animal) 
    if form.is_valid():
        variable = 0
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        if nouveau_lieu.disponibilite == 'libre':
            if nouveau_lieu.id_equip == 'mangeoire' : 
                if ancien_etat == 'affamé' : 
                    animal.etat = 'repus'
                    animal.save()
                    variable = 1
            if nouveau_lieu.id_equip == 'roue' : 
                if ancien_etat == 'repus' : 
                    animal.etat = 'fatigué'
                    animal.save()
                    variable = 1
            if nouveau_lieu.id_equip == 'nid' : 
                if ancien_etat == 'fatigué' : 
                    animal.etat = 'endormi'
                    animal.save()
                    variable = 1
            if nouveau_lieu.id_equip == 'litiere' : 
                if ancien_etat == 'endormi' : 
                    ancien_lieu.disponibilite = 'libre'
                    ancien_lieu.save
                    animal.etat = 'affamé'
                    animal.save()
                    variable = 1
        if variable == 1 :
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            if nouveau_lieu.id_equip != 'litiere' :
                nouveau_lieu.disponibilite = "occupé" 
                nouveau_lieu.save()
            return redirect('animal_detail', id_animal=id_animal)
        else :   
            message = "Cela ne fonctionne pas"
    form = MoveForm()
    return render(request,
              'animalerie/animal_detail.html',
              {'animal': animal, 'lieu': ancien_lieu, 'form': form, 'message' : message})