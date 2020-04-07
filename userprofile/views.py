from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from accounts.models import User
from . forms import ProfileUpdateForm
from userprofile.models import Profile
from userprofile.forms import UserUpdateForm
from django.contrib import messages



class TimelineView(DetailView):
    model = User
    template_name = "profile/user-profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"
    object = None
    
    


    def get_object(self, queryset=None):
        
        return self.model.objects.select_related('profile').prefetch_related("posts").get(username=self.kwargs.get(self.slug_url_kwarg))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


# class ProfileEditView(UpdateView):
#     model = Profile
#     template_name = "profile/edit-my-profile.html"
#     context_object_name = "profile"
#     object = None
    

#     def get_object(self, queryset=None):
#         return self.request.user.profile

#     def post(self, request, *args, **kwargs):
#         p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
#         print(request.POST.get('first_name'))
#         user = request.user
#         user.first_name = request.POST.get('first_name')
#         user.last_name = request.POST.get('last_name')
#         user.about = request.POST.get('about')
#         if request.POST.get('gender') == "male":
#             user.gender = "male"
#         else:
#             user.gender = "female"
#         user.save()
#         profile = user.profile
#         profile.country = request.POST.get('country')
#         profile.city = request.POST.get('city')
#         profile.phone = request.POST.get('phone')
#         profile.profile_image = request.POST.get('profile_image')
#         profile.save()
#         return redirect(reverse_lazy('profile:edit-profile'))

def ProfileEditView(request):
    if(request.method=='POST'):

        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if(p_form.is_valid() and u_form.is_valid()):
            p_form.save()
            u_form.save()
            messages.success(request, 'Your Account Successfully Updated')
            return redirect('core:home')
    else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form':u_form,'p_form':p_form}
    return render(request, "profile/edit-my-profile.html",context)
