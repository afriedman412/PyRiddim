# PyRiddim
---
A totally unofficial Python wrapper for [Riddimbase.org](http://www.riddimbase.org/riddimbase.php).

# Usage
---
The `PyRiddim()` constructor takes **q**, **q_type** and **track** as arguments, uses those arguments to query Riddimbase and stores the data as a Pandas dataframe.

- **q** is the search query
- **q_type** is what to search for
- **track** toggles print statements while running the query (if ur impatient)

**q_type** defaults to riddim, but can also be artist, tune, label, album or producer.

**track** defaults to False.


