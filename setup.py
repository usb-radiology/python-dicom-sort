import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dicom-sort", # Replace with your own username
    version="0.0.1",
    author="Francesco Santini",
    author_email="francesco.santini@gmail.com",
    description="Dicom sort utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    install_requires=['pydicom', 'progress'],
    extras_require={'GUI': ['PySide2']},
    scripts=['dicom_sort'],
    packages=['DcmMvLib'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)