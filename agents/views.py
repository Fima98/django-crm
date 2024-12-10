import random
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views import generic
from django.urls import reverse
from django.contrib.auth import get_user_model

from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin


User = get_user_model()

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile,
        )
        send_mail(
            subject="You are invited to be an agent",
            message="Go to the site to see the new lead",
            from_email=self.request.user.email,
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)
    

class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)




class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_object(self):
        agent_id = self.kwargs.get('pk')
        agent = get_object_or_404(Agent, pk=agent_id)
        if agent.organisation != self.request.user.userprofile:
            raise Http404("You do not have permission to update this agent.")
        
        return agent

    def get_success_url(self):
        return reverse_lazy('agents:agent-list')

    def get_initial(self):
        agent = self.get_object()
        return {
            'email': agent.user.email,
            'username': agent.user.username,
            'first_name': agent.user.first_name,
            'last_name': agent.user.last_name,
        }

    def form_valid(self, form):
        agent = self.get_object()  
        user = agent.user  
        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        
        if not isinstance(user, User):
            raise ValueError("Expected a User instance, but got something else.")
        user.save()
        agent.save()
        return super().form_valid(form)





