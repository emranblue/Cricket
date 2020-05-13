#!/usr/bin/env python3
import cricket as cr
import sys
game=cr.Game(sys.argv[1])
game.create_table()
game.play()
