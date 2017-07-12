#!/usr/bin/env python

# Copyright 2016 NeuroData (http://neurodata.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# graph.py
# Created by Greg Kiar on 2016-01-27.
# Email: gkiar@jhu.edu

from __future__ import print_function

from itertools import combinations
from collections import defaultdict
import numpy as np
import networkx as nx
import nibabel as nb
import ndmg
import time
from zindex import XYZMorton

class fibergraph(object):
    def __init__(self, N, rois, attr=None):
        """
        Initializes the fiber graph.
        """
        self.g = nx.Graph(name="Generated by NeuroData's MRI Graphs (ndmg)",
                          version=ndmg.version,
                          date=time.asctime(time.localtime()),
                          source="http://m2g.io",
                          region="brain",
                          sensor="Diffusion MRI",
                          ecount=0,
                          vcount=len(n_ids)
                          )
        print(self.g.graph)
        pass

    def make_graph(self, streamlines, attr=None):
        """
        Takes streamlines and produces a graph

        **Positional Arguments:**

                streamlines:
                    - Fiber streamlines either file or array in a dipy EuDX
                      or compatible format.
        """
        nlines = np.shape(streamlines)[0]
        print("# of Streamlines: " + str(nlines))

        for idx, streamline in enumerate(streamlines):
            if (idx % int(nlines*0.05)) == 0:
                print(idx)

            points = np.round(streamline).astype(int)
            p = set()
            for point in points:
                try:
                    loc = XYZMorton((point[0], point[1], point[2]))
                except IndexError:
                    pass
                else:
                    pass

                if loc:
                    p.add(loc)

            edges = combinations(p, 2)
            for edge in edges:
                # use string here for overflow issues
                lst = tuple([str(node) for node in edge])
                self.edge_dict[tuple(sorted(lst))] += 1

        edge_list = [(k[0], k[1], v) for k, v in self.edge_dict.items()]
        self.g.add_weighted_edges_from(edge_list)
        pass

    def get_graph(self):
        """
        Returns the graph object created
        """
        try:
            return self.g
        except AttributeError:
            print("Error: the graph has not yet been defined.")
            pass

    def save_graph(self, graphname, fmt='gpickle'):
        """
        Saves the graph to disk

        **Positional Arguments:**

                graphname:
                    - Filename for the graph
        """
        nx.write_edgelist(self.g, graphname)
        pass

    def summary(self):
        """
        User friendly wrapping and display of graph properties
        """
        print("\n Graph Summary:")
        print(nx.info(self.g))
        pass
