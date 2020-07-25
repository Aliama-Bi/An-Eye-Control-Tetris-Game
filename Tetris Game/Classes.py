#########################################
# File name: Classes.py                 #
# No need to modify                     #
#########################################
import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
CYAN = (0, 183, 235)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
TRANS_WHITE = (255, 255, 255, 50)
COLOURS = [BLACK, RED, GREEN, BLUE, ORANGE, CYAN, MAGENTA, YELLOW, WHITE]
CLR_names = ['black', 'red', 'green', 'blue', 'orange', 'cyan', 'magenta', 'yellow', 'white']
figures = [None, 'Z', 'S', 'J', 'L', 'I', 'T', 'O', None]


class Block(object):
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           drawself.blocks
            clr - colour
    """

    def __init__(self, col=1, row=1, clr=1):
        self.col = col
        self.row = row
        self.clr = clr

    def __str__(self):
        return '(' + str(self.col) + ',' + str(self.row) + ') ' + CLR_names[self.clr]

    def __eq__(self, other):
        if self.col == other.col and self.row == other.row:
            return True

    def draw(self, surface, gridsize=20, shadow=False):
        x = self.col * gridsize
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        if not shadow:
            pygame.draw.rect(surface, CLR, (x, y, gridsize - 2, gridsize - 2), 0)
            pygame.draw.rect(surface, WHITE, (x, y, gridsize, gridsize), 2)

        else:
            pygame.draw.rect(surface, TRANS_WHITE, (x, y, gridsize, gridsize), 3)

    def move_down(self):
        self.row = self.row + 1

    # --------------------------------------- #


class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """

    def __init__(self, col=1, row=1, blocksNo=1):
        self.col = col
        self.row = row
        self.clr = 0
        self.blocks = [Block()] * blocksNo
        self._colOffsets = [0] * blocksNo
        self._rowOffsets = [0] * blocksNo

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col + self._colOffsets[i]
            blockROW = self.row + self._rowOffsets[i]
            blockCLR = self.clr
            self.blocks[i] = Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize, shadow=False):
        for block in self.blocks:
            block.draw(surface, gridsize, shadow)

    def collides(self, other):
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block == obstacle:
                    return True
        return False

    def append(self, other):
        """ Append all blocks from another cluster to this one.
        """
        for block in other.blocks:
            self.blocks.append(block)


# -------------------------------------- #


class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """

    def __init__(self, col=0, row=0, blocksNo=0):
        Cluster.__init__(self, col, row, blocksNo)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print((block)._colOffsets)

    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        for block in self.blocks:
            rows.append(block.row)

        for row in range(top, bottom):
            if rows.count(row) == columns:
                fullRows.append(row)
        return fullRows

    def removeFullRows(self, fullRows):
        for row in fullRows:
            for i in reversed(range(len(self.blocks))):
                if self.blocks[i].row == row:
                    self.blocks.pop(i)
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()


# ---------------------------------------#
class Shape(Cluster):
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """

    def __init__(self, col=1, row=1, clr=1, rot=1, shadow=False):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self.shadow = shadow
        self._rot = rot
        self._colOffsets = [-1, 0, 0, 1]
        self._rowOffsets = [-1, -1, 0, 0]
        self._rotate()

    def __str__(self):
        return figures[self.clr] + ' (' + str(self.col) + ',' + str(self.row) + ') ' + CLR_names[self.clr]

    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:
            _colOffsets = [[-1, -1, 0, 0], [-1, 0, 0, 1], [1, 1, 0, 0], [1, 0, 0, -1]]
            _rowOffsets = [[1, 0, 0, -1], [-1, -1, 0, 0], [-1, 0, 0, 1], [1, 1, 0, 0]]
        elif self.clr == 2:
            _colOffsets = [[-1, -1, 0, 0], [1, 0, 0, -1], [1, 1, 0, 0], [-1, 0, 0, 1]]
            _rowOffsets = [[-1, 0, 0, 1], [-1, -1, 0, 0], [1, 0, 0, -1], [1, 1, 0, 0]]
        elif self.clr == 3:
            _colOffsets = [[-1, 0, 0, 0], [-1, -1, 0, 1], [1, 0, 0, 0], [1, 1, 0, -1]]
            _rowOffsets = [[1, 1, 0, -1], [-1, 0, 0, 0], [-1, -1, 0, 1], [1, 0, 0, 0]]
        elif self.clr == 4:
            _colOffsets = [[-1, 0, 0, 0], [1, 1, 0, -1], [1, 0, 0, 0], [-1, -1, 0, 1]]
            _rowOffsets = [[-1, -1, 0, 1], [-1, 0, 0, 0], [1, 1, 0, -1], [1, 0, 0, 0]]
        elif self.clr == 5:
            _colOffsets = [[0, 0, 0, 0], [2, 1, 0, -1], [0, 0, 0, 0], [-2, -1, 0, 1]]
            _rowOffsets = [[-2, -1, 0, 1], [0, 0, 0, 0], [2, 1, 0, -1], [0, 0, 0, 0]]
        elif self.clr == 6:
            _colOffsets = [[0, -1, 0, 0], [-1, 0, 0, 1], [0, 1, 0, 0], [1, 0, 0, -1]]  #
            _rowOffsets = [[1, 0, 0, -1], [0, -1, 0, 0], [-1, 0, 0, 1], [0, 1, 0, 0]]  #
        elif self.clr == 7:
            _colOffsets = [[-1, -1, 0, 0], [-1, -1, 0, 0], [-1, -1, 0, 0], [-1, -1, 0, 0]]
            _rowOffsets = [[0, -1, 0, -1], [0, -1, 0, -1], [0, -1, 0, -1], [0, -1, 0, -1]]
        self._colOffsets = _colOffsets[self._rot]
        self._rowOffsets = _rowOffsets[self._rot]
        self._update()

    def move_left(self):
        self.col = self.col - 1
        self._update()

    def move_right(self):
        self.col = self.col + 1
        self._update()

    def move_down(self):
        self.row = self.row + 1
        self._update()

    def move_up(self):
        self.row = self.row - 1
        self._update()

    def rotateClkwise(self):
        self._rot = (self._rot + 1) % 4

    def rotateCntclkwise(self):
        self._rot = (self._rot - 1) % 4


# --------------------------------------- #


class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """

    def __init__(self, col=1, row=1, blocksNo=1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i
        self._update()


# --------------------------------------- #


class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """

    def __init__(self, col=1, row=1, blocksNo=1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i
        self._update()
