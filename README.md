# Repository instruction

## Running

Set constants in file `constants.py` and run by:

    python flappy.py

## Plot image

Set constants in file `constants.py` and run by:

    python plot_chart.py

## /

### bot.py
Code for training.
### constants.py
Constants to change for different training parameter, etc.
### delete_data.py
Delete data of actual setted paramaters in `constants.py`.
### flappy.py
Game itself with added object for training and playing (`bot.py`).
### initialize_data.py
Prepare data files before running with new values.
### plot1.py - plot5.py
Addition plot generating images in `/images2` directory. It is for better visualisation of results.
### plot_all.py
Plot all the data in `/data` directory.
### plot_chart.py
Plot chart of data of actual setted paramaters in `constants.py`.
### plot_data_funcs.py
Functions for saving trained data.

## /assets
Audio, images, etc. for the game itself.

## /data
Folder for saving trained data.

## /images
Folder for saving figures generated by `plot_all.py` or `plot_chart.py`.

## /images2
Folder for saving figures generated by `plot1.py` - `plot5.py`.