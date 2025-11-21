.. currentmodule:: ultra_piston

Models
======

.. autoclass:: ultra_piston.CompileStage
  :members: code, output, stderr, stdout, signal
  :no-index:

.. autoclass:: ultra_piston.ExecutionOutput
  :members: language, version, run, compile, compile_memory_limit, compile_timeout
  :no-index:

.. autoclass:: ultra_piston.File
  :members: name, content, encoding
  :no-index:

.. autoclass:: ultra_piston.Package
  :members: language, language_version, installed
  :no-index:

.. autoclass:: ultra_piston.RunStage
  :members: code, output, stderr, stdout, signal
  :no-index:

.. autoclass:: ultra_piston.Runtime
  :members: language, version, aliases, runtime
  :no-index:
  