Publications
===

Publication tracking database for NSC.

The scripts can run in Anaconda, but you can also create a smaller conda environment `pub` by running `conda env create`.

## Usage

First activate the Conda envrionment:

* `conda activate anaconda` OR
* `conda activate pub` if created with `conda env create`.

Run the scripts with `python`. Use `-h` switch for usage information.

* Add new publications: `add.py DOI_OR_PMID`.
* Make html file and graph: `make_updated_files.py`.


## Advanced usage

* List entries: `ls.py`.
* Modify publication: `modify.py`. Argument: row ID from LS or DOI.
* Remove: `rm.py ROW_ID` (give a row ID from ls.py output)

