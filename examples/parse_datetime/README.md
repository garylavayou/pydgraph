# Parse DateTime Automatically

Simple demonstration on how to automatically convert Dgraph's DateTime strings to native python
datetime objects. This example expands on the `simple.py` demonstration. It uses a JSON custom
[object hook](https://docs.python.org/3/library/json.html#encoders-and-decoders) which iterates over
the return object. You can explore the source code in the `parse_datetime.py` file.

## Running

The conditions for running this example are the same as described in the
[simple example](https://github.com/hypermodeinc/pydgraph/tree/master/examples/simple).
