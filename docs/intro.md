# FastDRY

Library to help writing reusable FastAPI components.

## Status

The library is **experimental**, the API might change at any 0.x release.
Please provide feedback and issue reports, preferably on GitHub.

## Usage

FastDRY is build on FastAPI `0.100` and pydantic 2.
Reusability is build around Python's class system,
which at first seems un

It brings an intuitive pythonic way to reuse, extend and mix functionality.
Routing is done on **instances** of `fastdry.cr.ClassRouter`.

This allows simple form of reusability:

---8<---[../examples/hello_world.py]---

The 

The decorators `fastdry.cr.X` mirror FastAPI,
with the exact same parameters.

---8<---[../examples/hello_world.py]---