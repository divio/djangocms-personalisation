Django CMS Personalisation
==========================

Installation
------------

At this time, the package is not submitted to PyPi, but you can still use pip
if you like. Here's how to get started quickly:

Requirements:
- python 2.7+ or 3.5+
- Django 1.8+
- django CMS 3.5+

1. If you're using Python 3, it is recommended also install:
   `pip intall pyuca` for better collation of non-EN languages.
1. `pip install https://github.com/divio/djangocms-personalisation/archive/master.zip`
1. Add 'djangocms_personalisation' to INSTALLED_APPS in your Django project's settings file
1. `python manage.py migrate djangocms_personalisation`

Optional, but required if you intend to run the test project included in the
repo:

1. `pip install django-easy-select2` (if you opt not to do this, you must
    remove `'easy_select2'` from settings.INSTALLED_APPS in the test_project)

At this point you should be good to go. When you next run your project, the
first thing you may notice is that you have new–albeit empty–'Personalise' menu
in your toolbar.


Basic Usage
-----------

To use personalisation, you simply add Personalisation plugins into your
placeholders. The most important one is the Personalise plugin. This
serves as a container for all other personalisation plugins. Once you
add a Limit plugin to a placeholder, you'll then notice you have other
plugins that you can then install as children to the limit plugin.


Description
-----------

This django CMS application allows the CMS operator to display different
content to different "traits" of visitors.

By using different Personalisation Plugins, the CMS operator can define
rules which meet certain criteria, such as:

* Authenticated: Visitor has a valid session
* Retail Customer: Visitor presented a cookie named 'customer_type' with a
  value of 'retail'
* Offer Valid in Region: Visitor's IP address is thought to be in France

In addition, in order to aide the operator in providing "Fallbacks" when
conditions aren't met and other scenarios, this application provides a
"Personalise" plugin, which can be used to limit the number of
matching conditions that will display in any given placeholder.

Combining a Personalisation plugins can be use to create arbitrarily
complex logical conditions can be described. Here's the basics:

"Show details of 10% discount offer to retail customers only."

````
	> placeholder
		> Personalise: Show first
			> by Cookie: 'type' equals 'retail'
				> Text: 10% Discount offer...
			> Text: Details of offer with normal pricing...
````

In this example, the Personalise Plugin will only allow one of its children to be
displayed. If the "by Cookie" plugin is triggered because the visitor
has a cookie named 'type' with a value of 'retail', then the contained
plugins (all of them) will be displayed.

If the visitor does not have a 'type' cookie, or it does not contain 'retail',
then the "by Cookie" plugin will not be considered for rendering, nor
will any of its children. This will then permit consideration of the next
child. In this case, it is a normal, non-personalisation plugin
that will "count" for the limit of 1 and will be rendered.

In a similar manner, multiple conditions can be considered and combined with
AND, OR or XOR operations as required. Here's an OR operation:

````
	> placeholder
		> Personalise: Show first
			> by Cookie: 'type' equals 'retail'
				> Text: 10% offer for French customers OR retail customers only.
			> by Country: France
				> Text: 10% offer for French customers OR retail customers only.
			> Text: Normal pricing for everyone else...
````

An AND operation is a little more complex, but still very easy to do:

````
	> placeholder
		> Personalise: Show first
			> by Cookie: 'type' equals 'retail'
				> Personalise: Show first
					> by Country: France
						> Text: 10% offer for French Retail Customers only.
					> Text: Normal pricing...
			> Text: Normal pricing...
````

An XOR operation is also straight forward:

````
	> placeholder
		> Personalise: Show first
			> by Cookie: 'type' equals 'retail'
				> Limit Block: Show first
					> by Country: France
						> Text: Normal pricing...
					> Text: 10% offer for French customers OR retail customers only
					        (but not French retail customers).
			> by Country: France
				> Personalise: Show first
					> by Cookie: 'type' equals 'retail'
						> Text: Normal pricing...
					> Text: 10% offer for French customers OR retail customers only
					        (but not French retail customers).
			> Text: Normal pricing...
````
