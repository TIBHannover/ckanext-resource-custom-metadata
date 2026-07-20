# ckanext-resource-custom-metadata

The ckan extension for adding a set of new metadata for a data resource in ckan. 


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
|  2.10 | Yes    |
|  2.9 | No |
| earlier | No |           |


## Installation

To install ckanext-resource-custom-metadata:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

        > git clone https://github.com/TIBHannover/ckanext-resource-custom-metadata.git
        > cd ckanext-resource-custom-metadata
        > pip install -r requirements.txt
        > pip install -e .

3. Add `resource_custom_metadata` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

        sudo service supervisor reload
        sudo service nginx reload



## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini --cov=ckanext.resource_custom_metadata --disable-warnings ckanext/resource_custom_metadata



## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
