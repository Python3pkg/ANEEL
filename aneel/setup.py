# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="aneel",
    version="0.0.1",
    url="https://github.com/mstuttgart/codigo-avulso-test-tutorial",
    license="MIT License",
    author="Renato Eduardo Farias de Sousa",
    author_email="renato.ef.sousa@gmail.com",
    keywords="aneel cálculos regulamentos",
    description=u"Esse pacote realiza diversos cálculos relacionados a regulamentos da ANEEL",
    packages=["aneel"],
    install_requires=["csv", "json"],
)
