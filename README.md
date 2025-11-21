[![PyPI](https://img.shields.io/pypi/v/ultra-piston.svg?style=for-the-badge&logo=pypi&color=orange&logoColor=white)](https://pypi.org/project/ultra-piston/)
[![Github Releases](https://img.shields.io/github/v/release/Jiggly-Balls/ultra-piston?color=orange&include_prereleases&label=Latest%20Release&logo=github&sort=semver&style=for-the-badge&logoColor=white)](https://github.com/Jiggly-Balls/ultra-piston/releases)
[![Downloads](https://img.shields.io/pypi/dm/ultra-piston?label=Downloads%20/%20Month&color=orange&logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/ultra-piston/)
[![PyPI Downloads](https://img.shields.io/pepy/dt/ultra-piston?label=Total%20Downloads&color=orange&logo=pypi&logoColor=white&style=for-the-badge)](https://pepy.tech/projects/ultra-piston)
[![License](https://img.shields.io/github/license/Jiggly-Balls/ultra-piston?color=orange&logo=c&logoColor=white&style=for-the-badge)](https://github.com/Jiggly-Balls/ultra-piston/blob/main/LICENSE)
[![Docs](https://img.shields.io/readthedocs/ultra-piston?color=orange&logo=readthedocs&logoColor=white&style=for-the-badge)](https://ultra-piston.readthedocs.io/en/latest/)
![Versions](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?color=orange&logo=python&logoColor=white&style=for-the-badge)

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

- API Reference & Guide: https://ultra-piston.readthedocs.io/en/stable/
- PyPI Page: https://pypi.org/project/ultra-piston/

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
