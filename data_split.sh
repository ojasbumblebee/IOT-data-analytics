#!/usr/bin/env bash

python3 data_split.py -s bmp180 -p pressure --path /home/ojas/Documents/independent_study_harry_perros/chicago-complete.weekly.2018-12-17-to-2018-12-23

python3 data_split.py -s bmp180 -p temperature --path /home/ojas/Documents/independent_study_harry_perros/chicago-complete.weekly.2018-12-17-to-2018-12-23

python3 data_split.py -s tmp112 -p temperature --path /home/ojas/Documents/independent_study_harry_perros/chicago-complete.weekly.2018-12-17-to-2018-12-23

python3 data_split.py -s htu21d -p temperature --path /home/ojas/Documents/independent_study_harry_perros/chicago-complete.weekly.2018-12-17-to-2018-12-23

python3 data_split.py -s htu21d -p humidity --path /home/ojas/Documents/independent_study_harry_perros/chicago-complete.weekly.2018-12-17-to-2018-12-23

python3 data_split.py -s co -p concentration --path /home/ojas/Documents/independent_study_harry_perros/chicago-complete.weekly.2018-12-17-to-2018-12-23

python3 data_split.py -s so2 -p concentration --path /home/ojas/Documents/independent_study_harry_perros/chicago-complete.weekly.2018-12-17-to-2018-12-23

python3 data_split.py -s h2s -p concentration --path /home/ojas/Documents/independent_study_harry_perros/chicago-complete.weekly.2018-12-17-to-2018-12-23

