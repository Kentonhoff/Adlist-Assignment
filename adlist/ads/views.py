##just finish adding the templates, step #3 is complete
from ads.models import Ad, Comment
from ads.forms import CreateForm, CommentForm

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class AdListView(OwnerListView):
    model = Ad
    template_name = "ad_list.html"

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ad_detail.html"
    def get(self, request, pk) :
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : ad, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class AdFormView(LoginRequiredMixin, View):
    template = "ad_form.html"
    success_url = reverse_lazy("ads")
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
            form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = "ad_delete.html"

def stream_file(request, pk) :
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment_form = CommentForm(request.POST)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse_lazy('ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "comment_delete.html"

    def get_success_url(self):
        ad = self.object.ad
        return reverse_lazy('ad_detail', args=[ad.id])
