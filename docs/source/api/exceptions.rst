.. currentmodule:: ultra_piston.errors

Exceptions
==========

.. note::
  The exception hierarchy of this library is illustrated as so-
  
  * BasePistonError
      * InternalError
          * MissingDataError
      * ServerError
          * TooManyRequests
          * InternalServerError
          * NotFoundError
          * UnexpectedStatusError

.. autoclass:: BasePistonError
    :members:

.. autoclass:: InternalError
    :members:

.. autoclass:: ServerError
    :members:

.. autoclass:: MissingDataError
    :members:

.. autoclass:: TooManyRequests
    :members:

.. autoclass:: InternalServerError
    :members:

.. autoclass:: NotFoundError
    :members:

.. autoclass:: UnexpectedStatusError
    :members: