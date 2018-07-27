# PyRiddim
A totally unofficial Python wrapper for [Riddimbase.org](http://www.riddimbase.org/riddimbase.php).

# Installation
To install with pip, run

`pip install PyRiddim.py`

You can also clone this repository and run `python setup.py install`.

# Instructions
The `PyRiddim()` constructor takes `q` `q_type` and `track` as arguments, uses those arguments to search Riddimbase and stores the data as a Pandas dataframe.

- `q` is the search query
- `q_type` is what you are searching for (default is *riddim*, but can also be *artist*, *tune*, *label*, *album* or *producer*.)
- `track` toggles print statements while running the query (if ur impatient)

`track` defaults to *False*.

To see the search results, use the `.info` method.

# Example
How many songs does Riddimbase have for the artist Gyptian?

Run

`gyptian = PyRiddim(q='Gyptian', q_type='artist')`

to execute the search, then

`gyptian.info`

to see the results.
