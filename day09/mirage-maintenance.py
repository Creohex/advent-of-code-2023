#!python


def next_bfs(sequence, backwards=False):
    layers = [sequence]
    index = 0 if backwards else -1

    while any(layers[-1]):
        new_sequence = []
        for i in range(len(layers[-1]) - 1):
            new_sequence.append(layers[-1][i + 1] - layers[-1][i])
        layers.append(new_sequence)

    val = layers[-1][index]
    for layer in reversed(layers[:-1]):
        new_val = layer[index] + (val * (-1 if backwards else 1))
        layer.insert(0 if backwards else len(layer), new_val)
        val = new_val

    return layers[0][index]


with open("./input", "r") as f:
    report = [[int(v) for v in l] for l in map(str.split, f.readlines())]

# part 1:
print(sum(map(next_bfs, report)))

# part 2:
print(sum(next_bfs(r, backwards=True) for r in report))
