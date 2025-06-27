.. currentmodule:: ultra_piston.errors

Exceptions
==========

.. note::
  The exception hierarchy of this library is illustrated as so-
  
  * BasePistonError
      * InternalError
          * MissingDataError
      * ServerError
          * TooManyRequestsError
          * InternalServerError
          * NotFoundError
          * UnexpectedStatusError

.. autoclass:: ultra_piston.errors.BasePistonError
    :members:

.. autoclass:: ultra_piston.errors.InternalError
    :members:

.. autoclass:: ultra_piston.errors.ServerError
    :members:

.. autoclass:: ultra_piston.errors.MissingDataError
    :members:

.. autoclass:: ultra_piston.errors.TooManyRequestsError
    :members:

.. autoclass:: ultra_piston.errors.InternalServerError
    :members:

.. autoclass:: ultra_piston.errors.NotFoundError
    :members:

.. autoclass:: ultra_piston.errors.UnexpectedStatusError
    :members: