.. _contributing:

==================
Contributors Guide
==================

Ways to Contribute
==================

Ways to Contribute Documentation and/or Code
--------------------------------------------

* Tackle any issue that you wish! Some issues are labeled as **"good first issues"** to
  indicate that they are beginner friendly, meaning that they don't require extensive
  knowledge of the project.
* Make a tutorial or gallery example of how to do something.
* Improve the API documentation.
* Contribute code! This can be code that you already have and it doesn't need to be
  perfect! We will help you clean things up, test it, etc.

Ways to Contribute Feedback
---------------------------

* Provide feedback about how we can improve the project or about your particular use
  case. Open an `issue <https://github.com/NickleDave/vakt/issues>`_ with
  feature requests or bug fixes.
* Help triage issues, or give a "thumbs up" on issues that others reported which are
  relevant to you (using the
  `"Add Your Reaction" icon <https://github.blog/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/>`_).

Ways to Contribute to Community Building
----------------------------------------

* Cite ``vak`` when using the project.
  Please see `the CITATION.cff <https://github.com/NickleDave/vak/blob/main/CITATION.cff>`_ file for details.
  To obtain a citation in APA or BibTEX format, click on "Cite this repository" on the
  `GitHub repository <https://github.com/NickleDave/vak>`_.
* Spread the word about ``vak`` and star the project on GitHub!

Providing Feedback
==================

Two of the main ways to contribute are to report a bug or to request a feature.
Both can be done by opening an `Issue <https://github.com/NickleDave/vak/issues>`_
on GitHub and filling out the template.

* Find the `Issues <https://github.com/NickleDave/vak/issues>`_ tab on the
  top of the GitHub repository and click *New Issue*.
* Choose a template based on the type of feedback

  * For a bug report, click on *Get started* next to *Bug report*.

  * For a feature request, click on *Get started* next to *Feature request*.

* **Please try to fill out the template with as much detail as you can**.
* After submitting your bug report or feature request,
  try to answer any follow up questions as best as you can.

General Guidelines
==================

.. _getting-help:

Getting Help
------------

Discussion often happens on GitHub issues and pull requests. In addition, there is a
`Discourse forum <https://forum.vocles.org/>`_ for
the project where you can ask questions.

.. _dev-workflow:

Workflow for Contributing
-------------------------

We follow the `GitHub pull request workflow <http://www.asmeurer.com/git-workflow>`_
to make changes to our codebase. Every change made goes through a pull request, even
our own, so that our
`continuous integration <https://the-turing-way.netlify.app/reproducible-research/ci.html>`_
services have a chance to check that the code is up to standards and passes all
our tests. This way, the *main* branch is always stable.

For New Contributors
####################

Please take a look at these resources to learn about Git and pull requests:

* `How to Contribute to Open Source <https://opensource.guide/how-to-contribute/>`_.
* `Git Workflow Tutorial <http://www.asmeurer.com/git-workflow/>`_ by Aaron Meurer.
* `How to Contribute to an Open Source Project on GitHub <https://egghead.io/courses/how-to-contribute-to-an-open-source-project-on-github>`_.

And please don't hesitate to :ref:`ask questions <getting-help>`.


Writing commit messages
#######################

We follow the convention of beginning a ``git`` commit message
with an abbreviation that indicates the reason for the commit.
This convention is used by several Python data science libraries.
The standard abbreviations we use to start the commit message with are

    .. include:: commit-abbreviations.rst

.. _dev-env:

Setting up a development environment
====================================

This section describes how to set up an environment for development.
This is the steps the maintainers follow, and it can also be used by contributors.

You will need:
~~~~~~~~~~~~~~
1. the version control tool ``git``
  (you can install ``git`` from `Github <https://help.github.com/en/github/getting-started-with-github/set-up-git>`_,
  with your operating system package manager, or using ``conda``.)
2. ``make`` (installed by default on most Unix systems, not available on Windows)
  Here is an introduction to ``make`` from the Turing Way:
  https://the-turing-way.netlify.app/reproducible-research/reproducible-research.html

Steps
~~~~~

1. Clone the repository
#######################

Clone the repository from Github using ``git``

.. code-block:: shell

   git clone https://github.com/NickleDave/vak

2. Create a virtual environment
###############################

The repository includes a Makefile that automates setting up a development environment.

To create a virtual environment, run the following:

.. code-block:: shell

   make venv

You can then activate the virtual environment by executing:

.. code-block:: shell

   . ./.venv/activate

on MacOS and Linux, or

.. code-block:: shell

   ./.venv/activate.bat

on Windows.

3. Download test data
######################

There are three types of data of needed for tests.

1. **``.toml`` configuration files.**  These are under version control,
so you will already have them when you clone the repository

The other two types of data are made up of files
that are too large to keep in a GitHub repository.
Instead, the files are kept on a public
`Open Science Framework <https://osf.io>`_ project, here:
https://osf.io/vz48c/

There are commands in the Makefile that download this data.

The two other types of data for tests are:

2. "source" data, that consists of files used as input to ``vak``
such as audio and annotation files. These files are less likely to change
as ``vak`` develops, so they are kept separate.

To download these files, run:

.. code-block:: shell

   make test-data-download-source

3. "generated" data, that consists of files created by ``vak``,
such as .csv files that represent datasets, and the saved neural network
checkpoints.

These files are generated by a script: ``./tests/scripts/generate_data_for_tests.py``.
Generally speaking, the core maintainers are the only ones that should need
to run this script.

To download these files, run:

.. code-block:: shell

   make test-data-download-generated

4. Proceed with development
###########################

After completing these steps, you are ready for development!

Contributing Code
=================

``vak`` Code Overview
---------------------

The source code for ``vak`` is located in the directory ``./src/vak``. When contributing
code, be sure to follow the general guidelines in the
:ref:`dev-workflow` section.

Code Style
----------

In general, ``vak`` code should

* follow the `Zen of Python <https://www.python.org/dev/peps/pep-0020/#id2>`_ in terms of implementation
* follow the `PEP8 style guide <https://www.python.org/dev/peps/pep-0008/>`_ for code
* follow the `numpy standard for docstrings <https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_

We also use the tool `Black <https://github.com/psf/black>`_ to format the code, so we don't have to think about it.

Testing your Code
-----------------

Automated testing helps ensure that our code is as free of bugs as it can be.
It also lets us know immediately if a change we make breaks any other part of the code.

All of our test code and data are stored in the directory ``./tests``,
that is set up as if it were a Python package.
We use the `pytest <https://pytest.org>`_ framework to run the test suite.
To run the entire test suite, run ``pytest`` from the command line:

.. code-block:: shell

   pytest

You can also run tests in just one test script using:

.. code-block:: shell

   pytest ./tests/NAME_OF_TEST_FILE.py

Please write tests for your code so that we can be sure that it won't break any of the
existing functionality.
Tests also help us be confident that we won't break your code in the future.

If you're **new to testing**, see existing test files for examples of things to do.
**Don't let the tests keep you from submitting your contribution!**
If you're not sure how to do this or are having trouble, submit your pull request
anyway.
We will help you create the tests and sort out any kind of problem during code review.
It's OK if you can't or don't know how to test something.
Leave a comment in the pull request and we'll help you out.
