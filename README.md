# PyRiddim
A totally unofficial Python wrapper for [Riddimbase.org](http://www.riddimbase.org/riddimbase.php).

# Instructions
The `PyRiddim()` constructor takes `q` `q_type` and `track` as arguments, uses those arguments to search Riddimbase and stores the data as a Pandas dataframe.

- `q` is the search query
- `q_type` is what to search for
- `track` toggles print statements while running the query (if ur impatient)

`q_type` defaults to riddim, but can also be *artist*, *tune*, *label*, *album* or *producer*.

`track` defaults to *False*.

To see the search results, use the `.info` method.

# Example
How many songs does Riddimbase have for the artist Gyptian?

Run `gyptian = PyRiddim('Gyptian', 'artist')` to execute the search, then `gyptian.info` to see the results.
