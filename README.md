# Ultra Piston
An all-in-one wrapper for the [Piston API](https://piston.readthedocs.io/en/latest/) in Python.

## ✨ Features

This library offers robust customization options and essential functionalities, including:
- Complete 100% API coverage
- Rich data models
- Support for both synchronous and asynchronous methods
- Automatic rate limit handling
- Pluggable HTTP driver system — implement your own custom driver for handling requests

---

## 📦 Requirements & Installation

This library supports python versions `3.10` and higher.

To install ultra-piston via pip-
```
(.venv) $ pip install ultra_piston
```

Or by uv-
```
$ uv add ultra_piston
```

---

## 🚀 Quick Start

```python
from ultra_piston import PistonClient, File

client = PistonClient()

result = client.post_execute(
    language="python3",
    version="3.10.0",
    file=File(content='print("Hello from ultra-piston!")'),
)

print(result.run.output)
```

Ultra Piston also provides async methods for all the available endpoints!
To use the asynchronous variant of a method, simply append `_async` to the name of its synchronous counterpart.

```python
import asyncio
from ultra_piston import PistonClient, File

client = PistonClient()

async def main():
    result = await client.post_execute_async(
        language="python3",
        version="3.10.0",
        file=File(content='print("Hello from ultra-piston!")'),
    )

    print(result.run.output)

asyncio.run(main())
```

---

## 🔗 Links

Documentation - API Reference & Guide: https://ultra-piston.readthedocs.io/en/latest/index.html

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.