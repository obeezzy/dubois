import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name='dubois',
        version='0.1',
        author='Chronic Coder',
        author_email='efeoghene.obebeduo@gmail.com',
        description='A DIY robot',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='MIT',
        packages=setuptools.find_packages('.'),
)
