import os
import pygame
from os import path, walk
import random as rd
from random import random, uniform
import numpy as np
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
TILE_SIZE = 64