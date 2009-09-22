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
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'elementtree',
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

