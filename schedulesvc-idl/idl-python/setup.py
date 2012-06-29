#!/usr/bin/env python

from distutils.core import setup

setup(name='trschedulesvc',
      version='${project.version}',
      description='Tech Residents Service',
      packages=['trschedulesvc',
                'trschedulesvc.gen']
    )

