import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.DirectoryScanner import DirectoryScanner as dr

dr_test = dr('../data')
dr_test.displayAsTree()