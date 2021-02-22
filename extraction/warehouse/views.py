from django.urls import reverse, reverse_lazy

# Create your views here.

from django.views.generic import CreateView, UpdateView
from .models import  UserRequest
from .forms import UserRequestForm
from .tasks import initiate_crawler_async

from django.contrib.messages.views import SuccessMessageMixin


class UserRequestCreate(SuccessMessageMixin, CreateView):
    model = UserRequest
    form_class = UserRequestForm
    template_name = 'warehouse/index.html'

    success_message = "Crawler Initiated for Url Id -%(id)s. Please check the Dashboard"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            id=self.object.id,
        )

    def get_success_url(self):
        return reverse_lazy('user_request')


    def initiate_crawler(self, object):
        """
        Apply Async Approach to remove blockade
        Just Initiate the Crawler that crawls the URL's
        from this URL and store them to Database
        """
        kwargs = {
            'input_url': object.input_url,
            'id': object.id
        }
        initiate_crawler_async.apply_async(kwargs=kwargs, queue='initiate_crawler')
        return True

    def form_valid(self, form):

        self.object = form.save()
        self.initiate_crawler(object=self.object)
        return super(UserRequestCreate, self).form_valid(form)

