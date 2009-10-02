from setuptools import setup, find_packages
import os

version = '1.26.1'

setup(name='Products.RhaptosSite',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Rhaptos developers',
      author_email='rhaptos@cnx.rice.edu',
      url='http://rhaptos.org',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',

          # 3rd party dependencies : those eggs are insidedist.rhaptos.org
          'Products.AdvancedQuery==2.2-rhaptosdev-r30378',
          'Products.Five==1.4.4-rhaptosdev-r30378',
          'Products.LocalFS==1.7-rhaptosdev-r30378',
          'Products.ManagableIndex==1.7.3-rhaptosdev-r30378',
          'Products.MasterSelectWidget==0.2.3-rhaptosdev-r30378',
          'Products.NoHeaderFieldContinuation==0.1-rhaptosdev-r30378',
          'Products.OFolder==1.0-rhaptosdev-r30378',
          'Products.Ploneboard==1.1-rhaptosdev-r30378',
          'Products.References==0.10-rhaptosdev-r30378',
          'Products.SimpleAttachment==3.0.1-rhaptosdev-r30378',
          'Products.ZPsycopgDA==1.11-rhaptosdev-r30378',
          'Products.ExternalFile==0.1-rhaptosdev-r30470',
          'Products.ExternalStorage',

          # Rhaptos core dependencies
          'Products.CatalogMemberDataTool',
          'Products.CMFDiffTool',
          'Products.CNXMLDocument',
          'Products.CNXMLTransforms',
          'Products.ExtZSQL',
          'Products.FSImportTool',
          'Products.Lensmaker',
          'Products.LensOrganizer',
          'Products.LinkMapTool',
          'Products.MathEditor',
          'Products.RhaptosBugTrackingTool',
          'Products.RhaptosCacheTool',
          'Products.RhaptosCollaborationTool',
          'Products.RhaptosCollection',
          'Products.RhaptosContent',
          'Products.RhaptosForums',
          'Products.RhaptosHitCountTool',
          'Products.RhaptosModuleEditor',
          'Products.RhaptosModuleStorage',
          'Products.RhaptosPatchTool',
          'Products.RhaptosPDFLatexTool',
          'Products.RhaptosPrint',
          'Products.RhaptosRepository',
          'Products.RhaptosSimilarityTool',
          'Products.RhaptosWorkgroup',
          'Products.UniFile',
          'Products.XMLTemplateMaker',
          'Products.ZAnnot',

      ],
      tests_require = [
           'zope.testing>=3.5',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

