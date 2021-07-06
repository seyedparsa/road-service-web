from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from core.forms import AssignModeratorForm
from core.models import CountyExpert, Serviceman, Location, Region, CountryModerator, ProvinceModerator
from core.serializers import IssueAcceptanceSerializer, LocationSerializer


class AcceptIssue(APIView):
    def post(self, request, format=None):
        serializer = IssueAcceptanceSerializer(data=request.data)
        if serializer.is_valid():
            issue = serializer.validated_data['issue']
            mission_type = serializer.validated_data['mission_type']
            speciality_requirements = [tuple(sr.values())
                                       for sr in serializer.validated_data['speciality_requirements']]
            machinery_requirements = [tuple(mr.values())
                                      for mr in serializer.validated_data['machinery_requirements']]
            # TODO: select the corresponding county expert (this is for EAB)
            county_expert = CountyExpert.objects.all()[0]
            result = county_expert.accept_issue(issue, mission_type, speciality_requirements, machinery_requirements)
            return Response(result)
        return Response(serializer.error_messages)


class UpdateLocation(APIView):
    def post(self, request, format=None):
        # TODO: select the corresponding serviceman (this is for EAB)
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            lat = serializer.validated_data['lat']
            long = serializer.validated_data['long']
            service_man = Serviceman.objects.all()[0]
            service_man.update_location(Location(lat, long))
            return Response("Updated!")
        return Response(serializer.error_messages)


class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request=request,
                      template_name='core/dashboard.html')


class IssueCard(View):
    def get(self, request, *args, **kwargs):
        issue_id = kwargs['issue_id']
        context = {'card': issue_id}
        return render(request=request,
                      template_name='core/issuecard.html', context=context)

    def post(self, request, *args, **kwargs):
        issue_id = kwargs['issue_id']
        context = {'card': issue_id}
        return render(request=request,
                      template_name='core/issuecard.html', context=context)


class TeamDetails(View):
    def get(self, request, *args, **kwargs):
        team_id = kwargs['team_id']
        context = {'team': team_id}
        return render(request=request,
                      template_name='core/teamdetails.html', context=context)

    def post(self, request, *args, **kwargs):
        team_id = kwargs['team_id']
        context = {'team': team_id}
        return render(request=request,
                      template_name='core/teamdetails.html', context=context)


class ChangeTeam(View):
    def get(self, request, *args, **kwargs):
        team_id = kwargs['team_id']
        context = {'team': team_id}
        return render(request=request,
                      template_name='core/changeteam.html', context=context)

    def post(self, request, *args, **kwargs):
        team_id = kwargs['team_id']
        context = {'team': team_id}
        return render(request=request,
                      template_name='core/changeteam.html', context=context)


class ChangeMission(View):
    def get(self, request, *args, **kwargs):
        mission_id = kwargs['mission_id']
        context = {'mission': mission_id}
        return render(request=request,
                      template_name='core/changemission.html', context=context)

    def post(self, request, *args, **kwargs):
        mission_id = kwargs['mission_id']
        context = {'mission': mission_id}
        return render(request=request,
                      template_name='core/changemission.html', context=context)



class ChangeSpeciality(View):
    def get(self, request, *args, **kwargs):
        speciality_id = kwargs['speciality_id']
        context = {'speciality': speciality_id}
        return render(request=request,
                      template_name='core/changespeciality.html', context=context)

    def post(self, request, *args, **kwargs):
        speciality_id = kwargs['speciality_id']
        context = {'speciality': speciality_id}
        return render(request=request,
                      template_name='core/changespeciality.html', context=context)


class AssignModerator(View):
    def get(self, request, *args, **kwargs):
        assign_moderator_form = AssignModeratorForm()
        return render(request=request,
                      template_name='core/assignmoderator.html',
                      context={'form': assign_moderator_form})

    def post(self, request, *args, **kwargs):
        form = AssignModeratorForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            region_id = int(form.cleaned_data['region'])
            region = form.region_instances[region_id]
            user_id = form.cleaned_data['user']
            user = User.objects.get(id=user_id)
            if region.type == Region.Type.PROVINCE:
                CountryModerator.assign_province_moderator(user, region)
            else:
                ProvinceModerator.assign_county_moderator(user, region)
            messages.add_message(request, messages.INFO, 'دسترسی داده شد!')
        else:
            print('invalid form!')
        messages.add_message(request, messages.INFO, 'دسترسی داده شد!')
        return render(request=request,
                      template_name='core/assignmoderator.html',
                      context=context)


class ResourcesView(View):
    def get(self, request, *args, **kwargs):
        return render(request=request,
                      template_name='core/resources.html')

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'جدول بروز شد!')
        return render(request=request,
                      template_name='core/resources.html')


