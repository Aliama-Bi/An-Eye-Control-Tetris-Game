<!--
 * @Author: Chloe Bi
 * @Date: 2020-05-13 14:12:13
 * @LastEditTime: 2020-05-13 15:06:41
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: /Tetris_3.0.py/README.md
 -->

# Tetris Game

## Prerequisites

Install the PyGame Module with version same as your python, **not PC**. 

Source for windows:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

To install PyGame on a Windows system: 

```
# example
pip install pygame-1.9.3-cp36-cp36m-win32.whl
# or 
py -m pip install pygame --user
# remember you should have `pip` install beforehand
```

Successfully download will show message below:

```
Installing collected packages: pygame

Successfully installed pygame-1.9.3
```

*import pygame* won't get error means download successfully. 

To install PyGame on a unix based system (does not include Mac):

```
python3 -m pip install pygame --user
```

To install on a Mac, use **homebrew**

## Running the Game

- Rstudio

1. Set working directory to the folder '/Eye-Movement-Game', find RMD file *Link_R_Python* '/Eye-Movement-Game/Stacey and Chloe Code/Link_R_Python.rmd'

2. Change wave file address:
in below R chunk:
```{r}
# Load model
model <- readRDS("Models/rf_model2.rds")
# Load wave file 
wave_file <  ## add wave file address here##
  
# -------------- sample------------ #
# wave_file <- readRDS("/Users/doctor/Documents/GitHub/Eye-Movement-Game/Best-Data/RDS_files/best_wave_seq.rds")
# wave_label <- readRDS("Best-Data/RDS_files/best_wave_LABEL.rds")
# ------------------------------------------ #
```

3. Run the whole R script, run below function to start generating event instructions:
```{r}
Begin_Training()
```
The **instruction.txt** file is located in '/Tetris/instruction.txt' 

- Python

Navigate to the folder '/Eye-Movement-Game/Tetris' where all the game information is stored in CMD or Terminal and enter the following command:

```
python3 Tetris_3.0.py
```

Click space to start the game

## Built With

- PyGame 1.9.6
- VsCode - The IDE I used. 
- Python3.8.2 64-bit