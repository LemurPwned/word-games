import itertools as it

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from nltk.corpus import wordnet as wn
from rich.console import Console

THEMES = {
    'zoo': [
        'lion', 'zebra', 'hyena', 'zoo', 'elephant', 'giraffe', 'monkey',
        'kangaroo'
    ],
    'ocean': [
        'whale', 'dolphin', 'fish', 'sea', 'ocean', 'ship', 'compass', 'boat',
        'sail'
    ],
    'forest': [
        'tree', 'forest', 'oak', 'pine', 'maple', 'lumberjack', 'birch',
        'woods', 'chop'
    ],
}


def get_graphvis(g):
    pos = nx.spring_layout(g, k=10)  # For better example looking
    labels = {e: f"{g.edges[e]['weight']:.2f}" for e in g.edges}
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw(g, pos, with_labels=True, ax=ax)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, ax=ax)


class WordHierarchy:
    def __init__(self, theme: str) -> None:
        if theme not in THEMES:
            raise ValueError(f"Theme {theme} not found")
        self.theme_seeds = THEMES[theme]

    def generate_seed(self):
        seeds = set()
        for theme_word in self.theme_seeds:
            seeds.update(self.iterate_graph(theme_word))

        return self.get_similarity_graph(seeds)

    def __call__(self, size: int = 10):
        full_graph = self.generate_seed()

        sampled_nodes = np.random.choice(full_graph.nodes, size, replace=False)
        return full_graph.subgraph(sampled_nodes)

    def get_similarity_graph(self, nodes):
        nodes = list(nodes)
        N = len(nodes)
        g = nx.Graph()
        for i, node in enumerate(nodes):
            g.add_node(i, data=node)

        for i in range(N):
            for j in range(i + 1, N):
                score = nodes[i].path_similarity(nodes[j])
                g.add_edge(i, j, weight=score)
        return g

    def iterate_graph(self, seed: str) -> None:
        seed_sysnet = wn.synset(f"{seed}.n.01")
        visited = set()

        def recurse(s):
            if not s in visited:
                visited.add(s)
                # get all the hypernyms of the current synset
                for s1 in s.hypernyms():
                    recurse(s1)

        recurse(seed_sysnet)
        return visited


class WordHierarchyEngine:
    def __init__(self, theme, game_size: int = 10):
        self.theme = theme
        self.game_size = game_size
        self.word_hierarchy = WordHierarchy(theme)
        self.console = Console()
        self.print = self.console.print

    def __call__(self):
        self.print(f"Generating seed for theme: __{self.theme}__")
        graph = self.word_hierarchy(self.game_size)
        self.print("Find a best sequence of words to represent the theme")
        visual_map = {
            graph.nodes[i]['data'].name().split(".")[0]: i
            for i in graph.nodes
        }
        for word in visual_map:
            self.print(word)
        user_input = self.console.input("Type your sequence of words: \n")
        user_input = user_input.split(",")
        user_words = [word.strip() for word in user_input]
        score = 0
        for i in range(len(user_words) - 1):
            if user_words[i] not in visual_map:
                self.print(f"{user_words[i]} is not in the theme")
                return
            node_i = visual_map[user_words[i]]
            node_j = visual_map[user_words[i + 1]]
            score += graph.edges[(node_i, node_j)]['weight']
        self.print(f"Your score is {score:.2f}")
        best_score, best_path = self.compute_best_score(
            graph, pathlen=len(user_words))
        self.print(f"The best score is {best_score:.2f}")
        self.print(f"The best path is {best_path}")


    def propose_improvement_pairs(self, user_nodes):
        """
        For user selected words, pick pairs such that their 
        similarity is maximal and propose them for improvement.
        """
        ...

    def compute_best_score(self, game_graph, pathlen: int = 5):

        nodes = list(game_graph.nodes)
        best_score, best_path = float("inf"), []
        for (start_n, stop_n) in it.combinations(nodes, 2):
            for path in nx.all_simple_paths(game_graph,
                                            start_n,
                                            stop_n,
                                            cutoff=pathlen):
                score = 0
                if len(path) != pathlen:
                    continue
                for i in range(len(path) - 1):
                    score += game_graph.edges[(path[i], path[i + 1])]['weight']
                if score < best_score:
                    best_score = score
                    best_path = [
                        game_graph.nodes[i]['data'].name().split(".")[0]
                        for i in path
                    ]
        return best_score, best_path


if __name__ == "__main__":
    engine = WordHierarchyEngine("ocean")
    engine()
