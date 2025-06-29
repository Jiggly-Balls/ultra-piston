Guide
=====

To get started with this library first create a new project and create a
virtual environment & activate it (optional but recommended). Once you've done
that you may continue.

Installation
------------

Install ``ultra_piston`` through pip in your terminal-

.. code-block:: console

   (.venv) $ pip install ultra_piston

Using the Library
-----------------

.. note::
   This library provides both synchronous and asynchronous methods out of the box.
   To use the asynchronous variant of a method, simply append ``_async`` to the
   name of its synchronous counterpart.

Obtaining all the available runtime languages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pprint import pprint

   from ultra_piston import PistonClient

   piston = PistonClient()  # Creating an instance with default settings

   runtimes = piston.get_runtimes()
   # Getting all languages' runtime data

   pprint(runtimes)

   available_languages: list[str] = [runtime.language for runtime in runtimes]
   # Extracting only the available language names from the list of all
   # available runtimes along with their versions 
   
   pprint(available_languages)

Executing code via Piston API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pprint import pprint

   from ultra_piston import File, PistonClient

   piston = PistonClient()

   # Creating a File object containing the code.
   code_file = File(
      name="test.py",  # Name of the file (optional)
      content='print("Hello world")',  # The code to be executed
   )

   executed_state = piston.post_execute("python3", "3.10.0", code_file)
   pprint(executed_state)  # The entire ExecutionOutput object containing various data

   code_output = executed_state.run.output
   print(code_output)  # The executed output of the code

.. :toctree::

   api