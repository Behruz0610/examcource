from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Module, ModuleComment, ModuleRating
from django.contrib import messages

@login_required
def add_module_comment(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == "POST":
        comment = request.POST.get("comment")
        if comment:
            ModuleComment.objects.create(module=module, user=request.user, comment=comment)
            messages.success(request, "Comment added!")
        return redirect('module_detail', module_id=module.id)
    return render(request, "modules/add_comment.html", {"module": module})

@login_required
def add_module_rating(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        if rating and rating.isdigit():
            ModuleRating.objects.create(module=module, user=request.user, rating=int(rating))
            messages.success(request, "Rating added!")
        return redirect('module_detail', module_id=module.id)
    return render(request, "modules/add_rating.html", {"module": module})