# Get the home page 
import json

from wagtail.core.models import Page
from blog.models import ProjectDetailPage, PartnerDetailPage
from blog.models import BlogCategory
from wagtail.images.models import Image
# import sl
from datetime import datetime


project_page = Page.objects.get(slug="projects")

# Read a json file into a python object and parse it to the ProjectDetailPage
with open('projects.json') as json_file:
    projects = json.load(json_file)
    for project in projects['main_project']:
        print(project['title'])        
        projectdetailpage = ProjectDetailPage(title=project['title'], intro=project['long_name'], category=BlogCategory.objects.get(slug='projects'), card_image = Image.objects.get(title='image-1'),
                                heading_image = Image.objects.get(title='image-1'), call_id=project['call'], 

                                start_date= datetime.strptime(project['pub_date'], '%Y-%m-%d %H:%M:%S').date(), 
                                path=3, depth=2)
        project_page.add_child(instance=projectdetailpage)

        projectdetailpage.save()
        project_page.save()        
        richtext = json.dumps([ {'type': 'richtext', 'value': project['snippet']}, 
                                {'type': 'richtext', 'value': project['body']}])        
        projectdetailpage.content = richtext
        projectdetailpage.save()

partner_page = Page.objects.get(slug="partners")


## Read a json file into a python object and parse it to the ProjectDetailPage
with open('partners.json') as json_file:
    partners = json.load(json_file)
    for partner in partners['main_partner']:
        print(partner['name'])        

        partnerdetailpage = PartnerDetailPage(title=partner['name'], category=BlogCategory.objects.get(slug='partners'), card_image = Image.objects.get(title='image-1'),
                                heading_image = Image.objects.get(title='image-1'), path=3, depth=2)
        partner_page.add_child(instance=partnerdetailpage)
        partnerdetailpage.save()
        partner_page.save()
        richtext = json.dumps([{'type': 'richtext', 'value': partner['body']}])
        partnerdetailpage.content = richtext
        partnerdetailpage.save()

## Read a json file into a python object and parse it to the ProjectDetailPage
with open('news.json') as json_file:
    partners = json.load(json_file)
    for partner in partners['main_partner']:
        print(partner['name'])        

        partnerdetailpage = PartnerDetailPage(title=partner['name'], category=BlogCategory.objects.get(slug='partners'), card_image = Image.objects.get(title='image-1'),
                                heading_image = Image.objects.get(title='image-1'), path=3, depth=2)
        partner_page.add_child(instance=partnerdetailpage)
        partnerdetailpage.save()
        partner_page.save()
        richtext = json.dumps([{'type': 'richtext', 'value': partner['body']}])
        partnerdetailpage.content = richtext
        partnerdetailpage.save()
