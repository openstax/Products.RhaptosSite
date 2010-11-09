from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read("Products", "RhaptosSite", "version.txt").strip()

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
          'Products.MasterSelectWidget',
          'Products.NoHeaderFieldContinuation==0.1-rhaptosdev-r30378',
          'Products.Ploneboard',
          'Products.References==0.10-rhaptosdev-r30378',
          'Products.SimpleAttachment==3.5',
          'Products.ZPsycopgDA==2.0.13-enfold',
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
          'Products.ZAnnot',
          'Products.Lineup',
          'Products.RhaptosSword',

          # Unit tests dependencies
          'Products.RhaptosTest',

      ],
      tests_require = [
           'zope.testing>=3.5',
           'Products.RhaptosTest',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

