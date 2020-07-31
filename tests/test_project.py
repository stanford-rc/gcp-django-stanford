from django.test import TestCase
from gcpdjango.apps.main.models import Project


class ProjectTestCase(TestCase):
    def setUp(self):
        """Do creation of models here"""
        Project.objects.create(
            name="Dinosaur Project", description="This is a project for dinosaurs"
        )

    def test_projects(self):
        """Write tests for your project hers."""
        project = Project.objects.get(name="Dinosaur Project")
        self.assertEqual(project.get_label(), "project")